from data_repository import DataRepository
from ReadGoogleExcel import (
    AddSpreadSheetData, getSpreadSheetData,
    getSpreadSheetDataUniteDates, initService
)
from DataParser import GoogleSpreadDataParser


class GoogleSheetsRepository(DataRepository):

    def add_order(self, data_pack):
        if not initService():
            return False
        result = AddSpreadSheetData(data_pack.toGoogleSpreadSheetFormat())
        return bool(result)

    def get_orders_by_shipping_date(self, shipping_date_str):
        if not initService():
            return []
        rawDatas = getSpreadSheetData()
        parser = GoogleSpreadDataParser()
        orders = []
        filtered = rawDatas[rawDatas['出貨日期'] == shipping_date_str]
        for row in filtered[GoogleSpreadDataParser.interestColumn].iterrows():
            parser.setData(row)
            orders.append(parser.parse())
        return orders

    def get_available_shipping_dates(self):
        if not initService():
            return []
        return getSpreadSheetDataUniteDates()
