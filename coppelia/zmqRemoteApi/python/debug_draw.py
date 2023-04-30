
from multiprocessing import Process, Queue
import pygame as pg
import numpy as np

WIDTH: int = 10

def color_map(value):
    if value < 0.5: return pg.Color(255, 0, 0)
    elif value < 1.5: return pg.Color(0, 255, 0)
    elif value < 2.5: return pg.Color(255, 255, 0)
    else: return pg.Color(255, 0, 0)

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
        self.screen = pg.display.set_mode([300, 400])
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
        pg.draw.line(self.screen, behind_color, (100, 275), (200, 275), width=WIDTH)
        behind_text = self.font.render("{:2.2f}".format(readings[5]), True, (0, 0, 0))
        behind_rect = behind_text.get_rect()
        behind_rect.centerx = 150
        behind_rect.centery = 300
        self.screen.blit(behind_text, behind_rect)


    def draw_speed(self):
        speed = self.state[1]
        left_motor_text  = self.font.render("Left  Motor:", True, (0, 0, 0))
        right_motor_text = self.font.render("Right Motor:", True, (0, 0, 0))
        
        left_motor_rect = left_motor_text.get_rect()
        left_motor_rect.left = 50
        left_motor_rect.centery = 330
        right_motor_rect = right_motor_text.get_rect()
        right_motor_rect.left = 50
        right_motor_rect.centery = 360
        self.screen.blit(left_motor_text, left_motor_rect)
        self.screen.blit(right_motor_text, right_motor_rect)

        left_motor_text  = self.font.render("{:2.3f}".format(speed[0]), True, (0, 0, 0))
        right_motor_text = self.font.render("{:2.3f}".format(speed[1]), True, (0, 0, 0))
        
        left_motor_rect = left_motor_text.get_rect()
        left_motor_rect.left = 175
        left_motor_rect.centery = 330
        right_motor_rect = right_motor_text.get_rect()
        right_motor_rect.left = 175
        right_motor_rect.centery = 360
        self.screen.blit(left_motor_text, left_motor_rect)
        self.screen.blit(right_motor_text, right_motor_rect)

        

    def update_env (self, readings, speed):
        if self.queue is None: return 
        self.queue.put((readings, speed))


if __name__ == '__main__':
    display = DebugDisplay()
    while True: pass 