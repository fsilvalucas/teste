import mysql
import mysql.connector
import pymysql
import pymysql.cursors
from datetime import datetime, timedelta, date
import pandas as pd
import numpy as np
from sqlalchemy import create_engine


class ena:
    def __init__(self):
        self.__conn = connection = pymysql.connect(host='127.0.0.1', user='Lucas', password='Vodka123', db='urca',
                                                   charset='utf8mb4',
                                                   cursorclass=pymysql.cursors.DictCursor)
        self._data = date.today() - timedelta(days=2)
        self._vazao = pd.read_sql('SELECT * FROM urca.vazao', self.__conn,
                                  coerce_float=True, params=None, index_col='data')
        self._prod = pd.read_sql('SELECT * FROM urca.produtibilidade', self.__conn, coerce_float=True, params=None)

    def get_vazao(self):
        return self._vazao

    def get_prod(self):
        return self._prod

    def insere(self, dataframe):
        dataframe = dataframe.transpose()

        # dataframe.set_index('data')
        dataframe.reset_index(inplace=True)
        dataframe = round(dataframe, 0)

        engine = create_engine('mysql+pymysql://Lucas:Vodka123@127.0.0.1/urca')
        dataframe.to_sql(con=engine, name='ena', if_exists='replace')


if __name__ == '__main__':
    p = ena()
    vazao = p.get_vazao()
    prod = p.get_prod()

    var = prod.loc[prod['posto'] == 1]['vazao']

    var = prod.loc[prod['posto'] == int('66')]['vazao']

    vazao['66'] = vazao['66'] * var.iloc()[0] - (vazao['44'] * var.iloc()[0] + vazao['61'] * var.iloc()[0])

    vazao['666'] = vazao['44'] * var.iloc()[0]

    vazao['6662'] = vazao['61'] * var.iloc()[0]

    for i in vazao.columns:
        try:
            if i == '66':
                pass
            else:
                var = prod.loc[prod['posto'] == int(i)]['vazao']
                vazao[i] = vazao[i] * var.iloc()[0]

        except Exception as e:
            if i == 'data':
                pass
            elif i == 'correcao':
                var = 1
                vazao[i] = vazao[i] * var
            elif i == '666' or i == '6662':
                pass
            else:

                var = 0
                vazao[i] = vazao[i] * var
    p.insere(vazao)
