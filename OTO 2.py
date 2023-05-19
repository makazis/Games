#i want an infinite rougelike card game
# the name of the game should be JunkRat now
from math import *
from random import *
from cards import *
from enemies import *
import pygame
pygame.init()
#win=pygame.display.set_mode((2400,1200))
win=pygame.display.set_mode((0,0))

S=pygame.Surface((1200,600))
bcardsprite=pygame.Surface((200,300))
bcardsprite.set_alpha(200)
mouse_Q=[1200/win.get_width(),600/win.get_height()]
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
def achieve(which,get_achs=False):
    ach_file=open("Assets\\achievements.txt","r")
    achs=[]
    for i in ach_file:
        achs.append(int(i[:-1]))
    ach_file.close()
    if get_achs:
        return achs
    else:
        achs[which]=1
        ach_file=open("Assets\\achievements.txt","w")
        for i in range(len(achs)):
            ach_file.write(str(achs[i])+"\n")
        ach_file.close()
achs=achieve(0,True)
class Player:
    def __init__(self):
        self.deck=[]
        self.max_mana=3
        self.gold=99
        self.hp=150
        self.maxhp=150
    def draft(self,skippable=True,cards=[]):
        global run,click
        drafting=True
        if cards==[]:
            card_choice=[Card(1,[self.max_mana,achs])for i in range(3)] #Normally(Card(1,[3]))
        else:
            card_choice=cards[:3]
        while run and drafting:
            eventall()
            S.fill((0,0,0))
            for i in range(3):
                S.blit(card_choice[i].sprite,(100+i*400,150))
                if 300+i*400>mouse_pos[0]>100+i*400 and 450>mouse_pos[1]>150:
                    if click[0]==1:
                        self.deck.append(card_choice[i])
                        drafting=False
            if skippable:
                pygame.draw.rect(S,(155,155,155),(500,500,200,50))
                pygame.draw.rect(S,(255,255,255),(500,500,200,50),5)
                tsprite=produce("Times New Roman",35,"Skip",(255,255,255))
                S.blit(tsprite,(600-tsprite.get_width()/2,525-tsprite.get_height()/2))
                if 700>mouse_pos[0]>500 and 550>mouse_pos[1]>500 and click[0]==1:
                    drafting=False
            win.blit(pygame.transform.scale(S,win.get_size()),(0,0))
            clock.tick(100)
            pygame.display.update()
    def setup(self):
        self.t_deck=self.deck.copy()
        self.hand=[]
        self.bonus=[0 for i in range(100)]
    def draw(self):
        if len(self.t_deck)>0:
            card=choice(self.t_deck)
            self.hand.append(card)
            self.t_deck.remove(card)
    def play_card(self,card):
        self.mana-=card.level
        for i in range(len(card.effects)):
            if card.effects[i]==0:
                tdamage=card.data[i]+self.bonus[0]
                if tdamage>=50:
                    achieve(0)
                c2=c_enemy.block
                c_enemy.block=max(c_enemy.block-tdamage,0)
                tdamage-=c2
                if tdamage>0:
                    c_enemy.hp-=tdamage
                if c_enemy.bonus[5]>=0:
                    if self.block>0:
                        self.block-=c_enemy.bonus[5]
                    else:
                        self.hp-=c_enemy.bonus[5]
            elif card.effects[i]==1:
                self.block+=card.data[i]+self.bonus[1]
                if card.data[i]+self.bonus[1]>=50:
                    achieve(1)
            elif card.effects[i]==2:
                for i in range(card.data[i]):
                    self.draw()
            elif card.effects[i]==3:
                self.hp-=card.data[i]
            elif card.effects[i]==4:
                self.mana+=card.data[i]
            elif card.effects[i]==5:
                self.bonus[0]+=card.data[i]
            elif card.effects[i]==6:
                self.bonus[1]+=card.data[i]
            elif card.effects[i]==7:
                self.bonus[6]+=card.data[i]
            elif card.effects[i]==8:
                self.bonus[7]+=card.data[i]
            elif card.effects[i]==9:
                self.bonus[5]+=card.data[i]
        if card.seffect!=0:
            self.t_deck.append(card)
        if card in self.hand: self.hand.remove(card)
player=Player()
for i in range(8): # 8
    player.draft(False)
