from fastapi import APIRouter

from sample_rest_api.infrastructure import openapi_auth_dep
from . import (
    auth,
)

router = APIRouter()

outer_router = APIRouter()
outer_router.include_router(auth.router)

inner_router = APIRouter(
    dependencies=[openapi_auth_dep],
)

router.include_router(outer_router)
router.include_router(inner_router)
