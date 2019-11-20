import pandas as pd

import mysql.connector
import numpy as np
from datetime import date
from Postos import Support_acomph


bacias = ['Grande', 'Paranaíba', 'Tietê', 'Paranapanema', 'Paraná', 'Iguaçu', 'Uruguai', 'Jacui', 'Outras Sul',
          'Paraguai', 'Paraíba do Sul', 'Doce', 'Outras Sudeste', 'São Francisco', 'Outras Nordeste', 'Tocantins',
          'Amazonas', 'Araguari']


def op(str_string):
    a = open(str_string).readlines()
    for i in range(len(a)):
        a[i] = a[i].split()
        for j in range(len(a[i])):
            try:
                a[i][j] = int(a[i][j])
            except:
                pass
    return a


def dicionario(colunas, posicao):
    list_of_list = [bacias, colunas, posicao]
    d = {z[0]: list(z[1:]) for z in zip(*list_of_list)}
    return d


def mysql():
    a = op('mysql')
    for i in range(len(a)):
        a[i] = a[i].replace('\n', '')
    return a


def excel_to_dataframe(dict_geral, str_string):  # (Dicionario de bacias, nome da bacia)
    df = pd.read_excel(r'C:\Users\Lucas\Downloads\ACOMPH_06.11.2019.xls', str_string, skiprows=4, nrows=30,
                       head=None, usecols=(dict_geral[str_string][0]), names=dict_geral[str_string][1])

    df_arrumado = fix_dataframe(df, str_string)
    return df_arrumado


def fix_dataframe(dataframe, bacia):
    if bacia == 'Grande':
        dataframe[2] = dataframe[1]

    elif bacia == 'Tietê':
        dataframe[104] = dataframe[117] + dataframe[118]
        dataframe[109] = dataframe[118]
        dataframe[119] = (dataframe[118] - 0.2) / 0.81
        dataframe[160] = dataframe[161] * (320 / (4844 - 681 - 700))
        #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
        #   #   #   #   #   #   #   #   #   #   #   # ALTO - TIETE  #   #   #   #   #   #   #   #   #   #   #   #   #
        #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
        dataframe[301] = dataframe[118]
        dataframe[320] = dataframe[119]
        dataframe[116] = dataframe[118] - dataframe[119]

    elif bacia == 'São Francisco':
        dataframe[175] = dataframe[173]
        dataframe[176] = dataframe[173]

    elif bacia == 'Amazonas':
        aux = [314.0069143, 203.2740257, 366.6547014, 405.833171, 319.3609519, 203.9993751, 185.8195767, 184.6476084,
               173.3591056, 190.0128545, 264.9782052, 299.3082131]
        aux2 = [0.343337921, 0.362335438, 0.313470563, 0.279171077, 0.282620486, 0.35078518, 0.371938431, 0.375913107,
                0.392865675, 0.377560886, 0.339781702, 0.345798029]
        m = date.today().month

        dataframe[228] = aux[m - 1] + aux2[m - 1] * dataframe[229]
        # dataframe[203] = 1.009 * dataframe[229]

    elif bacia == 'Paraíba do Sul':
        aux = [-0.4, 0.4, -0.4, 0.3, 2, 0.5, 0.3, 0, -0.2, -0.1, 0, 0.1]
        aux2 = [1.478, 1.448, 1.481, 1.455, 1.285, 1.402, 1.418, 1.463, 1.493, 1.469, 1.461, 1.461]
        m = date.today().month
        dataframe[203] = aux[m - 1] + aux2[m - 1] * dataframe[201]

        aux3 = [2288, 315, 316, 304, 132, 131, 303, 306, 299, 127, 126]
        for i in aux3:
            dataframe = artificiais_paraiba(dataframe, i)

    elif bacia == 'Paraná':
        aux = pd.read_excel(r'C:\Users\Lucas\Downloads\ACOMPH_06.11.2019.xls', 'Tietê', skiprows=4,
                            nrows=30, head=None, usecols=[72], names=[73])
        dataframe[244] = aux[73] + dataframe[34]

    elif bacia == 'Paraguai':
        dataframe[252] = dataframe[259]

    return dataframe


