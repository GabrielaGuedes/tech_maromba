#!/usr/bin/env pybricks-micropython

#Imports ev3
from pybricks.hubs import EV3Brick

#Imports genericos
import time
import os
from constants import *

#Objetos ev3
ev3 = EV3Brick()

while True:
    ev3.screen.load_image(LARRY_LAGOSTA)
    time.sleep(2)
    ev3.screen.load_image(TECH_MAROMBA)
    time.sleep(2)
