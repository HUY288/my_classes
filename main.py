from flask import Flask, render_template
from os import listdir, path
import json
import re

app = Flask(__name__)

base_dir = "charecters"
files=listdir(base_dir)

class Person:
    def __init__(self, char_id, name,  species, gender, status, image):
        self.char_id = char_id
        self.name = name
        self.species = species
        self.gender = gender
        self.status = status
        self.image = image
    @classmethod
    def from_json(cls, json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
            char_id = json_path.split('\\')[-1].removesuffix('.json')
        return cls(char_id, data["name"], data["species"], data["gender"], data["status"], data["image"])
    
    def __repr__(self) :
        return [self.name, self.status]

# Укажите путь к папке с JSON-файлами
folder_path = f'{base_dir}'
# Инициализируем пустой список для хранения данных
combined_data = []
# Функция для извлечения числовой части из имени файла
def extract_number(filename):
    return int(re.search(r'(\d+)', filename).group())
# Сортировка списка
sorted_files = sorted(listdir(folder_path), key=extract_number)
# Вывод отсортированного списка
for filename in sorted_files:
    if filename.endswith('.json'):  # Проверяем, что файл имеет расширение .json
        file_path = path.join(folder_path, filename)
        combined_data.append(Person.from_json(file_path))


# Устанавливаем глобальную переменную в конфигурации
app.config['GLOBAL_VARIABLE'] = combined_data

# @app.route('/')
# def index():
#     a = (',').join([person.name for person in app.config['GLOBAL_VARIABLE']])
#     return a

@app.route('/')
def index():
    my_list = app.config['GLOBAL_VARIABLE']
    return render_template('index.html', data=my_list)  # Просто соединяем элементы строкой

@app.route('/charecter/<int:char_id>')
def charecter(char_id):
    person=app.config['GLOBAL_VARIABLE'][char_id-1]
    return render_template('charecter.html',person=person)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()