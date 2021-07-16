import pandas as pd
from pandas import DataFrame

dataTable = None

def addNewOrderData(dataPack):
    global dataTable
    if dataTable is None:
        dataTable = dataPack.createPdData()
    elif isinstance(dataTable, DataFrame):
        dataTable = dataTable.append(dataPack.createPdData())

def getOrderData():
    if isinstance(dataTable, DataFrame):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(dataTable.to_html(table_id="OrderTable", index=False), "html.parser")
        soup.find('table')['contenteditable'] = 'true'

        tableHeaders = soup.findAll('th')
        for th in tableHeaders:
            th['contenteditable'] = 'false'
        # soup.find('th')['contenteditable'] = 'false'
        return str(soup)
    return ""

class DataPack(object):
    TableIndex = 0
    DegreeLevel = "2"
    PackageSize = "3"
    Sender = "蔡麗琴"
    SendersPhone = ""
    SendersMobilePhone = "0953-813-100"
    SendersAddress = "彰化縣溪湖鎮彰水路二段460巷1號"
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

    def createPdData2(self):
        df2 = pd.DataFrame({"A": 1.0,
                            "B": pd.Timestamp("20130102"),
                            "C": pd.Series(1, index=list(range(4)), dtype="float32"),
                            "E": pd.Categorical(["test", "train", "test", "train"]),
                            "F": "foo"
                            }
         )
        df3 = pd.DataFrame({"A": 2.0,
                            "B": pd.Timestamp("20130102"),
                            "C": pd.Series(1, index=list(range(4)), dtype="float32"),
                            "E": pd.Categorical(["test", "train", "test", "train"]),
                            "F": "foo2"
                            }
         )
        d4 = df2.append(df3)
        print(d4.head())

import re
def TryParse(dt) -> DataPack:

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


if __name__ == '__main__':
    dt = """收件者姓名：周宜昌
聯繫電話：03-8561002
配送地址：花蓮市國福里福光街347巷56號
    """
    dt2 = """收件者姓名：周宜昌2
    聯繫電話：03-8561002
    配送地址：花蓮市國福里福光街347巷56號
        """
    data1 = TryParse(dt).createPdData()
    allData = data1.append(TryParse(dt2).createPdData())
    print(allData.head())
    # app.run()


