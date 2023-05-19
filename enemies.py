from math import *
from random import *
import pygame
from settings import *
pygame.init()
enemy_name_font=pygame.font.SysFont('Times New Roman',20)
infinity=10**100
e_rating=[1,2,3,6,               infinity]
d_colors=[
    [255,255,255],
    [155,255,155],
    [255,125,0],#2
    [200,255,255],
    [255,0,0],
    [255,255,0],#5
    [0,255,255],
    [0,0,255],
    [255,0,255],#8
    [125,0,125],
    [125,125,125],
    [255,215,0],
    [55,55,55]#12
    ]
d_color_power_level=[0,1,3,6,10,15,21,28,36,45,55,66,78,91,105,120]
color_names=[
    "White",
    "Lime",
    "Orange",
    "Snow White",
    "Red",
    "Yellow",
    "Light Blue",
    "Blue",
    "Pink",
    "Purple",
    "Gray",
    "Gold",
    "Dark"
    ]
e_names=[
    "Duck",
    "Hedgehog",
    "Fairy",
    "Eygel"
    ]
whitelist=[[i,i,i] for i in range(256)]
mbsscreen=pygame.Surface((500,500))
mbsscreen.set_alpha(55)
class Enemy:
    def __init__(self,req_power,difficulty_bonus,a_data=[]):
        self.a_data=a_data
        self.deathrattle=[]
        if self.a_data==[]:
            self.dbonus=difficulty_bonus
            self.t_power=1+req_power/20
            self.power=req_power
            self.tips=-1
            while e_rating[self.tips]>self.power:
                self.tips=randint(1,len(e_rating))-1
            self.power-=e_rating[self.tips]
            self.primary_color=randint(1,len(d_colors))-1
            while d_color_power_level[self.primary_color]>self.power:
                self.primary_color=randint(1,len(d_colors))-1
            self.power-=d_color_power_level[self.primary_color]
            self.secondary_color=randint(1,len(d_colors))-1
            while d_color_power_level[self.secondary_color]>self.power:
                self.secondary_color=randint(1,len(d_colors))-1
            if self.secondary_color!=self.primary_color:
                self.name=color_names[self.primary_color]+"-"+color_names[self.secondary_color]+" "+e_names[self.tips]
            else:
                self.name=color_names[self.secondary_color]+" "+e_names[self.tips]
            self.namesprite=enemy_name_font.render(self.name,1,(0,255,0))
        else:
            self.tips=self.a_data[0]
            self.dbonus=1
            self.t_power=1
            self.primary_color=self.a_data[1]
            self.secondary_color=self.a_data[2]
        self.colors=[self.primary_color,self.secondary_color]
        self.sprite=pygame.Surface((500,500))
        self.bonus=[0 for i in range(100)]
        self.True_name=e_names[self.tips]
        if self.tips==0:
            self.maxhp=40+randint(-5,5)
            # Attacks work like this
            # 0th index is the chance in % of the attack happening 
            # 1st index is a list containing all efects of an attack, where
            # 1 is attacking, second index is how much damage
            # 2 is blocking, second index means how much, 3rd index is target
            # 3 is gaining an effect, second index indicates what effect, 3 index is how much, 4th index is target
            # 4 is damaging itself
            # 5 is summoning an enemy, with some data added later, ig
            self.a_pattern="random"
            self.attacks=[
                [25,[[1,8],[1,8]],"Twin Flap"],
                [25,[[2,12,0],[2,3,1]],"Protect"],
                [25,[[1,15]],"Full Flap"],
                [25,[[2,8,0],[1,8]],"Careful Flap"]
                ]
            self.sprites=[
                Ssheet.subsurface((16,0,15,30)),
                Ssheet.subsurface((31,0,7,30)),
                ]
            self.do_color(self.sprites[0],[[249,245,241],[238,238,238],[227,227,227],[212,212,212]],d_colors[self.primary_color])
            self.do_color(self.sprites[1],[[249,245,241],[238,238,238],[227,227,227],[212,212,212]],d_colors[self.secondary_color])
            self.sprites[0]=pygame.transform.scale(self.sprites[0],(200,400))
            self.sprites[1]=pygame.transform.scale(self.sprites[1],(ceil(200/15*7),400))
            self.sprites[0].set_colorkey((1,0,0))
        if self.tips==1:
            self.maxhp=45+randint(0,9)
            self.a_pattern="random"
            self.bonus[5]+=3
            self.sprites=[
                pygame.transform.scale(Ssheet.subsurface((39,0,33,29)),(330,290)),
                ]
            self.do_color(self.sprites[0],whitelist[:174],d_colors[self.primary_color])
            self.do_color(self.sprites[0],whitelist[173:],d_colors[self.secondary_color])
            self.attacks=[
                [25,[[3,5,1,0]],"Sharpen"],
                [25,[[3,1,4,0],[2,0,0]],"Defend"],
                [50,[[1,3] for i in range(6)],"Impale"]
                ]
            self.sprites[0]=pygame.transform.scale(self.sprites[0],(330,290))
            self.sprites[0].set_colorkey((1,0,0))
        elif self.tips==2:
            self.maxhp=25+randint(0,randint(1,20))
            self.a_pattern="random"
            self.bonus[1]+=1
            self.bonus[0]+=1
            self.attacks=[
                [33,[[3,1,2,1]],"Freshen"],
                [33,[[3,0,2,1]],"Polish"],
                [33,[[2,5,1],[2,8,0],[1,12]],"Clean"],
                [1,[[1,2] for i in range(10)],"Exterminate"],
                ]
            self.sprite.fill((0,0,0))
            self.sprites=[
                Ssheet.subsurface((73,0,17,39)),(170,390),
                ]
            p_pixels=[]
            s_pixels=[]
            for i in range(17):
                for i1 in range(39):
                    color=self.sprites[0].get_at((i,i1))
                    if color[0]>color[1]+50 and color[0]>color[2]+50:
                        if not color in p_pixels:
                            p_pixels.append(list(color[:3]))
                    elif color[1]>color[2]+50 and color[1]>color[0]+50:
                        pass
                    elif not color in s_pixels:
                        s_pixels.append(list(color[:3]))
            self.do_color(self.sprites[0],p_pixels,d_colors[self.primary_color])
            self.do_color(self.sprites[0],s_pixels,d_colors[self.secondary_color])
            self.sprites[0]=pygame.transform.scale(self.sprites[0],(170,390))
            self.sprites[0].set_colorkey((1,0,0))
        elif self.tips==3:
            self.maxhp=55+randint(0,20)
            self.a_pattern="random"
            self.attacks=[
                [25,[[3,0,-2,2]],"Unstrike"],
                [25,[[3,1,-2,2]],"Undefend"],
                [25,[[3,0,3,0],[3,1,3,0],[1,0],[1,0],[1,0],[1,0],[1,0]],"Holy Blast"],
                [25,[[3,0,2,1],[3,1,2,1],[2,6,1]],"Bless"]
                ]
        if 1 in self.colors:
            self.bonus[1]+=e_rating[self.tips]+randint(-1,1)
        if 2 in self.colors:
            self.bonus[0]+=e_rating[self.tips]+randint(-1,1)
        self.bonus=[int(i*self.dbonus*self.t_power) for i in self.bonus]
        self.block=0
        self.next_block=0
        self.maxhp*=self.dbonus*self.t_power
        self.maxhp=int(self.maxhp)
        self.hp=self.maxhp
        self.atheta=0
        self.attacks_played=[]
    def do_color(self,sprite,lis,color2):
        for i1 in range(sprite.get_width()):
            for i2 in range(sprite.get_height()):
                color=sprite.get_at((i1,i2))
                if list(color[:-1]) in lis:
                    sprite.set_at((i1,i2),(color[0]/255*color2[0],color[1]/255*color2[1],color[2]/255*color2[2]))
    def prepare(self,enemies,player):
        self.block=self.next_block
        self.next_block=0
        self.out_damage=0
        self.friends=enemies
        self.enemy=player
        self.attacks_played=[]
        if self.a_pattern=="random":
            action=random()*100
            for i in self.attacks:
                if action>=i[0]:
                    action-=i[0]
                else:
                    action=i
                    break
            for i in action[1]:
                if i[0]==1:
                    self.out_damage+=max(1,int((self.bonus[0]+i[1])*max(0.75,self.dbonus/2)*self.t_power))
                else:
                    self.attacks_played.append(i)
        self.action=action
    def target(self,group):
        if group==0:
            return [self]
        elif group==1:
            return self.friends
        elif group==3:
            return [choice(self.friends)]
        elif group==2:
            return [self.enemy]
    def fight(self,enemies):
        for i in self.attacks_played:
            if i[0]==2:
                targets=self.target(i[2])
                for i1 in targets:
                    i1.next_block+=int((self.bonus[1]+i[1])*max(0.75,self.dbonus/2)*self.t_power)
            elif i[0]==3:
                targets=self.target(i[3])
                for i1 in targets:
                    i1.bonus[i[1]]+=int(i[2]*self.t_power)
            elif i[0]==4:
                self.hp-=i[1]
            elif i[0]==5:
                enemies.append(Enemy(0,0,i[1]))
    def resprite(self):
        self.atheta+=2*pi/100
        if self.tips==0:
            self.sprite.fill((0,0,0))
            self.sprite.blit(self.sprites[1],(250-self.sprites[1].get_width()/2,cos(self.atheta)*20+100))
            self.sprite.blit(self.sprites[0],(150,100-cos(self.atheta)*2))
        elif self.tips==1: #heg hog cute
            self.sprite.fill((0,0,0))
            for i in range(self.bonus[5]):
                pygame.draw.polygon(self.sprite,d_colors[self.secondary_color],((250+cos(i+self.atheta/3-0.04)*150,250+sin(i+self.atheta/3-0.04)*150),
                                                                        (250+cos(i+self.atheta/3+0.04)*150,250+sin(i+self.atheta/3+0.04)*150),
                                                                        (250+cos(i+self.atheta/3)*200,250+sin(i+self.atheta/3)*200)),3)
            self.sprite.blit(self.sprites[0],(250-self.sprites[0].get_width()/2,250-self.sprites[0].get_height()/2))
        elif self.tips==2:
            self.sprite.blit(mbsscreen,(0,0))
            self.sprite.blit(self.sprites[0],(250-self.sprites[0].get_width()/2+sin(self.atheta/3)*120,250-self.sprites[0].get_height()/2+sin(self.atheta/3*2)*60))
            
        elif self.tips==3:
            self.sprite.fill((0,0,0))
            pygame.draw.circle(self.sprite,(255,255,255),(250,250),250,10)
            pygame.draw.circle(self.sprite,(255,255,255),(250,250),320,10)
            pygame.draw.circle(self.sprite,d_colors[self.primary_color],(250,250+sin(self.atheta/3)*210),30,5)
            pygame.draw.circle(self.sprite,d_colors[self.secondary_color],(250+cos(self.atheta/3)*210,250),30,5)
            pygame.draw.circle(self.sprite,d_colors[self.primary_color],(250+cos(self.atheta/3+pi/2)*200,250+sin(self.atheta/3+pi/2)*200),30,5)
            pygame.draw.circle(self.sprite,d_colors[self.secondary_color],(250+cos(self.atheta/3-pi/2)*200,250+sin(self.atheta/3-pi/2)*200),30,5)
            pygame.draw.circle(self.sprite,(255,255,255),(250+cos(self.atheta/3)*100,250+sin(self.atheta/3)*100),70,5)
            pygame.draw.circle(self.sprite,d_colors[self.primary_color],(250+cos(self.atheta/3-pi)*100,250+sin(self.atheta/3-pi)*210),30,5)
            pygame.draw.circle(self.sprite,d_colors[self.secondary_color],(250+cos(self.atheta/3-pi+pi/6)*155,250+sin(self.atheta/3-pi+pi/6)*210),30,5)
            pygame.draw.circle(self.sprite,d_colors[self.secondary_color],(250+cos(self.atheta/3-pi-pi/6)*155,250+sin(self.atheta/3-pi-pi/6)*210),30,5)
            pygame.draw.circle(self.sprite,(255,255,255),(250+cos(self.atheta/3)*100,250+sin(self.atheta/3)*100),55,10)
            for i in range(20):
                i1=i
                i=2*pi/20*i
                pygame.draw.circle(self.sprite,[d_colors[self.secondary_color],d_colors[self.primary_color]][i1%2],(250+sin(self.atheta/9+i)*280,250+cos(self.atheta/9+i)*280),30,5)
