from DataPack import DataPack


class ParserBase():
    def parse(self, dt) -> DataPack:
        raise NotImplementedError

import re
class ReDataParser(ParserBase):
    def parse(self, dt) -> DataPack:
        def search(pattern, dt):
            result = re.search(pattern, dt, re.MULTILINE)
            if result is not None:
                return result.groups()
            return []

        def getName():
            pattern = r"^.+[姓名|收件人].{1}(.*)"
            group = search(pattern, dt)
            return group[0].strip() if len(group) > 0 else ""

        def getAddress():
            pattern = r"^.+[地址].{1}(.+[縣市].*)"
            group = search(pattern, dt)
            return group[0].strip() if len(group) > 0 else ""

        def getPhone():
            pattern = r"^.+[電話|].{1}(0[^9].*)"
            group = search(pattern, dt)
            return group[0].strip() if len(group) > 0 else ""

        def getmPhone():
            pattern = r"^.+[電話|手機].{1}(09.*)"
            group = search(pattern, dt)
            return group[0].strip() if len(group) > 0 else ""

        dp = DataPack()
        dp.name = getName()
        dp.Phone = getPhone()
        dp.mPhone = getmPhone()
        dp.address = getAddress()
        return dp

class GoogleSpreadDataParser(ParserBase):
    interestColumn = ['收件人', '到貨日期', '指定到貨時段', '住址', '聯絡電話 (04-88xxxxxx)', '手機 (09xx-xxx-xxx)']
    def parse(self, dt) -> DataPack:
        def getName():
            return dt[1][0]

        def getAddress():
            return dt[1][3]

        def getPhone():
            return dt[1][4]

        def getmPhone():
            return dt[1][5]

        def getShippingDate():
            import datetime
            shippingDate = datetime.datetime.strptime(dt[1][1], "%Y/%m/%d") - datetime.timedelta(days=1)
            return shippingDate.strftime("%Y/%m/%d")

        def getArrivalDate():
            return dt[1][1]

        dp = DataPack()
        dp.name = getName()
        dp.Phone = getPhone()
        dp.mPhone = getmPhone()
        dp.address = getAddress()
        dp.shippingDate = getShippingDate()
        dp.arrivalDate = getArrivalDate()
        return dp