import datetime
from datetime import datetime
import mysql
import mysql.connector


class Support_acomph:
    def __init__(self, data, valor):
        self._valor = valor
        self._data = datetime.strptime(data, '%Y-%m-%d').date()
        self.lista = [1100, 1600, 4000, 8000, 4000, 2000, 1200, 900, 750, 700, 800, 900]

    def get_mes(self):
        return self._data.month

    def get_valor(self):
        return self._valor

    def valor(self):
        if self.get_valor() <= self.lista[self.get_mes() - 1]:
            return 0
        elif self.get_valor() <= self.lista[self.get_mes() - 1] + 13900:
            return self.get_valor() - self.lista[self.get_mes() - 1]
        else:
            return 13900


if __name__ == '__main__':
    print(dir(mysql))
    #p = Support_acomph('2019-07-10', 723)
    #print(p.valor())
