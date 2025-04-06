from sqlalchemy.ext.asyncio import AsyncSession


class ClientCaseInferrer:
    def __init__(
            self,
            orm_session: AsyncSession,
    ):
        self.orm_session = orm_session
