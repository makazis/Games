from random import *
from math import *
import pygame
pygame.init()
win=pygame.display.set_mode((2400,1200))
run=True
clock=pygame.time.Clock()
drag=0.001#0.98
drag=1-drag
gravity=0.02
restitution=0.9
potential_decay=0.01
class Ball:
    def __init__(self):
        self.x=1200+(random()*2-1)*600
        self.y=600+(random()*2-1)*600
        self.yspeed=random()*2-1
        self.xspeed=random()*2-1
        self.vectors=[]
        self.radius=randint(1,1)*10
        self.k_e=0 #kinetic_energy
        self.mass=self.radius**2*pi/100
        self.angle=0
        self.p_e=0 #potential energy
    def exist(self):
        global chosen_ball
        self.color=(255,255,255)
        for i in self.vectors:
            self.xspeed+=i[0]
            self.yspeed+=i[1]
        self.vectors=[]
        self.xspeed=self.xspeed*drag
        self.yspeed=self.yspeed*drag
        self.x+=self.xspeed
        self.y+=self.yspeed
        #self.x=min(max(self.radius,self.x),2400-self.radius)
        #if self.x in [self.radius,2400-self.radius]: self.xspeed=-self.xspeed
        #self.y=min(max(self.radius,self.y),1200-self.radius)
        #if self.y in [self.radius,1200-self.radius]: self.yspeed=-self.yspeed
        self.k_e=sqrt(self.xspeed**2+self.yspeed**2)
        self.next_x=self.x+self.xspeed*drag
        self.next_y=self.y+self.yspeed*drag
        self.angle=atan2(-self.yspeed,-self.xspeed)
        for i in balls:
            if sqrt((self.next_x-i.x)**2+(self.next_y-i.y)**2)<self.radius+i.radius and i!=self:
                total_k_e=(self.k_e+i.k_e)*restitution
                energy_distribution=(i.mass/(self.mass+i.mass))
                self.speed=total_k_e*energy_distribution
                self.escape_angle=atan2(self.next_y-i.y,self.next_x-i.x)
                self.escape_angle=2*pi-self.angle+2*self.escape_angle
                i.vectors.append([self.xspeed*(1-energy_distribution)*restitution,self.yspeed*(1-energy_distribution)*restitution])
                self.xspeed=self.speed*cos(self.escape_angle)
                self.yspeed=self.speed*sin(self.escape_angle)
                if self==chosen_ball: chosen_ball=i
                elif i==chosen_ball: chosen_ball=self
                
                    
            dist=sqrt((self.x-i.x)**2+(self.y-i.y)**2)
            if dist<self.radius+i.radius and i!=self:
                self.color=(0,25,0)
                #self.xspeed=0
                #self.yspeed=0
                self.xspeed*=1.01/restitution
                self.yspeed*=1.01/restitution
                #self.radius*=random()/50+0.99
                #self.mass=self.radius**2*pi/100
        if self.color!=(0,25,0):
            self.xspeed*=1+self.p_e
            self.yspeed*=1+self.p_e
            self.p_e*=1-potential_decay
        self.mid_angle=atan2(600-self.y,1200-self.x)
        self.vectors.append([cos(self.mid_angle)*gravity,sin(self.mid_angle)*gravity])
balls=[Ball() for i in range(100)]
chosen_ball=balls[0]
while run:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    win.fill((0,0,0))
    t_k_e=0
    mouse_pos=pygame.mouse.get_pos()
    mouse_down=pygame.mouse.get_pressed()
    if mouse_down[0]:
        angle=atan2(mouse_pos[1]-chosen_ball.y,mouse_pos[0]-chosen_ball.x)
        chosen_ball.vectors.append([cos(angle)*0.2,sin(angle)*0.2])
    for i in balls:
        i.exist()
        t_k_e+=i.k_e
        if i==chosen_ball: pygame.draw.circle(win,(55,255,255),(i.x,i.y),i.radius,int(i.radius/4))
        else: pygame.draw.circle(win,i.color,(i.x,i.y),i.radius,int(i.radius/4))
    pygame.display.set_caption(str(t_k_e))
    pygame.draw.circle(win,(0,155,0),(1200,600),3)
    pygame.display.update()
    clock.tick(100)
pygame.quit()
