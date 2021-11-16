from flask import Flask
import os

#Programa principal
app = Flask(__name__)

#Funcoes de comunicacao com a central
@app.route('/<int:total_repeticoes>')
def recebe_serie(total_repeticoes):
    #Mata o codigo principal
    pid=os.system("ps -ef | grep wait -m 1 | cut -d ' ' -f 6")
    if pid=="":
        os.system("kill "+pid)
    else:
        os.system("kill $(ps -ef | grep wait -m 1 | cut -d ' ' -f 7)")
    #Inicia a serie
    os.system("brickrun -r -- pybricks-micropython series_counter.py "+str(total_repeticoes)+" &")
    return "ok"
