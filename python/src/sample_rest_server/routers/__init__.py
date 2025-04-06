from fastapi import APIRouter

from sample_rest_server.dishka import openapi_auth_dep
from . import (
    auth,
    client_cases,
)


# ===== OUTER (unprotected) ROUTER =====
outer_router = APIRouter()

# outer_router.include_router(auth.router)
outer_router.include_router(client_cases.router)

# ===== INNER (protected) ROUTER =======
inner_router = APIRouter(
    dependencies=[openapi_auth_dep],
)

# ========== GENERAL ROUTER ============
router = APIRouter()

router.include_router(outer_router)
router.include_router(inner_router)
