#!/usr/bin/python3

import os
from flask import Flask
app = Flask(__name__)

def create_app(test_config=None):
    #Applikation und Config wird erstellt
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev', DATABSE=os.path.join(app.instance_path, 'flaskr.sqlite'))
    #Secret Key sollte in Config überschrieben werden, Database wird im Instanzordner gespeichert
    if test_config is None:
        #Instanzconfig laden
        app.config.from_pyfile('config.py', silent=True)
    else:
        #testconfig laden, falls sie der funktion übergeben wurde
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Ich sage hier nur Hallo!'

    return app

@app.route('/') #der Pfad der Webseite (hier also das root Verzeichnis)
def hello_world():
    return 'Hello, World!'

@app.route('/test')
def test():
    return 'test uff!'

if __name__ == '__main__':
    app.run()
