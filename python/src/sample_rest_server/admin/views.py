from sqladmin import ModelView

from sample_core.models import PowerHoursAtsRecord
from sample_core.models.category_price_info_file import CategoryPriceInfoFile
from sample_core.models.power_hours_net import PowerHoursNet
from sample_core.models.user import (
    User,
)
from sample_core.models.application_config import ApplicationConfig


class UserAdmin(ModelView, model=User):
    column_list = [
        "id",
        "email",
        "phone_number",
        "full_name",
        "description",
        "created_at",
    ]


class ApplicationConfigAdmin(ModelView, model=ApplicationConfig):
    name = "Глобальная конфигурация приложения"
    name_plural = name

    column_list = [
        "power_price",
        "power_price_net",
        "comes_info_force_from",
    ]
    column_labels = {
        "power_price": "Цена за мощность на розничном рынке (за МВт)",
        "power_price_net": "Цена за мощность при передаче (за МВт)",
        "comes_info_force_from": "Конфигурация вступает в силу с",
    }


class CategoryPriceInfoFileAdmin(ModelView, model=CategoryPriceInfoFile):
    name = "Файл с тарифами ЦК на месяц (запись в реестре)"
    name_plural = "Реестр файлов с тарифами ЦК на месяц."

    column_list = [
        "file",
        "comment",
        "comes_info_force_from",
    ]
    column_labels = {
        "file": "Файл с тарифами ЦК на месяц",
        "comment": "Комментарий",
        "comes_info_force_from": "Вступает в силу с",
    }


class PowerHoursNetAdmin(ModelView, model=PowerHoursNet):
    name = "Конфигурация пиковых часов сетевой организации"
    name_plural = name

    column_list = [
        "include_hours",
        "comes_info_force_from",
    ]
    column_labels = {
        "include_hours": "Часы пик",
        "comes_info_force_from": "Конфигурация вступает в силу с",
    }


class PowerHoursAtsRecordAdmin(ModelView, model=PowerHoursAtsRecord):
    name = "Конфигурация пиковых часов АТС"
    name_plural = name

    column_list = [
        "date",
        "hour",
    ]
    column_labels = {
        "date": "Дата",
        "hour": "Пиковый час",
    }
