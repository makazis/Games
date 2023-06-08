from math import *
from random import *
import pygame
pygame.init()
win=pygame.display.set_mode((2400,1200))
S1=pygame.Surface((1200,1200))
S2=pygame.Surface((1200,1200))
#S1.set_alpha((127))
S2.set_alpha((127))
mouse_Q=[2400/win.get_width(),1200/win.get_height()]
run=True
clock=pygame.time.Clock()
click=[0,0,0]
fonts={}
texts={}
def produce(font,size,text,color):
    global fonts,texts
    font_key=font+str(size)+text+str(color)
    if not font+str(size) in fonts:
        fonts[font+str(size)]=pygame.font.SysFont(font,size)
    if not font_key in texts:
        texts[font_key]=fonts[font+str(size)].render(text,1,color)
    return texts[font_key]
def eventall():
    global run, mouse_pos,keys,mouse_down,click
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()
    mouse_pos=pygame.mouse.get_pos()
    mouse_pos=[mouse_pos[i]*mouse_Q[i] for i in range(2)]
    mouse_down=pygame.mouse.get_pressed()
    if keys[27]: run=False
    for i in range(3):
        if mouse_down[i]:
            click[i]+=1
        else:
            click[i]=0



class ball:
    def __init__(self,tips=0,surface=0):
        self.surface=[S1,S2][surface]
        self.tips=tips
        self.sprite=pygame.Surface((20,20))
        if self.tips==0:
            self.mass=3
            pygame.draw.circle(self.sprite,(255,255,255),(10,10),10,2)
            pygame.draw.circle(self.sprite,(255,255,255),(0,10),5,2)
            
        self.sprite.set_colorkey((0,0,0))
        self.xspeed=0
        self.yspeed=0
        self.vectors=[]
        self.x=600
        self.y=0
    def draw(self):
        self.sprite2=pygame.transform.rotate(self.sprite,0-self.angle*180/pi)
        self.surface.blit(self.sprite2,(self.x-self.sprite2.get_width()/2,self.y-self.sprite2.get_height()/2))
    def exist(self):
        global angl
        self.angle=atan2(-self.yspeed,-self.xspeed)
        for i in self.vectors:
            self.xspeed+=i[0]
            self.yspeed+=i[1]
        self.vectors=[]
        #self.x+=self.xspeed
        #self.y+=self.yspeed
        #self.next_x=self.x+self.xspeed
        #self.next_y=self.y+self.yspeed
        self.vectors.append([0,0.006*self.mass])
        self.x=min(1190,max(10,self.x))
        if self.x==1190 or self.x==10:
            self.xspeed=-self.xspeed*0.9
        for i in pegs:
            self.next_x=self.x+self.xspeed
            self.next_y=self.y+self.yspeed
            if sqrt((self.next_x-i.x)**2+(self.next_y-i.y)**2)<10+i.radius and i.surface==self.surface:
                angl=atan2(self.next_y-i.y,self.next_x-i.x)
                angl=pi-(self.angle-(pi/2+angl))+(pi/2+angl)
                self.tspeed=sqrt(self.xspeed**2+self.yspeed**2)*1# normal: 0.85
                self.xspeed=self.tspeed*cos(angl)
                self.yspeed=self.tspeed*sin(angl)
                if i in pegs:
                    pegs.remove(i)
        self.x+=self.xspeed
        self.y+=self.yspeed
        if self.y>1220:
            if self in balls:
                balls.remove(self)
class peg:
    def __init__(self,tips,surface,data=[]):
        self.tips=tips
        self.surface=[S1,S2][surface]
        if self.tips==0:
            self.x=600+randint(-200,200)
            self.y=600+randint(-300,100)
            self.radius=randint(10,20)
    def draw(self):
        if self.x>0:
            pygame.draw.circle(self.surface,(255,255,255),(self.x,self.y),self.radius)
    def exist(self):
        #self.x+=cos(atheta)*2
        #self.y+=sin(atheta)
        pass
balls=[]
pegs=[peg(0,randint(0,1)) for i in range(200)]
angl=0
atheta=0
while run:
    atheta+=2*pi/400
    eventall()
    win.fill((120,120,255))
    S1.fill((125,0,0))
    S2.fill((0,0,125))
    if 1800>mouse_pos[0]>600:
        if click[0]>=1 and click[0]%15==0:
            balls.append(ball(0,0))
            balls.append(ball(0,1))
            rel_angle=atan2(-mouse_pos[1],1200-mouse_pos[0])+pi
            balls[-1].vectors.append([cos(rel_angle)*3,sin(rel_angle)*3])
            balls[-2].vectors.append([cos(rel_angle)*3,sin(rel_angle)*3])
    for i in balls:
        i.exist()
        i.draw()
    for i in pegs:
        i.exist()
        i.draw()
    #pygame.draw.circle(S1,(0,0,0),(500+cos(angl)*60,600+sin(angl)*60),20)
    win.blit(S1,(600,0))
    win.blit(S2,(600,0))
    pygame.display.update()
pygame.quit()
