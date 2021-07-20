from pandas import DataFrame
dataTable = None

def clearOrderData():
    global dataTable
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
        return str(soup)
    return ""


if __name__ == '__main__':
    dt = """收件者姓名：周周周
聯繫電話：03-88123456
配送地址：花蓮市國福里3333333333
    """
    dt2 = """收件者姓名：宜宜宜2
    聯繫電話：03-8812345
    配送地址：花蓮市國福555555
        """
    data1 = TryParse(dt).createPdData()
    allData = data1.append(TryParse(dt2).createPdData())
    print(allData.head())
    # app.run()


