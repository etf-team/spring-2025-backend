from datetime import datetime, timedelta, time
from decimal import Decimal
import re
from enum import StrEnum

import pandas as pd
from pydantic import BaseModel

from sample_core.models import ApplicationConfig, PowerHoursNet
from sample_core.models.client_case import PowerConsumptionEntry, ClientCase
from sample_core.models.power_hours_ats import PowerHoursAtsRecord
from sample_core.models.voltage_category import VoltageCategoryEnum


def pd_read_excel_sel_rect_kws(
        rect_spec: str,
):
    r, l = rect_spec.split(":")
    regex = re.compile(r"(\D+)(\d+)")
    lcol, lrow = regex.match(l).groups()
    rcol, rrow = regex.match(r).groups()

    res = {
        "skiprows": min(int(lrow), int(rrow)) - 1,
        "nrows": abs(int(lrow) - int(rrow)) + 1,
        "usecols": f"{rcol}:{lcol}",
    }
    return res


class PriceCategoryTypeEnum(StrEnum):
    FIRST = "FIRST"
    SECOND_TWO_RANGES = "SECOND_TWO_RANGES"
    SECOND_THREE_RANGES = "SECOND_THREE_RANGES"
    THIRD = "THIRD"
    FORTH = "FORTH"
    FIFTH = "FIFTH"
    SIXTH = "SIXTH"


class BaseParsedCategory(BaseModel):
    def get_type(self) -> PriceCategoryTypeEnum:
        pass

    def evaluate_case_cost(
            self,
            app_config: ApplicationConfig,
            power_hours_ast_records: PowerHoursAtsRecord,
            power_hours_net: PowerHoursNet,
            case: ClientCase,
    ) -> Decimal:
        pass


class ParsedPricesInfoCat1(BaseParsedCategory):
    power_capacity_prices_full: dict[
        VoltageCategoryEnum,
        Decimal,
    ]
    power_capacity_prices_no_sup: dict[
        VoltageCategoryEnum,
        Decimal,
    ]

    def get_type(self) -> PriceCategoryTypeEnum:
        return PriceCategoryTypeEnum.FIRST

    def evaluate_case_cost(
            self,
            app_config: ApplicationConfig,
            power_hours_ast_records: PowerHoursAtsRecord,
            power_hours_net: PowerHoursNet,
            case: ClientCase,
    ) -> Decimal:
        if case.is_transmission_included:
            return (
                self.power_capacity_prices_full[case.voltage_category]
                * Decimal(case.total_power_capacity_mwt)
            )
        else:
            return (
                self.power_capacity_prices_no_sup[case.voltage_category]
                * Decimal(case.total_power_capacity_mwt)
            )


class Cat3Or4Entry(BaseModel):
    price: Decimal
    other: Decimal
    sales_allowance_before_670: Decimal
    sales_allowance_600_1000: Decimal
    sales_allowance_higher_than_10000: Decimal
    vn: Decimal
    sn1: Decimal
    sn11: Decimal
    nn: Decimal


class ParsedPricesInfoCat3Or4(BaseModel):
    by_datetimes: dict[datetime, Cat3Or4Entry]


