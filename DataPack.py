import pandas as pd

import GlobalSettings
import datetime
ARRIVALTIME_MORNING = "1"
ARRIVALTIME_AFTERNOON = "2"
ARRIVALTIME_NOT_SPECIFIED = "4"
PAYMENTMETHOD_TRANSFER = "1"
PAYMENTMETHOD_PAY_ON_DELIVERY = "2"

class DataPack(object):
    TableIndex = 0
    DegreeLevel = "2"# 1:常溫 2:冷藏 3:冷凍
    PackageSize = "3"
    Sender = GlobalSettings.Sender
    SendersPhone = ""
    SendersMobilePhone = GlobalSettings.SendersMobilePhone
    SendersAddress = GlobalSettings.SendersAddress
    Values = ""
    itemDescript = ""
    isPrint = "Y"
    isDonate = "N"
    GUINumbers = ""
    PortableDevice = ""
    SalePrice = GlobalSettings.SalePrice

    def __init__(self):
        self.name = None
        self.address = None
        self.mPhone = None
        self.phone = None
        self.shippingDate = ""
        self.arrivalDate = ""
        self.arrivalTime = ARRIVALTIME_MORNING  # 1:上午, 2:下午
        self.numbersOfPack = "0"
        self.numbers = '0'  # TODO: adjust value according to numbersOfPack
        self.paymentMethod = PAYMENTMETHOD_TRANSFER  # 轉帳 1 / 貨到付款 2
        self.userComment = ''
        self.googleComment = ''

    @property
    def arrivalTimeFormat(self):
        if self.arrivalTime == ARRIVALTIME_MORNING:
            return "上午"
        elif self.arrivalTime == ARRIVALTIME_AFTERNOON:
            return "下午"
        else:#self.arrivalTime == "4:
            return "不指定"

    @property
    def paymentMethodFormat(self):
        if self.paymentMethod == PAYMENTMETHOD_TRANSFER:
            return "轉帳"
        elif self.paymentMethod == PAYMENTMETHOD_PAY_ON_DELIVERY:
            return "貨到付款"
    @property
    def payOnDeliveryPrice(self):
        if self.paymentMethod == PAYMENTMETHOD_PAY_ON_DELIVERY:
            return int(self.numbers) * int(DataPack.SalePrice) + 30
        return ""

    def formatString(self):
        return "{name}  {Phone} {mPhone}    {address}".format(
            name=self.name,
            address=self.address,
            mPhone=self.mPhone,
            Phone=self.phone)

    def createPdData(self):
        DataPack.TableIndex += 1
        return pd.DataFrame({
                            "收件人姓名": self.name,
                            "收件人電話": self.phone,
                            "收件人手機": self.mPhone,
                            "收件人地址": self.address,
                            "代收金額或到付": self.payOnDeliveryPrice,
                            "件數": self.numbersOfPack,
                            "品名(詳參數表)": "4",
                            "備註": self.userComment,
                            "訂單編號": "",
                            "希望配達時間((詳參數表))": self.arrivalTime,
                            "出貨日期(YYYY / MM / DD)": self.shippingDate,
                            "預定配達日期(YYYY / MM / DD)": self.arrivalDate,
                            "溫層((詳參數表))": DataPack.DegreeLevel,
                            "尺寸((詳參數表))": DataPack.PackageSize,
                            "寄件人姓名": DataPack.Sender,
                            "寄件人電話": DataPack.SendersPhone,
                            "寄件人手機": DataPack.SendersMobilePhone,
                            "寄件人地址": DataPack.SendersAddress,
                            "保值金額(20001~10萬之間)": DataPack.Values,
                            "品名說明": DataPack.itemDescript,
                            "是否列印": DataPack.isPrint,
                            "是否捐贈": DataPack.isDonate,
                            "統一編號": DataPack.GUINumbers,
                            "手機載具": DataPack.PortableDevice}, index=[DataPack.TableIndex])

    def toDict(self):
        return {
            "name": self.name,
            "phone": self.phone,
            "mPhone": self.mPhone,
            "address": self.address,
            "shippingDate": self.shippingDate,
            "arrivalDate": self.arrivalDate,
            "numbersOfPack": self.numbersOfPack,
            "numbers": self.numbers,
            "userComment": self.userComment,
            "paymentMethod": self.paymentMethod,
            "arrivalTime": self.arrivalTime
        }

    def toGoogleSpreadSheetFormat(self):
        # 收件人
        # 到貨日期
        # 指定到貨時段
        # 住址
        # 聯絡電話(04 - 88
        # xxxxxx)    手機(0
        # 9
        # xx - xxx - xxx)    數量
        # 付款方式
        # 其他需求
        # 備註
        # 數量分析
        # 出貨日期
        # 套袋
        return [[datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                 self.name,
                 self.arrivalDate,
                 self.arrivalTimeFormat,
                 self.address,
                 self.phone,
                 self.mPhone,
                 self.numbers,
                 self.paymentMethodFormat,
                 self.googleComment,
                 self.userComment,
                 self.numbers,
                 self.shippingDate,
                 ]]
