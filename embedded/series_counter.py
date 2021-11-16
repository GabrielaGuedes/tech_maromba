from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor)
from pybricks.parameters import Port

import time
import os
import sys
import multiprocessing
from constants import *

ev3 = EV3Brick()
motor=Motor(Port.A)
panico=TouchSensor(Port.S2)
lumin=ColorSensor(Port.S1)

def monitor_panico(serie_pid):
    global ev3
    global motor
    global panico
    global lumin
    global TEMPO_LONGO
    global TEMPO_CURTO
    global O01DESISTIU
    global LIMITE_LUMINOSIDADE
    global SCREEN_WIDTH

    while not panico.pressed():
        time.sleep(TEMPO_CURTO)

    #ev3.speaker.play_file(O01DESISTIU)
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, "Ele nao aguenta o tranco!")
    while lumin.ambient()>=LIMITE_LUMINOSIDADE:
        ev3.screen.draw_text(0, 60, str(lumin.ambient()))
        time.sleep(TEMPO_LONGO)
    motor.run_angle(360, -370)
    #Reinicia o processo principal
    os.system("brickrun -r -- pybricks-micropython wait.py &")
    os.system("kill "+str(serie_pid))

#Pega total_repeticoes dos argumentos
total_repeticoes=int(sys.argv[1])

#Inicia monitor do botao de panico
pid=os.getpid()
monitor=multiprocessing.Process(target=monitor_panico, args=(pid,))
monitor.start()
monitor_pid=monitor.pid
#Destrava pesos
motor.run_angle(360, 360)

#Conta repeticoes
while total_repeticoes>0:
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, "Repeticoes")
    ev3.screen.draw_text(0, 20, "faltantes:")
    ev3.screen.draw_text(0, 40, str(total_repeticoes))
    ev3.screen.draw_text(0, 60, str(lumin.ambient()))
    while lumin.ambient()<LIMITE_LUMINOSIDADE:
        time.sleep(TEMPO_LONGO)
    while lumin.ambient()>=LIMITE_LUMINOSIDADE:
        time.sleep(TEMPO_LONGO)
    total_repeticoes-=1

#Termina serie
ev3.screen.clear()
ev3.screen.draw_text(0, SCREEN_WIDTH//2, "Sua serie terminou, solte os pesos!")
while lumin.ambient()>=LIMITE_LUMINOSIDADE:
    time.sleep(TEMPO_LONGO)
motor.run_angle(360, -370)

#Mata processo do monitor
os.system("kill "+str(monitor_pid))
#Reinicia o processo principal
os.system("brickrun -r -- pybricks-micropython wait.py &")
