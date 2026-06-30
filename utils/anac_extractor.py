
import json
import requests

class AnacExtractor():
    def __init__(self, year,month):
        self.file_path = f"https://sistemas.anac.gov.br/dadosabertos/Operador%20Aeroportu%C3%A1rio/Dados%20de%20Movimenta%C3%A7%C3%A3o%20Aeroportu%C3%A1rias/{year}/Movimentacoes_Aeroportuarias_{year}{month}.csv"

    def extract_data(self):
        response = requests.get(self.file_path)
        if response.status_code == 200:
            linhas = response.text.splitlines()
            # Verifica se a primeira linha é o metadado "Atualizado em:" e a descarta
            if linhas[0].startswith('"Atualizado em:') or "Atualizado" in linhas[0]:
                print(f"Removendo linha de metadados: {linhas[0]}")
                linhas = linhas[1:]  # Mantém da segunda linha em diante
    
                # Junta as linhas limpas de volta em uma única string de texto
                
                clean_text = "\n".join(linhas)
            return clean_text
        
    
    