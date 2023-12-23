import sys
import subprocess
import psutil
import json
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

try:
    with open('Settings.json', 'r') as file:
        Settings = json.load(file)
        ElementInstalled = Settings['ElementInstalled']
except:
    ElementInstalled = False
    

if ElementInstalled == True:
    CommandModule = 'StartELM.exe'
else:
    CommandModule = 'StartELMINST.exe'

try:
    FlaskServer = subprocess.Popen([CommandModule], creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
except Exception as e:
    print(f"Ошибка запуска Flask-сервера: {e}")
    sys.exit(1)

def get_children(proc):
    children = []
    for child in proc.children(recursive=True):
        children.extend(get_children(child))
    return [proc] + children

class MainWindow (QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.NoCache)
        profile.defaultProfile().setHttpUserAgent('ElementClient')

        self.WebView = QWebEngineView()
        self.WebView.setUrl(QUrl('http://127.0.0.1:5023'))
        self.WebView.setZoomFactor(1.3)
        self.setCentralWidget(self.WebView)
        self.setWindowTitle('Element')
        self.showMaximized()

    def closeEvent(self, event):
        try:
            flask_server_procs = get_children(psutil.Process(FlaskServer.pid))
            for proc in flask_server_procs:
                try:
                    proc.kill()
                except Exception as e:
                    print(f"Ошибка завершения процесса: {e}")
            FlaskServer.terminate()
            FlaskServer.wait()
        except Exception as e:
            print(f"Ошибка завершения Flask-сервера: {e}")
        event.accept()

if __name__ == '__main__':
    App = QApplication(sys.argv)
    Window = MainWindow()
    Window.show()
    sys.exit(App.exec_())