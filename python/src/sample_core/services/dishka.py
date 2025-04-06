from dishka import Provider, provide, Scope

from sample_core.services.client_case_resolver import ServiceClientCaseResolver
from .docs_parser import ServiceDocsParser

class ProviderCoreServices(Provider):
    get_service_client_case_resolver = provide(
        ServiceClientCaseResolver,
        scope=Scope.REQUEST,
    )

    get_service_docs_parser = provide(
        ServiceDocsParser,
        scope=Scope.REQUEST,
    )
