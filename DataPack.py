import pandas as pd

import GlobalSettings

class DataPack(object):
    TableIndex = 0
    DegreeLevel = "2"
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

    def __init__(self):
        self.name = None
        self.address = None
        self.mPhone = None
        self.Phone = None
        self.shippingDate = ""
        self.arrivalDate = ""
        self.arrivalTime = "1"
        self.numbersOfPack = "1"

    def formatString(self):
        return "{name}  {Phone} {mPhone}    {address}".format(
            name=self.name,
            address=self.address,
            mPhone=self.mPhone,
            Phone=self.Phone)

    def createPdData(self):
        DataPack.TableIndex += 1
        return pd.DataFrame({
                            "收件人姓名": self.name,
                            "收件人電話": self.Phone,
                            "收件人手機": self.mPhone,
                            "收件人地址": self.address,
                            "代收金額或到付": "",
                            "件數": self.numbersOfPack,
                            "品名(詳參數表)": "6",
                            "備註": "",
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