def artificiais_paraiba(dataframe, posto):
    if posto == 2288:
        dataframe[2288] = 0
        for i in range(len(dataframe[125])):
            if dataframe[125].iloc[i] < 190:
                dataframe[2288].iloc[i] = dataframe[125].iloc[i] * 119 / 190
            elif dataframe[125].iloc[i] < 209:
                dataframe[2288].iloc[i] = 119
            elif dataframe[125].iloc[i] < 250:
                dataframe[2288].iloc[i] = dataframe[125].iloc[i] - 69
            else:
                dataframe[2288].iloc[i] = 160

    elif posto == 315:
        dataframe[315] = dataframe[203] - dataframe[201] + dataframe[2288] + maximo(dataframe[201] - 25, 0)

    elif posto == 316:
        dataframe[316] = minimo(dataframe[315], 190)

    elif posto == 304:
        dataframe[304] = dataframe[315] - dataframe[316]

    elif posto == 132:
        dataframe[132] = dataframe[202] + minimo(dataframe[201], 25)

    elif posto == 131:
        dataframe[131] = minimo(dataframe[316], 144)

    elif posto == 303:
        dataframe[303] = 0
        for i in range(len(dataframe[132])):
            if dataframe[132].iloc[i] < 17:
                dataframe[303].iloc[i] = dataframe[132].iloc[i] + minimo(dataframe[316] - dataframe[131], 34).iloc[i]
            else:
                dataframe[303].iloc[i] = 17 + minimo(dataframe[316] - dataframe[131], 34).iloc[i]

    elif posto == 306:
        dataframe[306] = dataframe[131] - dataframe[303]

    elif posto == 299:
        dataframe[299] = dataframe[130] - dataframe[2288] - dataframe[203] + dataframe[304]

    elif posto == 127:
        dataframe[127] = dataframe[129] - dataframe[2288] - dataframe[203] + dataframe[304]

    elif posto == 126:
        dataframe[126] = 0
        for i in range(len(dataframe[127])):
            if dataframe[127].iloc[i] <= 430:
                dataframe[126].iloc[i] = maximo(dataframe[127] - 90, 0).iloc[i]
            else:
                dataframe[126].iloc[i] = 340

    return dataframe


def outros(dataframe):
    aux1 = [dataframe[237], dataframe[238], dataframe[239], dataframe[240], dataframe[241], dataframe[242],
            dataframe[243], dataframe[244], dataframe[245], dataframe[246], dataframe[266]]
    aux2 = [37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 66]
    # [dataframe[161], dataframe[117], dataframe[118]]

    for i in range(len(aux2)):
        dataframe[aux2[i]] = aux1[i] - 0.1 * (dataframe[161] - dataframe[117] - dataframe[118]) - dataframe[117] - \
                             dataframe[118]

    dataframe[75] = dataframe[76] + minimo(dataframe[73] - 10, 173.5)
    dataframe[318] = dataframe[116] + dataframe[117] + dataframe[118] + 0.1 * (
            dataframe[161] - dataframe[117] - dataframe[118])

    dataframe[2460] = dataframe[2460] + dataframe[1540]
    dataframe = dataframe.drop(1540, axis=1)

    return dataframe


def correcao(dataframe):
    a = list(map(Support_acomph, pd.DataFrame(list(map(lambda x: str(x)[0:10], dataframe['data'])))[0], dataframe[288]))
    t = [i.valor() for i in a]
    return pd.DataFrame(t)[0]


def maximo(series, valor):
    aux = []
    for i in series:
        aux.append(max(i, valor))
    return pd.DataFrame(aux, dtype='float64')[0]


def minimo(series, valor):
    aux = []
    for i in series:
        aux.append(min(i, valor))
    return pd.DataFrame(aux, dtype='float64')[0]


def main():
    colunas = op('cols')
    posicao = op('pos')
    dict_geral = dicionario(colunas, posicao)
    lista = []
    for i in list(dict_geral.keys()):
        df = excel_to_dataframe(dict_geral, i)
        lista.append(df)
    teste = pd.concat(lista, axis=1)
    teste = outros(teste)
    cols = [168, 169, 171, 172, 173, 178, 175, 176]
    teste[cols] = teste[cols].applymap(np.float64)
    teste['correcao'] = correcao(teste)
    #a = 0
    #for i in teste.data:
    #    p = Support_acomph(str(i)[0:10], teste[288][a])
    #    print(p.valor())
    #    a += 1

    #print(teste.data)
    #print(teste[288])
    print(dir(mysql))
    #cnx = mysql.connector.connect(user='Lucas', password='Vodka123', host='127.0.0.1', database='urca')
    #teste.to_sql(con=cnx, name='urca.vazao', if_exists='replace')

    list(map(print, teste.columns))


if __name__ == '__main__':
    #main()
    print(dir(mysql))