#Syntax e=Enemy(20000,1)
class Boss:
    def __init__(self,level,special=""):
        self.action=[0,0,"Getting Ready"]
        self.sprite=pygame.Surface((500,500))
        self.deathrattle=[]
        self.level=level
        if special=="":
            if self.level==0:
                self.tips=randint(0,2)
                #self.tips=2
                # Attacks work like this
                # 0th index is the chance in % of the attack happening 
                # 1st index is a list containing all efects of an attack, where
                # 1 is attacking, second index is how much damage
                # 2 is blocking, second index means how much, 3rd index is target
                # 3 is gaining an effect, second index indicates what effect, 3 index is how much, 4th index is target
                # 4 is damaging itself
                # 5 is summoning an enemy, with some data added later, ig
                if self.tips==0:
                    self.maxhp=350
                    self.True_name="KR_AVIS"
                    self.bonus=[0 for i in range(100)]
                    self.sprite=pygame.Surface((500,500))
                    self.sprites=[Ssheet.subsurface((91,0,71,94))]
                    #self.sprites[0].set_alpha(55)
                    self.a_pattern="scripted"
                    self.c_attack=0
                    self.attacks=[
                        [ [ [5,[0,0,0]], [5,[1,0,0]]  ],"Mitosis"],
                        [[[4,10],[1,10],[1,10],[1,10],[1,10], [1,10],[1,10],[1,10],[1,10]],
                         "Quadrotatic Diffusion"],
                        [[[2,50,0],[3,5,1,0]],"Javelinize"],
                        [[[1,50]],"Obliterate"],
                        [[[3,0,4,1],[3,1,4,1]],"Power Up"],
                        ]
                    self.sprites[0]=pygame.transform.scale(self.sprites[0],(71*5,94*5))
                elif self.tips==1:
                    self.maxhp=200
                    self.True_name="The Party"
                    self.bonus=[0 for i in range(100)]
                    self.sprite=pygame.Surface((500,500))
                    self.sprites=[pygame.transform.scale(pygame.image.load("Assets\Random Stuff\\"+i+".png"),(125,125)) for i in ["Bear","Monk","Warlock","Druid","Knight","Horse","Mage"]]
                    self.a_pattern="scripted"
                    self.c_attack=0
                    self.attacks=[
                            [[[4,3]],"Introduce Yourself"],
                            [[[2,20,1]],"Use Conversation Skills"],
                            [[[1,5], [1,5], [1,5], [1,5]],"Argue"],
                            [[[3,0,10,0]],"Get Angry"],
                            [[[1,20]],"Break Down"],
                            [ [ [6,"The Gank"],[4,20000]],"Split Up"],
                            ]
                    self.deathrattle=[[6,"The Gank"]]
                elif self.tips==2: # Master Shiguken, king of Strength
                    self.maxhp=200
                    self.True_name="Master Shiguken"
                    self.sprites=[pygame.transform.scale(pygame.image.load("Assets\Enemy Sprites\Alpha-Shiguken.jpg"),(500,500))]
                    self.bonus=[0 for i in range(100)]
                    self.bonus[0]=5
                    self.a_pattern="random"
                    self.attacks=[
                            [20,[[3,0,3,0]],"Warm Up"],
                            [20,[[1,7],[1,7],[1,8],[1,8],[3,0,-3,0]],"Release Steam"],
                            [20,[[1,20],[3,0,1,0]],"Red Slash"],
                            [20,[[2,20,0],[3,7,2,0]],"Toughen Up"],
                            [20,[[3,6,3,0],[3,0,1,0]],"Gain Momentum"]
                            ]
                    self.deathrattle=[[6,"Enraged Master Shiguken"]]
                self.hp=self.maxhp
                self.next_block=0
                self.block=0
                self.atheta=0
                self.dbonus=1
                self.t_power=1
                self.attacks_played=[]
        elif special=="The Gank":
            self.attacks_played=[]
            self.tips=0
            self.maxhp=200
            self.True_name="The Party"
            self.bonus=[0 for i in range(100)]
            self.sprite=pygame.Surface((500,500))
            self.sprites=[pygame.transform.scale(pygame.image.load("Assets\Random Stuff\\"+i+".png"),(125,125)) for i in ["Bear","Monk","Warlock","Druid","Knight","Horse","Mage"]]
            for i in range(7):
                self.sprites[i].set_alpha(100)
            self.a_pattern="SevenFoldRandom"
            self.attacks=[
                [[[1,10]],"Something"],
                [[[3,1,2,0]],"Something"],
                [[[3,0,2,0]],"Something"],
                [[[2,10,0]],"Something"],
                [[[4,-4]],"Something"],
                [[[1,3],[1,3]],"Something"],
                [[[2,3,0],[2,3,0]],"Something"],
                ]
            self.hp=self.maxhp
            self.next_block=0
            self.block=0
            self.atheta=0
            self.dbonus=1
            self.t_power=1
        elif special=="Enraged Master Shiguken":
            self.attacks_played=[]
            self.action=[0,0,"Getting Ready"]
            self.maxhp=200
            self.tips=1
            self.True_name="Enraged Master Shiguken"
            self.sprites=[pygame.transform.scale(pygame.image.load("Assets\Enemy Sprites\Beta-Shiguken.jpg"),(500,500))]
            self.bonus=[0 for i in range(100)]
            self.bonus[0]=5
            self.a_pattern="random"
            self.attacks=[
                    [20,[[3,0,6,0]],"Rage"],
                    [20,[[1,5],[1,5],[1,9],[1,9],[3,0,-2,0]],"Cool Down"],
                    [20,[[1,20],[1,20],[3,0,2,0]],"Two Red Slashes"],
                    [20,[[2,10,0],[3,7,3,0]],"Solidify"],
                    [20,[[3,6,6,0],[3,0,4,0]],"Gain Momentum"]
                    ]
            self.deathrattle=[[-1,2]]
            self.hp=self.maxhp
            self.next_block=0
            self.block=0
            self.atheta=0
            self.dbonus=1
            self.t_power=1
    def prepare(self,enemies,player):
        self.block=self.next_block
        self.next_block=self.bonus[7]
        self.out_damage=self.bonus[6]
        self.friends=enemies
        self.enemy=player
        self.attacks_played=[]
        if self.a_pattern=="random":
            action=random()*100
            for i in self.attacks:
                if action>=i[0]:
                    action-=i[0]
                else:
                    action=i
                    break
            for i in action[1]:
                if i[0]==1:
                    self.out_damage+=max(1,int((self.bonus[0]+i[1])*max(0.75,self.dbonus/2)*self.t_power))
                else:
                    self.attacks_played.append(i)
        elif self.a_pattern=="scripted":
            for i in self.attacks[self.c_attack][0]:
                if i[0]==1:
                    self.out_damage+=max(1,int((self.bonus[0]+i[1])*max(0.75,self.dbonus/2)*self.t_power))
                else:
                    self.attacks_played.append(i)
            action=[0 ,self.attacks[self.c_attack][0] ,self.attacks[self.c_attack][1] ]
            self.c_attack=(self.c_attack+1)%len(self.attacks)
        elif self.a_pattern=="SevenFoldRandom":
            for i1 in range(7):
                action=self.attacks[randint(0,6)]
                for i in action[0]:
                    if i[0]==1:
                        self.out_damage+=max(1,int((self.bonus[0]+i[1])*max(0.75,self.dbonus/2)*self.t_power))
                    else:
                        self.attacks_played.append(i)
            action=[0 ,action[0] ,action[1] ]
        self.action=action
        self.hp=min(self.hp,self.maxhp)
    def target(self,group):
        if group==0:
            return [self]
        elif group==1:
            return self.friends
        elif group==3:
            return [choice(self.friends)]
        elif group==2:
            return [self.enemy]
    def fight(self,enemies):
        for i in self.attacks_played:
            if i[0]==2:
                targets=self.target(i[2])
                for i1 in targets:
                    i1.next_block+=int((self.bonus[1]+i[1])*max(0.75,self.dbonus/2)*self.t_power)
            elif i[0]==3:
                targets=self.target(i[3])
                for i1 in targets:
                    i1.bonus[i[1]]+=int(i[2]*self.t_power)
            elif i[0]==4:
                self.hp-=i[1]
            elif i[0]==5:
                enemies.append(Enemy(0,0,i[1]))
            elif i[0]==6:
                enemies.append(Boss(-1,i[1]))
    def resprite(self):
        self.atheta+=2*pi/100
        if self.level==0:
            if self.tips==0:
                self.sprite.blit(self.sprites[0],(250-self.sprites[0].get_width()/2,250-self.sprites[0].get_height()/2))
            elif self.tips==1:
                self.sprite.blit(self.sprites[0],(250-self.sprites[0].get_width()/2,250-self.sprites[0].get_height()/2))
                self.sprite.blit(self.sprites[1],(400-self.sprites[0].get_width()/2,250-self.sprites[0].get_height()/2))
                self.sprite.blit(self.sprites[2],(100-self.sprites[0].get_width()/2,250-self.sprites[0].get_height()/2))
                self.sprite.blit(self.sprites[3],(250-self.sprites[0].get_width()/2,400-self.sprites[0].get_height()/2))
                self.sprite.blit(self.sprites[4],(250-self.sprites[0].get_width()/2,100-self.sprites[0].get_height()/2))
                self.sprite.blit(self.sprites[5],(400-self.sprites[0].get_width()/2,100-self.sprites[0].get_height()/2))
                self.sprite.blit(self.sprites[6],(100-self.sprites[0].get_width()/2,100-self.sprites[0].get_height()/2))
                
            elif self.tips==2:
                self.sprite.blit(self.sprites[0],(0,0))
        elif self.level==-1:
            if self.tips==1:
                self.sprite.blit(self.sprites[0],(0,0))
            elif self.tips==0:
                self.sprite.blit(mbsscreen,(0,0))
                for i in range(7):
                    if i==0:
                        adx=cos(self.atheta/5)*200
                        ady=sin(self.atheta/2.5)*100
                    elif i==1:
                        adx=cos(self.atheta/2.5+pi/2)*100
                        ady=sin(self.atheta/5+pi/2)*200
                    elif i==2:
                        adx=-cos(self.atheta/4)*150
                        ady=sin(self.atheta/3)*150
                    elif i==3:
                        adx=cos(self.atheta/3+pi)*150
                        ady=sin(self.atheta/4+pi)*150
                    elif i==4:
                        adx=cos(self.atheta/5+pi)*80
                        ady=sin(self.atheta/4+pi)*180
                    elif i==6:
                        adx=cos(self.atheta/7+pi)*180
                        ady=-sin(self.atheta/4+pi)*80
                    else:
                        adx=-cos(self.atheta/3)*80
                        ady=sin(self.atheta/3)*80
                    self.sprite.blit(self.sprites[i],(250-self.sprites[0].get_width()/2+adx,250-self.sprites[0].get_height()/2+ady))
                
                
