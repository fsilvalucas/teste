import pandas as pd
import datetime
from datetime import date, timedelta
import zipfile
import pymysql
import pymysql.cursors
from sqlalchemy import create_engine


class produtibilidade:
    def __init__(self):
        self._data = date.today() - timedelta(days=0)
        self._path = 'C:\\Users\\Lucas\\Downloads'
        self._path2 = '\\Consistido_201911_PMO'
        self._path3 = r'C:\Users\Lucas\Downloads\Consistido_201911_PMO (2)\Consistido'
        self._file = '\\Relatório_de_Previsão de Vazões_PMO_de_NOVEMBRO_2019-preliminar.xls'

    def descompacta(self):
        path = r'C:\Users\Lucas\Downloads' + '\\'
        file = zipfile.ZipFile(self._path + self._path2)
        file.extractall(self._path)
        file.close()
        print('extraido com sucesso')

    def prod(self):
        excel = pd.read_excel(self._path3 + self._file, 'Tab-24', skiprows=3, nrows=52, head=None, usecols=[0,2],
                              names=['posto', 'vazao'])
        excel2 = pd.read_excel(self._path3 + self._file, 'Tab-24', skiprows=3, nrows=51, head=None, usecols=[4,6],
                              names=['posto', 'vazao'])
        excel3 = pd.read_excel(self._path3 + self._file, 'Tab-24', skiprows=3, nrows=51, head=None, usecols=[8, 10],
                               names=['posto', 'vazao'])
        oi = pd.concat([excel,excel2, excel3], axis=0, ignore_index=True)
        return oi


if __name__ == '__main__':
    a = produtibilidade()
    b = a.prod()
    #lista=[118,119]
    #lista2=[0, 0]

    #a = (map(lambda x,y : b.append({'posto': x, 'vazao':str(y)}, ignore_index=True), lista, lista2))
    #print(a)
    #c = pd.DataFrame([])
    #[pd.concat(pd.DataFrame({'posto': str(x), 'vazao':y}), ignore_index=True) for x,y in zip(lista, lista2)]
    #print(c)
    ''' b = b.append({'posto': '118', 'vazao':0}, ignore_index=True)
    b = b.append({'posto': '117', 'vazao': 0}, ignore_index=True)
    b = b.append({'posto': '161', 'vazao': 0}, ignore_index=True)
    b = b.append({'posto': '237', 'vazao': 0}, ignore_index=True)
    b = b.append({'posto': '238', 'vazao': 0}, ignore_index=True)
    b = b.append({'posto': '239', 'vazao': 0}, ignore_index=True)
    b = b.append({'posto': '240', 'vazao': 0}, ignore_index=True)
    b = b.append({'posto': '242', 'vazao': 0}, ignore_index=True)
    b = b.append({'posto': '243', 'vazao': 0}, ignore_index=True)
    b = b.append({'posto': '104', 'vazao': 0}, ignore_index=True)
    b = b.append({'posto': '238', 'vazao': 0}, ignore_index=True)'''

    #try:
    #    var = b.loc[b['Nome'] == 'CAMARGOS']['Valor']
    #except:
    #    var = 0
    #print(float(var))
    #print(b)
    #connection = pymysql.connect(host='127.0.0.1', user='Lucas', password='Vodka123',db='urca',charset='utf8mb4',
    #                             cursorclass=pymysql.cursors.DictCursor)

    #engine = create_engine('mysql+pymysql://Lucas:Vodka123@127.0.0.1/urca')

    #b.to_sql(con=engine, name='produtibilidade', if_exists='replace', index=False)