class ParsedPricesInfoCat3(BaseParsedCategory):
    by_datetimes: dict[datetime, Cat3Or4Entry]

    def get_type(self) -> PriceCategoryTypeEnum:
        return PriceCategoryTypeEnum.THIRD

    def evaluate_case_cost(
            self,
            app_config: ApplicationConfig,
            power_hours_ast_records: list[PowerHoursAtsRecord],
            power_hours_net: PowerHoursNet,
            case: ClientCase,
    ) -> Decimal:
        energy_cost = Decimal(0)
        power_points_ast = []
        ast_records_iter = iter(sorted(power_hours_ast_records, key=lambda x: x.date))
        current_ast_record = next(ast_records_iter)
        for case_entry, (price_dt, price_entry) \
                in zip(case.power_consumption_entries, self.by_datetimes.items()):
            assert case_entry.time == price_dt.time()

            amount_mwt = Decimal(case_entry.amount_mwt)
            energy_cost += amount_mwt * price_entry.price

            if case.max_power_capacity_kwt < 670:
                regulated_service_price = price_entry.sales_allowance_before_670
            elif case.max_power_capacity_kwt <= 10_000:
                regulated_service_price = price_entry.sales_allowance_600_1000
            else:
                regulated_service_price = price_entry.sales_allowance_higher_than_10000
            energy_cost += amount_mwt * regulated_service_price

            if case.is_transmission_included:
                if case.voltage_category is VoltageCategoryEnum.HH:
                    transmission_price = price_entry.nn
                elif case.voltage_category is VoltageCategoryEnum.CH1:
                    transmission_price = price_entry.sn1
                elif case.voltage_category is VoltageCategoryEnum.CH11:
                    transmission_price = price_entry.sn11
                elif case.voltage_category is VoltageCategoryEnum.BH:
                    transmission_price = price_entry.vn
                else:
                    raise TypeError(case.voltage_category)

                energy_cost += amount_mwt * transmission_price

            # power
            print(price_dt, str(current_ast_record))
            if price_dt.time().hour == \
                    current_ast_record.hour:
                print("Accepted")
                if current_ast_record.date > price_dt.date():
                    continue
                if current_ast_record.date < price_dt.date():
                    breakpoint()
                    raise RuntimeError("Lack of ATS records")
                power_points_ast.append(amount_mwt)
                try:
                    current_ast_record = next(ast_records_iter)
                except StopIteration:
                    print('Stop iteration')
                    pass

        power_cost = (sum(power_points_ast)
                      / Decimal(len(power_points_ast))
                      * app_config.power_price)

        return energy_cost + power_cost


class ParsedPricesInfoCat4(BaseParsedCategory):
    by_datetimes: dict[datetime, Cat3Or4Entry]

    def get_type(self) -> PriceCategoryTypeEnum:
        return PriceCategoryTypeEnum.FORTH

    def evaluate_case_cost(
            self,
            app_config: ApplicationConfig,
            power_hours_ast_records: list[PowerHoursAtsRecord],
            power_hours_net: PowerHoursNet,
            case: ClientCase,
    ) -> Decimal:
        energy_cost = Decimal(0)
        power_points_ast = []
        power_points_net = []
        ast_records_iter = iter(sorted(power_hours_ast_records, key=lambda x: x.date))
        current_ast_record = next(ast_records_iter)

        for case_entry, (price_dt, price_entry) \
                in zip(case.power_consumption_entries, self.by_datetimes.items()):
            assert case_entry.time == price_dt.time()

            amount_mwt = Decimal(case_entry.amount_mwt)
            energy_cost += amount_mwt * price_entry.price

            if case.max_power_capacity_kwt < 670:
                regulated_service_price = price_entry.sales_allowance_before_670
            elif case.max_power_capacity_kwt <= 10_000:
                regulated_service_price = price_entry.sales_allowance_600_1000
            else:
                regulated_service_price = price_entry.sales_allowance_higher_than_10000
            energy_cost += amount_mwt * regulated_service_price

            if case.is_transmission_included:
                if case.voltage_category is VoltageCategoryEnum.HH:
                    transmission_price = price_entry.nn
                elif case.voltage_category is VoltageCategoryEnum.CH1:
                    transmission_price = price_entry.sn1
                elif case.voltage_category is VoltageCategoryEnum.CH11:
                    transmission_price = price_entry.sn11
                elif case.voltage_category is VoltageCategoryEnum.BH:
                    transmission_price = price_entry.vn
                else:
                    raise TypeError(case.voltage_category)

                energy_cost += amount_mwt * transmission_price


            # power
            print(price_dt, str(current_ast_record))
            if price_dt.time().hour == \
                    current_ast_record.hour:
                print("Accepted")
                if current_ast_record.date > price_dt.date():
                    continue
                if current_ast_record.date < price_dt.date():
                    breakpoint()
                    raise RuntimeError("Lack of ATS records")
                power_points_ast.append(amount_mwt)
                try:
                    current_ast_record = next(ast_records_iter)
                except StopIteration:
                    print('Stop iteration')
                    pass

            if case.is_transmission_included:
                if str(price_dt.time().hour) in power_hours_net.include_hours:
                    power_points_net.append(case_entry.amount_kwt)

        power_cost = (sum(power_points_ast)
                      / Decimal(len(power_points_ast))
                      * app_config.power_price)

        if case.is_transmission_included:
            power_cost_net = (
                    Decimal(sum(power_points_net))
                    / Decimal(len(power_points_net))
                    * app_config.power_price_net)
        else:
            power_cost_net = 0

        return energy_cost + power_cost + power_cost_net


