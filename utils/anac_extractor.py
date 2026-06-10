
import json

class AnacExtractor():
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_data(self):
        with open(self.file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return data