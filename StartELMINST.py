import os
import json
import requests
import hashlib
import zipfile
from flask import Flask, render_template, request, jsonify

def CreateSHA256 (FilePath):
    with open(FilePath, 'rb') as f:
        Hash = hashlib.sha256()
        for byte_block in iter(lambda: f.read(4096), b""):
            Hash.update(byte_block)
    return Hash.hexdigest()

def UpdateSettings():
    Settings = {
        'ElementInstalled': True
    }
    with open('Settings.json', 'w') as file:
        json.dump(Settings, file)

def ClearTemp():
    Files = os.listdir('Temp')
    for File in Files:
        FileURL = os.path.join('Temp', File)
        if os.path.isfile(FileURL):
            os.remove(FileURL)


CurrentDirectory = os.getcwd()
app = Flask(__name__, template_folder=os.path.join(CurrentDirectory, 'EAppCore'), static_url_path='', static_folder=os.path.join(CurrentDirectory, 'EAppCore'))

@app.route('/')
def Home():
    return render_template('index.html')

@app.route('/AutoInstal', methods=['GET'])
def AutoInstal():
    TempPath = os.path.join('Temp', 'RESOURCES')
    response = requests.get('https://elm.lol/Download/RESOURCES')
    with open(TempPath, 'wb') as file:
        file.write(response.content)
    with zipfile.ZipFile(TempPath, 'r') as zip_ref:
        zip_ref.extractall('ElementRes')
    UpdateSettings()
    ClearTemp()
    response = { 'Title':'Инфо', 'Info':'Отлично, Элемент установлен, теперь перезайдите в приложение и войдите в аккаунт'}
    return jsonify(response)

@app.route('/UploadFile', methods=['POST'])
def UploadFile():

    File = request.files['File']
    FileName = File.filename
    TempPath = os.path.join('Temp', FileName)
    File.save(TempPath)

    with open(TempPath, 'rb') as f:
        Hash = CreateSHA256(TempPath)
        print(Hash)
        ApiURL = 'https://elm.lol/System/API/VerifyFileSignature.php'
        Data = {'Hash': Hash}
        Headers = {
            'User-Agent': 'ElementClient',
        }
        try:
            Request = requests.post(ApiURL, data=Data, headers=Headers)
            try:
                Answer = Request.json()
            except:
                Answer = None
        except requests.exceptions.RequestException as e:
            Request = None
            Answer = None

        if Answer:
            if Answer['Content'] == 'Signed':
                with zipfile.ZipFile(TempPath, 'r') as zip_ref:
                    zip_ref.extractall('ElementRes')
                UpdateSettings()
                ClearTemp()
                response = { 'Title':'Инфо', 'Info':'Отлично, Элемент установлен, теперь перезайдите в приложение и войдите в аккаунт'}
                return jsonify(response)
            else:
                response = { 'Title':'Осторожно', 'Info':'Этот файл не подписан, устанавливая эти ресурсы вы принимаете все возможные риски, включая взлом аккаунта. Устанавливайте только подписанные ресурсы или с же надёжных источников.'}
                return jsonify(response)
        else:
            response = { 'Title':'Ошибка', 'Info':'Не удалось проверить файл.'}
            return jsonify(response)
        
@app.route('/ConfirmUpload', methods=['POST'])
def ConfirmUpload():
    json = request.json
    FileName = json.get('FileName')
    TempPath = os.path.join('Temp', FileName)
    with zipfile.ZipFile(TempPath, 'r') as zip_ref:
        zip_ref.extractall('ElementRes')
    UpdateSettings()
    ClearTemp()
    response = { 'Title':'Инфо', 'Info':'Отлично, Элемент установлен, теперь перезайдите в приложение и войдите в аккаунт'}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5023, debug=True, threaded=True)