class ServiceDocsParser:
    def parse_xlsx_prices_info_cat1(
            self,
            path: str,
    ) -> ParsedPricesInfoCat1:
        df1 = pd.read_excel(
            path,
            sheet_name="1, 2 ц.к.",
            names=["ВН", "СН1", "СН11", "НН"],
            **pd_read_excel_sel_rect_kws("K9:N10"),
        )
        df2 = pd.read_excel(
            path,
            sheet_name="1, 2 ц.к.",
            names=["ВН", "СН1", "СН11", "НН"],
            **pd_read_excel_sel_rect_kws("O9:R10"),
        )
        return ParsedPricesInfoCat1(
            power_capacity_prices_full=dict(
                zip(map(VoltageCategoryEnum.from_any_lang, df1.columns.values), df1.values[0])
            ),
            power_capacity_prices_no_sup=dict(
                zip(map(VoltageCategoryEnum.from_any_lang, df2.columns.values), df2.values[0])
            ),
        )

    def parse_xlsx_prices_info_cat4(
            self,
            path: str,
    ) -> ParsedPricesInfoCat4:
        as_cat_3 = self.parse_xlsx_prices_info_cat3(
            path=path,
            _sheet_name="четвертая ц.к.",
        )
        return ParsedPricesInfoCat4.model_validate(
            as_cat_3, from_attributes=True,
        )

    def parse_xlsx_prices_info_cat3(
            self,
            path: str,
            _sheet_name: str = "третья ц.к."
    ) -> ParsedPricesInfoCat3:
        df1 = pd.read_excel(
            path,
            usecols="A",
            sheet_name=_sheet_name,
        )
        dates = []
        for i in df1.values:
            v = i[0]
            if isinstance(v, datetime):
                dates.append(v)

        if _sheet_name == "третья ц.к.":
            selector = f"C9:K{10+len(dates)*24}"
        elif _sheet_name == "четвертая ц.к.":
            selector = f"C9:L{10+len(dates)*24}"
        else:
            raise ValueError(_sheet_name)

        df2 = pd.read_excel(
            path,
            sheet_name=_sheet_name,
            **pd_read_excel_sel_rect_kws(selector)
        )
        if _sheet_name == "четвертая ц.к.":
            del df2["ВН1*"]
        entries = []
        for i in df2.values:
            (
                price, other,
                sales_allowance_before_670,
                sales_allowance_600_1000,
                sales_allowance_higher_than_10000,
                vn, sn1, sn11, nn,
            ) = i
            entry = Cat3Or4Entry(
                price=price,
                other=other,
                sales_allowance_before_670=sales_allowance_before_670,
                sales_allowance_600_1000=sales_allowance_600_1000,
                sales_allowance_higher_than_10000=sales_allowance_higher_than_10000,
                vn=vn,
                sn1=sn1,
                sn11=sn11,
                nn=nn,
            )
            entries.append(entry)
        by_datetimes = dict()
        entries_iterator = iter(entries)
        for i in dates:
            for j in range(24):
                by_datetimes.update({
                    i.replace(hour=j): next(entries_iterator),
                })
        return ParsedPricesInfoCat3(
            by_datetimes=by_datetimes,
        )

    def parse_xlsx_power_consumption_entries(
            self,
            name: str,
    ) -> list[PowerConsumptionEntry]:
        df = pd.read_excel(
            name,
            parse_dates=True,
        )
        results = []

        # try horizontal
        for n, i in enumerate(df.iloc[:, 0]):
            if isinstance(i, datetime):
                for hour, j in enumerate(df.iloc[n].values):
                    results.append(PowerConsumptionEntry(
                        time=time(hour=hour),
                        day=n+1,
                        date=i.date(),
                        duration=timedelta(hours=1),
                        amount_kwt=j,
                    ))

        if results:
            return results

        # try vertical
        days = df.iloc[:, 0][~df.iloc[:, 0].isna()]
        offset = days.index[0]
        hours = df.iloc[offset:, 1]
        power_capacities = df.iloc[offset:, 2]
        for day, hour, power_capacity \
                in zip(days, hours, power_capacities):
            if isinstance(day, datetime):
                date_ = day
                day = date_.day
            elif isinstance(day, float):
                date_ = None
            else:
                raise ValueError(day)

            results.append(PowerConsumptionEntry(
                date=date_,
                day=day,
                time=time(hour=int(hour)),
                duration=timedelta(hours=1),
                amount_kwt=power_capacity,
            ))

        return results