menu="Choosing where to go"
#menu="LootScreen"
reward_q=1
difficulty_bonus=1
event_count=0
# 0 is combat
# 1 is shop
# 2 is something else
unlocks=1
level=0
choicesS=[-1,-1,-1]
difficulty_bonuses=[0.75,1,1.25,1.5,2,3,5,10]
difficulty_colors=[[0,200,0],[200,200,0],[200,100,0],[200,0,0],[50,0,0],[125,0,125],[255,255,255],[125,125,0]]
difficulty_texts=[enemy_name_font.render(i,1,(0,255,0)) for i in [
    "A simple fight, with few rewards",
    "A fair fight, with adequate rewards",
    "A harder fight, with better rewards",
    "A difficult fight, with big rewards",
    "An extreme battle, with amazing loot",
    "An Epic battle, with remarkable loot",
    "A Legendary battle, with the loot of gods",
    "Gods can't beat them"
    ]]
while run and player.hp>0:
    eventall()
    if menu=="Choosing where to go":
        if choicesS==[-1,-1,-1]:
            level+=1
            if level==15: # First Boss
                menu="Combat"
                enemies=[Boss(0)]
                reward_q=1
                turn=0
                team_going=0
                facing_enemy=0
                player.setup()
                total_in_damage=0
                player.block=0
                player.next_block=0
            else:
                choicesS=[randint(0,event_count),randint(0,event_count),randint(0,event_count)]
                choices_enemies=[[],[],[]]
                for i in range(3):
                    if choicesS[i]==0:
                        difficulty_bonus=randint(0,randint(1,randint(4,6)))
                        #difficulty_bonus=randint(6,7)
                        choices_enemies[i].append(difficulty_bonus)
                        choices_enemies[i].append([])
                        total_power=int((level+2))#*difficulty_bonuses[difficulty_bonus])
                        while total_power>0:
                            this_power=randint(ceil(total_power/2),total_power)
                            total_power-=this_power
                            choices_enemies[i][1].append(Enemy(this_power,difficulty_bonuses[difficulty_bonus]))
        if menu=="Choosing where to go":
            S.fill((0,0,0))
            tsprite=produce("Times New Roman",30,"HP:"+str(player.hp)+"/"+str(player.maxhp)+"   Gold:"+str(player.gold),(255,255,255))
            S.blit(tsprite,(0,400))
            for i in range(3):
                if choicesS[i]==0:
                    pygame.draw.rect(S,(difficulty_colors[choices_enemies[i][0]]),(i*400,0,400,400))
                    pygame.draw.rect(S,(0,0,0),(i*400+20,20,360,360))
                    S.blit(difficulty_texts[choices_enemies[i][0]],(20+i*400,20))
                    for i1 in range(len(choices_enemies[i][1])):
                        S.blit(choices_enemies[i][1][i1].namesprite,(20+i*400,40+i1*20))
                    if i*400+400>mouse_pos[0]>i*400 and 400>mouse_pos[1]>0:
                        if click[0]==1:
                            menu="Combat"
                            enemies=choices_enemies[i][1]
                            reward_q=choices_enemies[i][0]
                            turn=0
                            team_going=0
                            facing_enemy=0
                            player.setup()
                            total_in_damage=0
                            player.block=0
                            player.next_block=0
    elif menu=="Combat":
        choicesS=[-1,-1,-1]
        enemies_alive=0
        if team_going==0:
            turn+=1
            player.hp-=max(0,total_in_damage-player.block)
            player.block=player.next_block+player.bonus[7]
            player.next_block=0
            total_in_damage=0
            for i in enemies:
                if i.hp>0:
                    if turn>1:
                        i.fight(enemies)
                    i.prepare(enemies,player)
                    i.hp-=player.bonus[6]
                    total_in_damage+=i.out_damage
                    if i.out_damage>0:
                        i.hp-=player.bonus[5]
                    enemies_alive+=1
            team_going=1
            player.mana=player.max_mana
            for i in player.hand:
                player.t_deck.append(i)
            player.hand=[]
            for i in range(6):
                player.draw()
        S.fill((0,0,0))
        c_enemy=enemies[facing_enemy%len(enemies)]
        while c_enemy.hp<=0:
            for i in c_enemy.deathrattle:
                if i[0]==1:
                    total_in_damage+=max(1,int((c_enemy.bonus[0]+i[1])*max(0.75,c_enemy.dbonus/2)*c_enemy.t_power))
                if i[0]==2:
                    targets=c_enemy.target(i[2])
                    for i1 in targets:
                        i1.next_block+=int((c_enemy.bonus[1]+i[1])*max(0.75,c_enemy.dbonus/2)*c_enemy.t_power)
                elif i[0]==3:
                    targets=c_enemy.target(i[3])
                    for i1 in targets:
                        i1.bonus[i[1]]+=int(i[2]*c_enemy.t_power)
                elif i[0]==4:
                    c_enemy.hp-=i[1]
                elif i[0]==5:
                    enemies.append(Enemy(0,0,i[1]))
                elif i[0]==6:
                    enemies.append(Boss(-1,i[1]))
                elif i[0]==-1:
                    achieve(i[1])
            enemies.remove(c_enemy)
            if len(enemies)==0:
                menu="LootScreen"
                break
            else:
                c_enemy=enemies[facing_enemy%len(enemies)]
        pygame.draw.rect(S,(155,155,155),(0,500,100,100))
        pygame.draw.rect(S,(155,155,155),(400,500,100,100))
        pygame.draw.rect(S,(255,255,255),(0,500,100,100),5)
        pygame.draw.rect(S,(255,255,255),(400,500,100,100),5)
        if c_enemy.hp>0:
            c_enemy.resprite()
            S.blit(c_enemy.sprite,(0,0))
            pygame.draw.rect(S,(0,0,0),(105,505,290,20))
            if c_enemy.hp>=1:
                pygame.draw.rect(S,(255-c_enemy.hp/c_enemy.maxhp*255,c_enemy.hp/c_enemy.maxhp*255,0),(396-c_enemy.hp/c_enemy.maxhp*290,505,c_enemy.hp/c_enemy.maxhp*290,20))
            pygame.draw.rect(S,(155,200,200),(396-c_enemy.block/c_enemy.maxhp*290,505,c_enemy.block/c_enemy.maxhp*290,20))
            tsprite=produce('Times New Roman',20,str(c_enemy.hp)+"/"+str(c_enemy.maxhp),(255,255,255))
            S.blit(tsprite,(250-tsprite.get_width()/2,505))
            tsprite=produce('Times New Roman',20,c_enemy.True_name,(255,255,255))
            S.blit(tsprite,(250-tsprite.get_width()/2,525))
            tsprite=produce('Times New Roman',15,"Will Use:",(255,255,255))
            S.blit(tsprite,(250-tsprite.get_width()/2,545))
            tsprite=produce('Times New Roman',15,c_enemy.action[2],(255,255,255))
            S.blit(tsprite,(250-tsprite.get_width()/2,560))
            tsprite=produce('Times New Roman',15,"Strength:"+str(c_enemy.bonus[0])+" Dexterity: "+str(c_enemy.bonus[1]),(255,255,255))
            S.blit(tsprite,(250-tsprite.get_width()/2,575))
            if c_enemy.block>0:
                tsprite=produce('Times New Roman',15,str(c_enemy.block),(0,0,205))
                S.blit(tsprite,(380-tsprite.get_width()/2,505))
            
        if 100>mouse_pos[0]>0 and 600>mouse_pos[1]>500:
            pygame.draw.polygon(S,(0,255,255),((20,550),(70,520),(70,580)),5)
            if click[0]==1:
                facing_enemy=facing_enemy-1
                if facing_enemy==-1:
                    facing_enemy+=len(enemies)
        else:
            pygame.draw.polygon(S,(255,255,255),((20,550),(70,520),(70,580)),5)
        if 500>mouse_pos[0]>400 and 600>mouse_pos[1]>500:
            pygame.draw.polygon(S,(0,255,255),((480,550),(430,520),(430,580)),5)
            if click[0]==1:
                facing_enemy=(facing_enemy+1)%len(enemies)
        else:
            pygame.draw.polygon(S,(255,255,255),((480,550),(430,520),(430,580)),5)
        for i in range(min(3,len(player.hand))):
            try:
                S.blit(player.hand[i].sprite,(500+i*200,0))
                if player.mana<player.hand[i].level:
                    S.blit(bcardsprite,(500+i*200,0))
                else:
                    if 700+i*200>mouse_pos[0]>500+i*200 and 300>mouse_pos[1]>0:
                        if click[0]==1:
                            player.play_card(player.hand[i])
            except Exception as e:
                print(e)
        for i in range(min(3,len(player.hand)-3)):
            try:
                S.blit(player.hand[i+3].sprite,(500+i*200,300))
                if player.mana<player.hand[i+3].level:
                    S.blit(bcardsprite,(500+i*200,300))
                else:
                    if 700+i*200>mouse_pos[0]>500+i*200 and 600>mouse_pos[1]>300:
                        if click[0]==1:
                            player.play_card(player.hand[i+3])
            except Exception as e:
                print(e)
        pygame.draw.rect(S,(155,155,155),(1100,500,100,100))
        pygame.draw.rect(S,(255,255,255),(1100,500,100,100),5)
        if 1200>mouse_pos[0]>1100 and 600>mouse_pos[1]>500:
            pygame.draw.circle(S,(255,0,0),(1150,550),40,5)
            if click[0]==1:
                team_going=0
        else:
            pygame.draw.circle(S,(255,255,255),(1150,550),40,5)
        if player.hp>0:
            pygame.draw.rect(S,(255-player.hp/player.maxhp*255,player.hp/player.maxhp*255,0),(1105,500-player.hp/player.maxhp*200,20,player.hp/player.maxhp*200))
            if total_in_damage>0:
                pygame.draw.rect(S,(255,255,0),(1105,max(1,500-total_in_damage/player.maxhp*200),20,total_in_damage/player.maxhp*200))
                tsprite=produce("Times New Roman",15,str(total_in_damage),(0,0,0))
                S.blit(tsprite,(1115-tsprite.get_width()/2,500-total_in_damage/player.maxhp*200))
            pygame.draw.rect(S,(155,200,200),(1105,500-player.block/player.maxhp*200,20,player.block/player.maxhp*200))
            tsprite=produce("Times New Roman",15,str(player.hp)+"/"+str(player.maxhp),(255,255,255))
            S.blit(tsprite,(1167-tsprite.get_width()/2,480))
            tsprite=produce("Times New Roman",15,"Energy:",(255,255,255))
            S.blit(tsprite,(1167-tsprite.get_width()/2,450))
            tsprite=produce("Times New Roman",15,str(player.mana),(255,255,255))
            S.blit(tsprite,(1167-tsprite.get_width()/2,465))
            tsprite=produce("Times New Roman",15,"extra",(255,255,255))
            S.blit(tsprite,(1167-tsprite.get_width()/2,405))
            tsprite=produce("Times New Roman",15,"cards:",(255,255,255))
            S.blit(tsprite,(1167-tsprite.get_width()/2,420))
            tsprite=produce("Times New Roman",15,str(max(0,len(player.hand)-6)),(255,255,255))
            S.blit(tsprite,(1167-tsprite.get_width()/2,435))
            if player.block>0:
                tsprite=produce("Times New Roman",15,str(player.block),(0,0,255))
                S.blit(tsprite,(1115-tsprite.get_width()/2,max(0,500-player.block/player.maxhp*200)))
    elif menu=="LootScreen":
        S.fill((25,55,55))                                                                                    
        reward_pool=randint(1,5)+int((level+2)*difficulty_bonuses[difficulty_bonus])*5
        top3=[[0,Card(unlocks,[player.max_mana,achs])],[0,Card(unlocks,[player.max_mana,achs])],[0,Card(unlocks,[player.max_mana,achs])]]
        for i in range(int(7*(reward_q**2))):
            draftable=Card(unlocks,[player.max_mana,achs])
            for i in range(3):
                if draftable.G_power>top3[i][0]:
                    top3[i]=[draftable.G_power,draftable]
                    break
        player.draft(True,[top3[i][1] for i in range(3)])
        player.gold+=reward_pool
        player.hp=min(player.hp+10,player.maxhp)
        menu="Choosing where to go"
    elif menu=="Shop":
        S.fill((0,125,0))
        
    win.blit(pygame.transform.scale(S,win.get_size()),(0,0))
    clock.tick(100)
    pygame.display.update()
S.fill((0,0,0))
death_messages=[]
file=open("Assets\death_messages.txt","r")
for i in file:
    death_messages.append(i[:-1])
file.close()
tsprite=produce("Gabriola",60,choice(death_messages),(255,0,0))
S.blit(tsprite,(600-tsprite.get_width()/2,270))
while run: # death screen
    eventall()
    win.blit(pygame.transform.scale(S,win.get_size()),(0,0))
    clock.tick(100)
    pygame.display.update()
pygame.quit()
