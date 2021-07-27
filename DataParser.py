from DataPack import DataPack
import math


class ParserBase():
    def __init__(self):
        self.dt = None

    def setData(self, dt):
        self.dt = dt

    def getName(self):
        raise NotImplementedError

    def getAddress(self):
        raise NotImplementedError

    def getPhone(self):
        raise NotImplementedError

    def getmPhone(self):
        raise NotImplementedError

    def getShippingDate(self):
        raise NotImplementedError

    def getArrivalDate(self):
        raise NotImplementedError

    def getNumbersOfPack(self):
        raise NotImplementedError

    def getNumbers(self):
        raise NotImplementedError

    def getPaymentMethod(self):
        raise NotImplementedError

    def getUserComment(self):
        return ""

    def parse(self) -> DataPack:
        dp = DataPack()
        dp.name = self.getName()
        dp.phone = self.getPhone()
        dp.mPhone = self.getmPhone()
        dp.address = self.getAddress()
        dp.shippingDate = self.getShippingDate()
        dp.arrivalDate = self.getArrivalDate()
        dp.numbersOfPack = self.getNumbersOfPack()
        dp.numbers = self.getNumbers()
        dp.userComment = self.getUserComment()
        return dp

import re
class ReDataParser(ParserBase):
    def search(self, pattern, dt):
        result = re.search(pattern, dt, re.MULTILINE)
        if result is not None:
            return result.groups()
        return []

    def getName(self):
        pattern = r"^.+[姓名|收件人].{1}(.*)"
        group = self.search(pattern, self.dt)
        return group[0].strip() if len(group) > 0 else ""

    def getAddress(self):
        pattern = r"^.+[地址].{1}(.+[縣市].*)"
        group = self.search(pattern, self.dt)
        return group[0].strip() if len(group) > 0 else ""

    def getPhone(self):
        pattern = r"^.+[電話|].{1}(0[^9].*)"
        group = self.search(pattern, self.dt)
        return group[0].strip() if len(group) > 0 else ""

    def getmPhone(self):
        pattern = r"^.+[電話|手機].{1}(09.*)"
        group = self.search(pattern, self.dt)
        return group[0].strip() if len(group) > 0 else ""

    def getShippingDate(self):
        return ""

    def getArrivalDate(self):
        return ""

    def getNumbersOfPack(self):
        return "1"  # TODO

    def getNumbers(self):
        return "4"  # TODO

    def getPaymentMethod(self):
        return "remittance"  # TODO

    def getUserComment(self):
        return "" # TODO

class GoogleSpreadDataParser(ParserBase):
    interestColumn = ['收件人', '到貨日期', '指定到貨時段', '住址', '聯絡電話 (04-88xxxxxx)', '手機 (09xx-xxx-xxx)', '數量']
    def getName(self):
        return self.dt[1][0]

    def getAddress(self):
        return self.dt[1][3]

    def getPhone(self):
        return self.dt[1][4]

    def getmPhone(self):
        return self.dt[1][5]

    def getShippingDate(self):
        import datetime
        shippingDate = datetime.datetime.strptime(self.dt[1][1], "%Y/%m/%d") - datetime.timedelta(days=1)
        return shippingDate.strftime("%Y/%m/%d")

    def getArrivalDate(self):
        return self.dt[1][1]

    def getNumbersOfPack(self):
        return '{}'.format(math.ceil(float(self.dt[1][6].split('箱')[0])/4.0))

    def getNumbers(self):
        return '{}'.format(self.dt[1][6].split('箱')[0])

    def getPaymentMethod(self):
        return "remittance"  # TODO

    def getUserComment(self):
        return ""  # TODO