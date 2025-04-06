from tempfile import NamedTemporaryFile

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, UploadFile
from starlette import status

from sample_core.models.client_case import ClientCase
from sample_core.models.client_case_resolved import (
    ClientCaseResolved,
)
from sample_core.models.voltage_category import VoltageCategoryEnum
from sample_core.services import ServiceClientCaseResolver
from sample_core.services.docs_parser import ServiceDocsParser

router = APIRouter()


@router.post(
    "/clients/cases",
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_volumes_info(
        client_case_resolver: FromDishka[ServiceClientCaseResolver],
        service_docs_parser: FromDishka[ServiceDocsParser],
        payload: UploadFile,
        is_transmission_included: bool,
        max_power_capacity_kwt: float,
        voltage_category: VoltageCategoryEnum,
) -> ClientCaseResolved:
    file_data = await payload.read()
    tempfile = NamedTemporaryFile(suffix=".xls")
    with open(tempfile.name, "wb") as fs:
        fs.write(file_data)
    power_consumption_entries = \
        service_docs_parser.parse_xlsx_power_consumption_entries(tempfile.name)
    case = ClientCase(
        is_transmission_included=is_transmission_included,
        max_power_capacity_kwt=max_power_capacity_kwt,
        voltage_category=voltage_category,
        power_consumption_entries=power_consumption_entries,
    )
    return await client_case_resolver.resolve_case(case)
