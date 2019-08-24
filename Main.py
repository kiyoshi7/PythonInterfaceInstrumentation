# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 20:37:39 2019

@author: Daniel
"""

import multiprocessing 
from time import sleep
from operator import methodcaller

from SerialConnection import SerialConnection as SC

class Spawn:
    def __init__(self, _number, _max):
        self._number = _number
        self._max = _max
        # Don't call update here

    def request(self, x):
        print("{} was requested.".format(x))

    def update(self):
        while True:
            print("Spawned {} of {}".format(self._number, self._max))
            sleep(2)

if __name__ == '__main__':
    '''
    spawn = Spawn(1, 1)  # Create the object as normal
    p = multiprocessing.Process(target=methodcaller("update"), args=(spawn,)) # Run the loop in the process
    p.start()
    while True:
        sleep(1.5)
        spawn.request(2)  # Now you can reference the "spawn"
    '''
    device = SC()
    p = multiprocessing.Process(target=methodcaller("ReadData"), args=(device,)) # Run the loop in the process
    p.start()
    while True:
        sleep(1.5)
        device.SendData('0003')
    
    

