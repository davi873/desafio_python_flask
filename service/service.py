from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
import csv
import json
import requests


url_app = "http://localhost:5000";#URL da aplicação

class Listen(FileSystemEventHandler):
    """ 
    Classe que monitara as alterações no diretório
    """
    def on_modified(self, event):
        try:
            path_file = event.src_path
            if(path_file[-3:] == 'csv'): #Verifica a extensão do arquivo
                data = {'content_csv':[]} #Dic para receber os dados do csv 
                with open(event.src_path, 'r') as new_file:
                    csv_file = csv.reader(new_file,  delimiter=';')
                    for row in csv_file:
                        data['content_csv'].append(row)
        except Exception as e:
            print("ERRO PARA LER O ARQUIVO")
            print(e)
        #Envia os dados para aplicação web
        sendData(data)

def sendData(data):
    """ 
    Envia os dados do csv para aplicação WEB

    @param data: Dic com os dados do csv
    @except: Em caso de erro uma mensagem é enviada
    """
    try:
        headers = {'Content-type': 'application/json'}
        response = requests.post(url_app +'/create_score', data= json.dumps(data), headers=headers)
        if response.status_code != 200:
            print(response['menssage'])
        print("Arquivo enviado")
    except Exception as e:
        print("Erro ao tentar comunicar com servidor")
        print(e)


#Executa a aplicação
if __name__ == "__main__":
    #cria e starta o evento que monitora a pasta dir
    event_listen = Listen()
    observer = Observer()
    observer.schedule(event_listen,  path="dir/", recursive=True)
    observer.start()

    #Garante que a aplicação não será encerrada
    try:
        print("Serviço Iniciado")
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()