from decimal import Decimal

from fastapi import APIRouter, UploadFile

from sample_core.models.resolved_volumes_info import (
    ResolvedVolumesInfo,
    ResolvedCategoryInfo,
)

router = APIRouter()


@router.post("/volumes-info")
async def create_volumes_info(
        payload: UploadFile,
        return_resolved: bool = True,
) -> ResolvedVolumesInfo:
    # volumes_info = VolumesInfo.from_xlsx(
    #     data=await payload.read(),
    # )
    return ResolvedVolumesInfo(
        categories=[
            ResolvedCategoryInfo(
                category_name="Первая ценовая категория",
                total_cost=Decimal(1000),
            ),
            ResolvedCategoryInfo(
                category_name="Третья ценовая категория",
                total_cost=Decimal(2000),
            ),
            ResolvedCategoryInfo(
                category_name="Шестая ценовая категория",
                total_cost=Decimal(2500),
            ),
        ],
    )
