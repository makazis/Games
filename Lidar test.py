from math import *
from random import *
import pygame
pygame.init()
win=pygame.display.set_mode((2400,1200))
map_s=pygame.Surface((1200,1200))
map_s.fill((125,65,0))
run=True
MAP=[[(i1!=59)*(i1!=0)*(i!=59)*(i!=0)*randint(0,5)!=0 for i1 in range(60)] for i in range(60)]
MAP[30][30]=1
for i in range(60):
    for i1 in range(60):
        if MAP[i][i1]==0:
            pygame.draw.rect(map_s,(255,155,55),(i*20+1,i1*20+1,18,18))
x=30
z=30
pygame.display.update()
pygame.mouse.set_pos((600,600))
tx_angle=0
y_angle=0
FOV=1 #0 to pi
pygame.mouse.set_visible(False)
lidar_spots=[[(randint(0,599),randint(0,100),randint(0,599)),0] for i in range(1000)] #(x,y,z),tips
frame=0
player_speed=2
while run:
    frame+=1
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    keys=pygame.key.get_pressed()
    mouse_pos=pygame.mouse.get_rel()
    if not frame%20:
        pygame.mouse.set_pos((600,600))
    tx_angle+=mouse_pos[0]/400
    y_angle+=mouse_pos[1]/400
    if tx_angle>pi:
        tx_angle-=2*pi
    if tx_angle<-pi:
        tx_angle+=2*pi
    tri_angles=[(tx_angle-pi*2)%(-2*pi),tx_angle,(tx_angle-pi*2)%(2*pi),(tx_angle-pi)%(2*pi)]
    for x_angle in tri_angles:
        if x_angle-FOV<-pi:
            regions=[[-pi,x_angle+FOV],[pi-x_angle+FOV,pi]]
        elif x_angle+FOV>pi:
            regions=[[-pi,x_angle+FOV-pi*2],[x_angle-FOV,pi]]
        else:
            regions=[[x_angle-FOV,x_angle+FOV]]
        if keys[27]: run=False
        if keys[pygame.K_w]:
            x-=cos(x_angle)*player_speed/100
            z-=sin(x_angle)*player_speed/100
        if keys[pygame.K_a]:
            x-=cos(x_angle+pi/2*3)*player_speed/100
            z-=sin(x_angle+pi/2*3)*player_speed/100
        if keys[pygame.K_s]:
            x-=cos(x_angle+pi)*player_speed/100
            z-=sin(x_angle+pi)*player_speed/100
        if keys[pygame.K_d]:
            x-=cos(x_angle+pi/2)*player_speed/100
            z-=sin(x_angle+pi/2)*player_speed/100
        
        #Lidar Point Shot
        xtra_x_angle=random()*2-1
        xtra_y_angle=random()*2-1
        #Screen Drawing
        win.fill((0,0,0))
        for i in lidar_spots:
            shot_to_camera=atan2(i[0][2]-z*10,i[0][0]-x*10)
            for i1 in regions:
                if i1[1]>=shot_to_camera>=i1[0]:
                    xz_distance=sqrt((z*10-i[0][2])**2+(x*10-i[0][0])**2)
                    ball_radius=ceil(8/(xz_distance/100))-2
                    ball_y=(50-i[0][1])/60*848/xz_distance
                    camera_x_offset=(shot_to_camera%(2*pi)-x_angle%(2*pi))
                    if 1200+ball_radius/2>600+camera_x_offset*600>-ball_radius/2:
                        pygame.draw.circle(win,(255,255,255),(600+camera_x_offset*600,600+ball_y*100-y_angle*1000),ball_radius)
                    #print(camera_x_offset)
    win.blit(map_s,(1200,0))
    pygame.draw.circle(win,(255,0,0),(x*20+1210,z*20+10),5)
    pygame.display.set_caption(str(round(x_angle,3))+"  "+str(round(y_angle,3)))
    pygame.display.update()
pygame.quit()
