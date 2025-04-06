# todo: rm this as SQLAlchemy already keeps this models in a registry.

from sample_core.utils import Registry

from .first import PriceCategoryFirst
from .second import PriceCategorySecond
from .third import PriceCategoryThird
from .fourth import PriceCategoryFourth


price_categories_registry = Registry()

price_categories_registry.register(PriceCategoryFirst)
price_categories_registry.register(PriceCategorySecond)
price_categories_registry.register(PriceCategoryThird)
price_categories_registry.register(PriceCategoryFourth)
