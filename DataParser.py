from DataPack import DataPack, PAYMENTMETHOD_TRANSFER, PAYMENTMETHOD_PAY_ON_DELIVERY, ARRIVALTIME_MORNING, \
    ARRIVALTIME_AFTERNOON, ARRIVALTIME_NOT_SPECIFIED
import math
import datetime

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

    def getArrivalTime(self):
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
        dp.arrivalTime = self.getArrivalTime()
        dp.numbersOfPack = self.getNumbersOfPack()
        dp.numbers = self.getNumbers()
        dp.userComment = self.getUserComment()
        dp.paymentMethod = self.getPaymentMethod()
        return dp

import re
class ReDataParser(ParserBase):
    def removeWords(self, text, removechars):
        for ch in removechars:
            if ch in text:
                text = text.replace(ch, '')
        return text.strip()

    def search(self, pattern, dt):
        result = re.search(pattern, dt, re.MULTILINE)
        if result is not None:
            return result.groups()
        return []

    def getName(self):
        pattern = r"^.+[姓名|收件人].{1}(.*)"
        group = self.search(pattern, self.dt)
        name = group[0].strip() if len(group) > 0 else ""

        if name == "" or len(name) > 10:
            for line in self.dt.split("\n"):
                # assume the length of name is less within 2-4
                if 4 >= len(line) > 1:
                    name = line
                    break

        return name

    def getAddress(self):
        pattern = r"^.+[地址].{1}(.+[縣市].*)"
        group = self.search(pattern, self.dt)
        address = group[0].strip() if len(group) > 0 else ""

        if address == "" or len(address) < 9:
            for line in self.dt.split("\n"):
                # assume the length of name is less within 2-4
                if len(line) > 9 and (str(line).find("縣") != -1 or str(line).find("市") != -1):
                    address = line
                    break
        return address

    def getPhone(self):
        pattern = r"^.+[電話|].{1}(0[^9].*)"
        group = self.search(pattern, self.dt)
        if len(group) > 0:
            candidate = group[0]
            candidate2 = self.removeWords(candidate, ['-', '(', ')', '－'])
            if len(candidate2) >= 9:
                return '{}-{}'.format(candidate2[:2], candidate2[2:])
        return group[0].strip() if len(group) > 0 else ""

    def getmPhone(self):
        pattern = r"^.+[電話|手機].{1}(09.*)"
        group = self.search(pattern, self.dt)
        mPhone = ""
        if len(group) > 0:
            candidate = group[0]
            candidate2 = self.removeWords(candidate, ['-', '(', ')', '－'])
            if len(candidate2) == 10:
                mPhone = '{}-{}-{}'.format(candidate2[:4], candidate2[4:7], candidate2[7:])
            else:
                mPhone = group[0].strip() if len(group) > 0 else ""

        if (mPhone == ""):
            pattern = r".*(09.*)"
            group = self.search(pattern, self.dt)
            if len(group) > 0:
                candidate = group[0]
                candidate2 = self.removeWords(candidate, ['-', '(', ')', '－'])
                if len(candidate2) == 10:
                    mPhone = '{}-{}-{}'.format(candidate2[:4], candidate2[4:7], candidate2[7:])
                else:
                    mPhone = group[0].strip() if len(group) > 0 else ""
        return mPhone

    def getShippingDate(self):
        return ""

    def getArrivalDate(self):
        pattern = r"到貨日期.*(\d+)\/(\d+)"
        group = self.search(pattern, self.dt)
        if len(group) == 2:
            now = datetime.datetime.now()
            dt = datetime.datetime.strptime("{}/{}/{}".format(now.year, group[0], group[1]),
                                       "%Y/%m/%d")
            return dt.strftime("%Y/%m/%d")
        return ""

    def getNumbersOfPack(self):
        return '{}'.format(math.ceil(float(self.getNumbers())/4.0))

    def getNumbers(self):
        pattern = r"(\d+).*[箱盒]"
        group = self.search(pattern, self.dt)
        if len(group) > 0:
            candidate2 = self.removeWords(group[0], ['箱', '盒', '(', ')', '－'])
            numbers = int(candidate2)
            return numbers
        return 0

    def getPaymentMethod(self):
        pattern = r".*(貨到付款).*"
        group = self.search(pattern, self.dt)
        return PAYMENTMETHOD_PAY_ON_DELIVERY if len(group) > 0 else PAYMENTMETHOD_TRANSFER

    def getUserComment(self):
        return ""  # TODO

    def getArrivalTime(self):
        pattern = r".*(下午).*"
        group = self.search(pattern, self.dt)
        return ARRIVALTIME_AFTERNOON if len(group) > 0 else ARRIVALTIME_MORNING

class GoogleSpreadDataParser(ParserBase):
    interestColumn = ['收件人', '到貨日期', '指定到貨時段', '住址', '聯絡電話 (04-88xxxxxx)', '手機 (09xx-xxx-xxx)', '數量', "付款方式", "備註"]
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

    def getArrivalTime(self):
        if self.dt[1][2] == "下午":
            return ARRIVALTIME_AFTERNOON
        return ARRIVALTIME_MORNING

    def getNumbersOfPack(self):
        return '{}'.format(math.ceil(float(self.dt[1][6].split('箱')[0])/4.0))

    def getNumbers(self):
        return '{}'.format(self.dt[1][6].split('箱')[0])

    def getPaymentMethod(self):
        if str(self.dt[1][7]).find("貨到付款") != -1:
            return PAYMENTMETHOD_PAY_ON_DELIVERY
        return PAYMENTMETHOD_TRANSFER

    def getUserComment(self):
        if self.dt[1][8]:
            return self.dt[1][8]
        return ""

class HtmlFormDataParser(ParserBase):
    def getName(self):
        return self.dt['name-input']

    def getAddress(self):
        return self.dt['address-input']

    def getPhone(self):
        return self.dt['phone-input']

    def getmPhone(self):
        return self.dt['mPhone-input']

    def getShippingDate(self):
        return self.dt['shippingDate-input']

    def getArrivalDate(self):
        return self.dt['arrivalDate-input']

    def getArrivalTime(self):
        if self.dt['arriveTime-input'] == "上午":
            return ARRIVALTIME_MORNING
        elif self.dt['arriveTime-input'] == "下午":
            return ARRIVALTIME_AFTERNOON
        else:  #不指定
            return ARRIVALTIME_NOT_SPECIFIED

    def getNumbersOfPack(self):
        return '{}'.format(math.ceil(float(self.dt['numbers-input'])/4.0))

    def getNumbers(self):
        return self.dt['numbers-input']

    def getPaymentMethod(self):
        if self.dt['PaymentMethod-input'] == "貨到付款":
            return PAYMENTMETHOD_PAY_ON_DELIVERY
        # if self.dt['PaymentMethod-input'] == "轉帳":
        return PAYMENTMETHOD_TRANSFER

    def getUserComment(self):
        return self.dt['userComment-input']
