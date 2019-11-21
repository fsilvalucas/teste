import pandas as pd
import mysql
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from scipy.interpolate import make_interp_spline, BSpline
from datetime import datetime


class bbce_plots:
    def __init__(self, int_numero, str_lista):
        self._numero = int_numero
        self._cnx = mysql.connector.connect(user='Lucas', password='Vodka123', host='127.0.0.1', database='bbce2')
        self._lista = str_lista

    # lista de querys
    def quantos(self):
        nova_lista = []

        '''query = "SELECT * FROM bbce2.negociacoes WHERE Produto IN ("
        for i in range(self._numero):
            query += "'SE CON MEN " + self._lista[i] + "/19 - Preço Fixo'"
            if i < self._numero - 1:
                query += ","
        query += ")AND Cancelado = 'Não'"'''
        for i in range(self._numero):
            #if i == 1:
            #    nova_lista.append("SELECT * FROM bbce2.negociacoes WHERE Produto = 'SE CON TRI ABR/19 JUN/19 - Preço Fixo' and Cancelado = 'Não' and date(data_hora)<='2019-07-31'")
            #    nova_lista.append("SELECT * FROM bbce2.negociacoes WHERE Produto = 'SE CON MEN JUN/19 - Preço Fixo' and Cancelado = 'Não' and date(data_hora)<='2019-07-31'")
            if self._lista[i] == 'JAN' or self._lista[i] == 'FEV':
                nova_lista.append("SELECT * FROM bbce2.negociacoes where Produto = 'SE CON MEN " + self._lista[
                    i] + "/20 - Preço Fixo' and Cancelado = " \
                         "'Não' ")
            else:
                nova_lista.append("SELECT * FROM bbce2.negociacoes where Produto = 'SE CON MEN " + self._lista[
                    i] + "/19 - Preço Fixo' and Cancelado = " \
                         "'Não' ")

        return nova_lista

    # abre o dataframe
    def open_dataframe(self, lista):
        lista_dataframe = []
        for i in lista:
            df = pd.read_sql(i, self._cnx)
            lista_dataframe.append(df)
        self._cnx.close()

        return lista_dataframe

    # organiza em data, preço e volume
    def organiza_dataframe(self, lista_dataframe):
        novo_dataframe = []
        for i in lista_dataframe:
            data = i.data_hora
            preco = i.Preço
            volume = i.MWm
            novo = pd.concat([data, preco, volume], axis=1)
            novo_dataframe.append(novo)

        return novo_dataframe

    # retira o horario para trabalhar apenas com a data
    def parse_datetime_to_date(self, lista_dataframe):
        novo_lista_dataframe = []
        for i in lista_dataframe:  # i recebe dataframe para cada dataframe na lista
            for j in range(len(i.index)):  # j percorre o tamanho de elementos no dataframe
                i.data_hora[j] = i.data_hora[j].date()  # coluna data_hora do dataframe i na posição j
            novo_lista_dataframe.append(i)

        return novo_lista_dataframe

    # Pondera o preço em função do volume agrupado pela data
    def pondera(self, lista_dataframe):
        volume = []
        nova_lista_dataframe_ponderado = []
        for i in lista_dataframe:
            group = i.groupby('data_hora')
            preco_average = lambda g: np.average(g["Preço"], weights=g["MWm"])
            final = group.apply(preco_average)
            nova_lista_dataframe_ponderado.append(final)
        if len(lista_dataframe) == 1:
            for i in lista_dataframe:
                volume = i.groupby('data_hora')['MWm'].sum()
                print(volume)
            return nova_lista_dataframe_ponderado, volume
        else:
            return nova_lista_dataframe_ponderado

    def plotar_grafico(self, lista):
        legenda = []
        listcor = ['black', 'olive', 'blue', 'gray', 'goldenrod', 'brown']
        print(len(self._lista))
        for i in range(len(self._lista)):
            legenda.append(mpatches.Patch(color=listcor[i], label=self._lista[i]))
        # plt.legend(handles=legenda)
        plt.figure(figsize=(11, 8))
        plt.title('Preço Médio')
        plt.grid(True)
        plt.xlabel('Data')
        plt.ylabel('Preço')

        for i in range(len(lista)):
            plt.plot(lista[i], marker='o', markersize=3, color=listcor[i], linewidth=2)
        plt.legend(handles=legenda)
        plt.show()

    def plotar_grafico_com_volume(self, lista, volume):
        legenda = []
        listcor = ['black', 'olive', 'blue', 'gray', 'goldenrod', 'brown']
        for i in range(len(self._lista)):
            legenda.append(mpatches.Patch(color=listcor[i], label=self._lista[i]))
        legenda.append(mpatches.Patch(color=listcor[1], label='Volume'))

        fig, ax1 = plt.subplots()
        ax1.set_ylabel('Volume')
        plt.grid(True)
        ax1.bar(volume.index, volume, color=listcor[1])
        ax1.tick_params(axis='y', labelcolor=listcor[1])

        ax2 = ax1.twinx()
        ax2.plot(lista[0], marker='o', markersize=3, color=listcor[0], linewidth=2)

        # color = listcor[1]
        ax2.set_ylabel('Preço', color=listcor[0])
        # ax2.plot(volume, color=listcor[1])
        ax2.tick_params(axis='y', labelcolor=listcor[0])
        ax2.yaxis.tick_right()

        fig.tight_layout()
        plt.title('Preço Médio')
        plt.show()


def main():
    p = bbce_plots(3, ['NOV', 'DEZ', 'JAN'])
    print('instanciado')
    quantos = p.quantos()
    print('lista_1')
    df = p.open_dataframe(quantos)
    print('Dataframe aberto')
    df_organizado = p.organiza_dataframe(df)
    print('Dataframe organizado')
    df_2 = p.parse_datetime_to_date(df_organizado)
    print('datas arrumadas')
    if len(df_2) == 1:
        ponderado, volume = p.pondera(df_2)

        p.plotar_grafico_com_volume(ponderado, volume)
        print(volume)
    else:
        ponderado = p.pondera(df_2)
        p.plotar_grafico(ponderado)


if __name__ == '__main__':
    main()
