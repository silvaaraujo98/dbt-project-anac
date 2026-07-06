
import json
import requests
import pandas as pd
import logging 
import timeit


class AnacExtractor():
    def __init__(self, year,month):
        self.file_path = f"https://sistemas.anac.gov.br/dadosabertos/Operador%20Aeroportu%C3%A1rio/Dados%20de%20Movimenta%C3%A7%C3%A3o%20Aeroportu%C3%A1rias/{year}/Movimentacoes_Aeroportuarias_{year}{month}.csv"

    def extract_data(self,nrows=None):
        df = pd.read_csv(
                self.file_path,
                skiprows = 1,
                delimiter = ";",
                nrows = nrows
                         
                         )
        return df

    
    