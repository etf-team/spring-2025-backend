from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from sample_core.models import CategoryPriceInfoFile, ApplicationConfig, \
    PowerHoursNet
from sample_core.models.client_case import ClientCase
from sample_core.models.client_case_category_applicability import \
    ClientCaseCategoryApplicability
from sample_core.models.client_case_resolved import (
    ClientCaseResolvedCategory,
    ClientCaseResolved,
)
from sample_core.models.power_hours_ats import PowerHoursAtsRecord
from sample_core.services.docs_parser import ServiceDocsParser


class ServiceClientCaseResolver:
    def __init__(
            self,
            orm_session: AsyncSession,
            service_docs_parser: ServiceDocsParser,
    ):
        self.orm_session = orm_session
        self.service_docs_parser = service_docs_parser

    async def resolve_case(
            self,
            case: ClientCase,
    ) -> ClientCaseResolved:
        # todo: save input into temporary table and evaluate
        #  results using SQL or directly supply input data within
        #  calculation query to improve performance

        stmt = (select(CategoryPriceInfoFile)
                .order_by(func.abs(func.extract("epoch", CategoryPriceInfoFile.comes_into_force_from)
                                   - func.extract("epoch", datetime.now())).asc()))
        files = await self.orm_session.scalars(stmt)
        files = list(files)
        elected_file = files[0]
        parsed_cat_1 = self.service_docs_parser.parse_xlsx_prices_info_cat1(
            elected_file.file)
        parsed_cat_3 = self.service_docs_parser.parse_xlsx_prices_info_cat3(
            elected_file.file)
        parsed_cat_4 = self.service_docs_parser.parse_xlsx_prices_info_cat4(
            elected_file.file)

        stmt = select(ApplicationConfig)
        app_config = await self.orm_session.scalar(stmt)

        stmt = (select(PowerHoursAtsRecord)
                .where(func.date_part("year", PowerHoursAtsRecord.date) == elected_file.comes_into_force_from.year)
                .where(func.date_part("month", PowerHoursAtsRecord.date) == elected_file.comes_into_force_from.month))
        power_hours_ast_records = await self.orm_session.scalars(stmt)
        power_hours_ast_records = list(power_hours_ast_records)

        stmt = select(PowerHoursNet)
        power_hours_net = await self.orm_session.scalar(stmt)

        resolved_categories = []
        for i in [parsed_cat_1, parsed_cat_3, parsed_cat_4]:
            resolved_categories.append(
                ClientCaseResolvedCategory(
                    applicability=ClientCaseCategoryApplicability(
                        is_applicable_power_capacity=True,
                        power_capacity_change_recommendation=0,
                    ),
                    category_type=i.get_type(),
                    total_cost=i.evaluate_case_cost(
                        app_config=app_config,
                        power_hours_ast_records=power_hours_ast_records,
                        power_hours_net=power_hours_net,
                        case=case,
                    )
                )
            )

        return ClientCaseResolved(
            categories=resolved_categories,
        )
