'''
avoid.py

Sample client for the Pioneer P3DX mobile robot that implements a
kind of heuristic, rule-based controller for collision avoidance.

Copyright (C) 2023 Javier de Lope

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import robotica
from multiprocessing import Process, Queue
import pygame as pg
import numpy as np

WIDTH: int = 10; INICIO: bool = True

def color_map(value):
    if value < 0.5:
        return pg.Color(255, round(value*(255-1)*2), 0)
    else:
        return pg.Color(round(255 - (value - 0.5)*(255-1)*2), 255, 0)
    """if value < 0.2: return pg.Color(255, 0, 0)
    elif value < 0.9: return pg.Color(255, 255, 0)
    elif value < 1.1: return pg.Color(0, 255, 0)
    else: return pg.Color(255, 0, 0)"""

class DebugDisplay:
    def __init__(self):
        self.state   = None
        self.queue   = Queue()
        self.process = Process(target = self.debug_thread, args = (self.queue, ))

        self.process.daemon = True
        self.process.start()

    def debug_thread(self, queue):
        pg.init()
        self.width = 300 
        self.height = 400
        self.screen = pg.display.set_mode([300, 500])
        pg.display.set_caption( "Robotica Sensor Display: Debug")
        self.font = pg.font.SysFont('Times New Roman', 22)
        
        keep_drawing = True
        while keep_drawing:
            self.screen.fill( (255, 255, 255)) # White Background

            for event in pg.event.get():
                if event.type == pg.QUIT: keep_drawing =  False            

            while not queue.empty(): self.state = queue.get()
            # self.state = [(0, 2, 0.5, 0, 1, 0, 0, 0,), (9, 0)]

            self.debug_draw()

            pg.display.flip()

    def debug_draw(self):
        if self.state is None: return 
        self.draw_sensors()
        self.draw_speed()

    def draw_sensors(self):
        
        readings = self.state[0]

        left = color_map(readings[0])        
        pg.draw.line(self.screen, left, (40, 250), (40, 125), width=WIDTH)

        left_text = self.font.render("{:2.2f}".format(readings[0]), True, (0, 0, 0))
        left_text = pg.transform.rotate(left_text, 90)
        left_rect = left_text.get_rect()
        left_rect.centerx = 25
        left_rect.centery = 190
        self.screen.blit(left_text, left_rect)

        left_top = color_map(readings[1])        
        pg.draw.line(self.screen, left_top, (40, 125), (100, 50), width=WIDTH)

        left_top_text = self.font.render("{:2.2f}".format(readings[1]), True, (0, 0, 0))
        left_top_text = pg.transform.rotate(left_top_text, 50)
        left_top_rect = left_top_text.get_rect()
        left_top_rect.centerx = 55
        left_top_rect.centery = 75
        self.screen.blit(left_top_text, left_top_rect)

        top_color = color_map(readings[2])        
        pg.draw.line(self.screen, top_color, (100, 50), (200, 50), width=WIDTH)
        top_text = self.font.render("{:2.2f}".format(readings[2]), True, (0, 0, 0))
        # top_text = pg.transform.rotate(left_text, 90)
        top_rect = top_text.get_rect()
        top_rect.centerx = 150
        top_rect.centery = 30
        self.screen.blit(top_text, top_rect)

        right_top_color = color_map(readings[3])        
        pg.draw.line(self.screen, right_top_color, (200, 50), (self.width - 40, 125), width=WIDTH)

        left_text = self.font.render("{:2.2f}".format(readings[3]), True, (0, 0, 0))
        left_text = pg.transform.rotate(left_text, - 50)
        lett_rect = left_text.get_rect()
        lett_rect.centerx = self.width - 55
        lett_rect.centery = 75
        self.screen.blit(left_text, lett_rect)

        right = color_map(readings[4])        
        pg.draw.line(self.screen, right, (self.width - 40, 250), (self.width - 40, 125), width=WIDTH)

        right_text = self.font.render("{:2.2f}".format(readings[4]), True, (0, 0, 0))
        right_text = pg.transform.rotate(right_text, - 90)
        right_rect = right_text.get_rect()
        right_rect.centerx = self.width - 25
        right_rect.centery = 190
        self.screen.blit(right_text, right_rect)
        
        behind_color = color_map(readings[5])        
        pg.draw.line(self.screen, behind_color, (100, 325), (200, 325), width=WIDTH)
        behind_text = self.font.render("{:2.2f}".format(readings[5]), True, (0, 0, 0))
        behind_rect = behind_text.get_rect()
        behind_rect.centerx = 150
        behind_rect.centery = 350
        self.screen.blit(behind_text, behind_rect)
        
        left_bot = color_map(readings[6])     # (40, 125), (100, 50)
        pg.draw.line(self.screen, left_bot, (40, 250), (100, 325), width=WIDTH)
        left_bot_text = self.font.render("{:2.2f}".format(readings[6]), True, (0, 0, 0))
        left_bot_text = pg.transform.rotate(left_bot_text, - 50)
        left_bop_rect = left_bot_text.get_rect()
        left_bop_rect.centerx = 60
        left_bop_rect.centery = 300
        self.screen.blit(left_bot_text, left_bop_rect)


    def draw_speed(self):
        speed = self.state[1]
        left_motor_text  = self.font.render("Left  Motor:", True, (0, 0, 0))
        right_motor_text = self.font.render("Right Motor:", True, (0, 0, 0))
        
        left_motor_rect = left_motor_text.get_rect()
        left_motor_rect.left = 50
        left_motor_rect.centery = 380
        right_motor_rect = right_motor_text.get_rect()
        right_motor_rect.left = 50
        right_motor_rect.centery = 410
        self.screen.blit(left_motor_text, left_motor_rect)
        self.screen.blit(right_motor_text, right_motor_rect)

        left_motor_text  = self.font.render("{:2.3f}".format(speed[0]), True, (0, 0, 0))
        right_motor_text = self.font.render("{:2.3f}".format(speed[1]), True, (0, 0, 0))
        
        left_motor_rect = left_motor_text.get_rect()
        left_motor_rect.left = 175
        left_motor_rect.centery = 380
        right_motor_rect = right_motor_text.get_rect()
        right_motor_rect.left = 175
        right_motor_rect.centery = 410
        self.screen.blit(left_motor_text, left_motor_rect)
        self.screen.blit(right_motor_text, right_motor_rect)
        
        status_text = self.font.render(str(speed[2]), True, (0, 0, 0))
        status_rect = status_text.get_rect()
        status_rect.left = 50
        status_rect.centery = 440
        self.screen.blit(status_text, status_rect)

    def update_env (self, readings, speed):
        if self.queue is None: return 
        self.queue.put((readings, speed))


def avoid(readings):
    global INICIO
    lspeed = 0; rspeed = 0; status = "Parado"
    izq, izq_fro, front, izq_back = (
            np.mean([readings[0], readings[15]]),
            np.mean([readings[1], readings[2]]),
            np.mean([readings[3], readings[4]]),
            np.mean([readings[13], readings[14]])) 

    if INICIO:
        if front < 0.4:
            lspeed, rspeed, status = 1, 0, "curva inicio" # 
        elif izq < 0.3:
            INICIO = False
        else:
            lspeed, rspeed, status = 0.5, 0.5, "inicio" # 
    elif front < 0.4:
        if izq < 0.3:
            lspeed, rspeed, status = 1, 0, "curva" # 
        """else:
            if readings[15] < 0.3:
                lspeed, rspeed, status = 0.5, 0.1, "aun no salido"
            elif readings[15] > 0.9 and readings[1] < 0.4:
                lspeed, rspeed, status = +0.3, 0.2, "final curva"
            else:
                lspeed, rspeed, status = +0.3, front - 0.3, "paralelo pared pared" """
    elif izq_fro < 0.4 and izq > 0.5:
        lspeed, rspeed, status = 0.3, 0.1, "terminando vuelta extremo" # 
    
    else:
        if (readings[0] > 0.9 and readings[15] < 0.4):
            lspeed, rspeed, status = +0.4, 0.4, "inicio extremo" # 
        elif izq < 0.2:
            if readings[2] == 1:
                lspeed, rspeed, status = +0.4, 0.4, "inicio curva" # 
            elif izq < 0.1:
                lspeed, rspeed, status = +0.3, 0.2, "muy cerca de la pared" #
            else:
                if np.isclose(izq_fro, izq_back, atol = 0.05):
                    lspeed, rspeed, status = +0.5, +0.5, "cabecea largo" # 
                elif izq_fro < izq_back:
                    lspeed, rspeed, status = +0.2 + (izq_back - izq_fro), +0.2, "cabecea lejos" #
                else:
                    lspeed, rspeed, status = +0.2, +0.2 + (izq_fro - izq_back), "cabecea cerca" #
        elif  izq_fro < 0.5:
            lspeed, rspeed, status = +0.3, +0.3, "acercandose pared" # 
        else:
            lspeed, rspeed, status = +0.1, +0.45, "lejos de todo" #  # 
    return lspeed, rspeed, status
    

def main(args=None):
    display = DebugDisplay()
    coppelia = robotica.Coppelia()
    robot = robotica.P3DX(coppelia.sim, 'PioneerP3DX')
    coppelia.start_simulation()
    while coppelia.is_running():
        readings = robot.get_sonar()
        readings_use = (
            np.mean([readings[0], readings[15]]),
            np.mean([readings[1], readings[2]]),
            np.mean([readings[3], readings[4]]),
            np.mean([readings[5], readings[6]]),
            np.mean([readings[7], readings[8]]),
            np.mean([readings[11], readings[12]]),
            np.mean([readings[13], readings[14]]))
        lspeed, rspeed, status = avoid(readings)
        display.update_env(readings_use, (lspeed, rspeed, status))
        robot.set_speed(lspeed, rspeed)
        
    coppelia.stop_simulation()

if __name__ == '__main__':
    main()