import mysql
import mysql.connector
import pandas as pd
import datetime
from datetime import datetime
import os


class Connection:
    def __init__(self):
        self.__con = mysql.connector.connect(user='Lucas', password='Vodka123', host='127.0.0.1', database='bbce2')
        self.path = r'C:\Users\Lucas\Downloads\bbce_contratos.xlsx'
        self.sql = ("INSERT INTO book "
                    "( numero, Produto, cancelado, tipo, data_hora, MWm, MWh, preco, contraparte, cnpj, operador, "
                    "solicitado, aprovado) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

    def get_file(self):
        return self.path

    def get_sql(self):
        return self.sql

    def get_cursor(self):
        return self.__con.cursor()

    def read(self):
        file = self.get_file()
        excel = pd.read_excel(file)
        excel.rename(columns={'Número': 'numero', 'Produto': 'Produto', 'Status': 'cancelado', 'Tipo': 'tipo',
                              'Data / Hora': 'data_hora', 'MWm': 'MWm', 'MWh': 'MWh', 'R$/MWh': 'preco',
                              'Contraparte': 'contraparte', 'CNPJ': 'cnpj', 'Operador': 'operador',
                              'Cancelamento Solicitado Por': 'solicitado', 'Cancelamento Aprovado Por': 'aprovado'},
                     inplace=True)
        excel.fillna('', inplace=True)
        excel.drop('Preço Referência', axis=1, inplace=True)
        os.remove(file)

        return excel

    def parse_datetime(self, excel):
        for i in range(len(excel.data_hora)):
            ano = int(excel.data_hora[i][6:10])
            mes = int(excel.data_hora[i][3:5])
            dia = int(excel.data_hora[i][0:2])
            hora = int(excel.data_hora[i][11:13])
            minuto = int(excel.data_hora[i][14:16])
            segundo = int(excel.data_hora[i][17:19])
            excel.data_hora[i] = datetime(ano, mes, dia, hora, minuto, segundo)

        return excel

    def parse_float(self, excel):
        dict_teste = {}
        for i in range(len(excel.index)):
            dict_teste[i] = excel.loc[i, :]

        for i in range(len(dict_teste)):
            dict_teste[i] = list(dict_teste[i])

        for i in range(len(dict_teste)):
            dict_teste[i][5] = float(dict_teste[i][5])
            dict_teste[i][6] = float(dict_teste[i][6])
            dict_teste[i][7] = float(dict_teste[i][7])

        return dict_teste

    def insert_into(self, dict_excel):
        sql = self.get_sql()
        cursor = self.get_cursor()
        for i in range(len(dict_excel)):
            cursor.execute(sql, dict_excel[i])
        self.commit_mysql(cursor)

    def commit_mysql(self, cursor):
        self.__con.commit()
        cursor.close()
        self.__con.close()


def main():
    cnx = Connection()
    excel = cnx.read()
    excel = cnx.parse_datetime(excel)
    dicionario = cnx.parse_float(excel)
    cnx.insert_into(dicionario)


if __name__ == '__main__':
    main()
