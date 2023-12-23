import os
import shutil
import json
from flask import Flask, render_template, request, jsonify

CurrentDirectory = os.getcwd()
app = Flask(__name__, template_folder=os.path.join(CurrentDirectory, 'ElementRes'),  static_url_path='', static_folder=os.path.join(CurrentDirectory, 'ElementRes'))

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/DeleteAppResource', methods=['GET'])
def DeleteAppResource():
    ElementRes = os.path.join('ElementRes')
    shutil.rmtree(ElementRes)
    Settings = {
        'ElementInstalled': False
    }
    with open('Settings.json', 'w') as file:
        json.dump(Settings, file)

    response = { 'Type':'Info', 'Content':'Отлично, Элемент удалён, теперь перезайдите в приложение'}
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5023, debug=True, threaded=True)