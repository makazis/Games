from random import *
from math import *
import pygame
pygame.init()
card_font=pygame.font.SysFont('Times New Roman',20)
rarities=[
    'Common',
    'Uncommon',
    'Rare',
    'Super Rare',
    'Ultra Rare',

    'Golden',
    'Platinum',
    'Diamond',
    'Mythical',
    'Legendary'
    ]
rarity_colors=[
    [55,55,55],
    [0,125,0],
    [0,125,125],
    [125,65,0],
    [125,0,65],

    [125,105,0],
    [55,155,155],
    [155,155,155],
    [50,0,100],
    [0,0,0],
    ]
Effect_names=[
    ['Deal ',' Damage'],
    ['Gain ',' Block'],
    ['Draw ',' Cards'],
    ['Lose ',' HP'],
    ['Gain ' ,' Energy'],
    ['Gain ',' Strength'],
    ['Gain ',' Dexterity'],
    ["Get ",' Anger Aura'],
    ["Get ",' Speed Aura'],
    ["Get ",' Thorns']
    ]
Seffect_names=[
    "Vanish"
    ]
mutagen_cost=       [1,1,7,-3,7,7,6,13,8,4]
mutagen_probability=[1,1,5,7 ,4,3,3,5,5,4]

Smutagen_cost=[8]
card_back_sprites=[pygame.image.load("Assets\\Card Backs\\"+i+".png") for i in ["Common","Uncommon","Rare","Super Rare","Ultra Rare","Golden"]]
card_shape=pygame.image.load("Assets\\Card Backs\\Card Shape.png")
class Card:
    def __init__(self,fold,data):
        self.level=randint(1,data[0])
        self.rarity=-1 # starts at -1
        c=0
        while c==0 and -9<self.rarity<9:
            c=randint(0,4) # usually is at 0,4
            self.rarity+=1
        self.mutagen=10*self.level+self.rarity*(self.level+1)
        self.G_power=self.mutagen*(self.rarity+1)/self.level
        if self.mutagen==0:
            self.mutagen+=1
        self.data=[0 for i in range(5)]
        c=[i for i in range(5)]
        for i in range(len(data[1])):
            if data[1][i]==1:
                c.append(i+5)
        self.effects=[]
        for i in range(randint(1,randint(2,5))):
            self.effects.append(choice(c))
            c.remove(self.effects[-1])
        self.seffect=-1
        if randint(1,7)==1:
            self.seffect=randint(1,len(Seffect_names))-1
            self.mutagen+=Smutagen_cost[self.seffect]*(self.level+int(self.rarity/3))
        moves=0
        self.starting_mutagen=self.mutagen
        while self.mutagen>0 and moves<self.starting_mutagen*(self.level+1)+50:
            moves+=1
            effect=randint(1,len(self.effects))-1
            which=self.effects[effect]
            if randint(1,mutagen_probability[which])==1 and self.mutagen>=mutagen_cost[which]:
                self.data[effect]+=1
                self.mutagen-=mutagen_cost[which]
        self.sprite=pygame.Surface((200,300))
        self.sprite.fill(rarity_colors[self.rarity])
        if self.rarity<len(card_back_sprites):
            self.sprite.blit(card_back_sprites[self.rarity],(0,0))
        self.sprite.blit(card_font.render(str(self.level),1,(255,255,255)),(10,10))
        lines=-1
        for i in self.effects:
            if self.data[self.effects.index(i)]>0:
                lines+=1
                text=Effect_names[i][0]+str(self.data[self.effects.index(i)])+Effect_names[i][1]
                if self.rarity==5:
                    self.sprite.blit(card_font.render(text,1,(0,255,125)),(10,160+lines*20))
                else:
                    self.sprite.blit(card_font.render(text,1,(255,255,255)),(10,160+lines*20))
        if self.rarity==9:
            rsprite=card_font.render(rarities[self.rarity],1,(255,125,0))
            self.sprite.blit(rsprite,(100-rsprite.get_width()/2,277))
        elif self.rarity==3 or self.rarity==2:
            rsprite=card_font.render(rarities[self.rarity],1,(255,255,0))
            self.sprite.blit(rsprite,(100-rsprite.get_width()/2,277))
        else:
            rsprite=card_font.render(rarities[self.rarity],1,(0,0,0))
            self.sprite.blit(rsprite,(100-rsprite.get_width()/2,277))
        if self.seffect!=-1:
            rsprite=card_font.render(Seffect_names[self.seffect],1,(255,255,255))
            self.sprite.blit(rsprite,(100-rsprite.get_width()/2,260))
        self.sprite.blit(card_shape,(0,0))
        #print(self.effects)
        #print(self.data)
#card=[Card(1) for i in range(30)]
#card=Card(1,[3,[1,1,1]])
