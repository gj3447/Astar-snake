import pygame as pg
import random
import time
import parameter as pm
import numpy as np
class World:
    def __init__(self):
        pg.init()
        self.mapmatrix = [[Map(x=row,y=col,world=self)for col in range(pm.map_count_x)]for row in range(pm.map_count_y)]
        self.maparray = []
        self.screen = pg.display.set_mode([int(pm.map_count_x*pm.map_size_x*pm.box_size)+int(500),int(pm.map_count_y*pm.map_size_y*pm.box_size)])
        self.font = pg.font.SysFont("arial",pm.font_size,True,True)
        for e in self.mapmatrix:
            for a in e:
                self.maparray.append(a)
        self.find_mean = int(0)
        self.count_mean = int(0)
        self.distance_mean = int(0)
        self.find_std = int(0)
        self.count_std = int(0)
        self.distance_std = int(0)
        self.generic_count = int(0)
        self.valuescore()
        self.draw()
        self.update()
    def valuescore(self):
        find =[]
        count =[]
        distance = []
        for e in self.maparray:
            find.append(e.genericfind)
            count.append(e.genericcount)
            distance.append(e.genericdistance)
        self.find_mean = np.array(find).mean()
        self.count_mean = np.array(count).mean()
        self.distance_mean =np.array(distance).mean()
        self.find_std = np.array(find).std()
        self.count_std = np.array(count).std()
        self.distance_std = np.array(distance).std()
    def start(self):
        for e in range(pm.map_update_count):
            self.updatemap(count=e)
            self.draw(count=e)
    def update(self):
        while True :
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key ==pg.K_ESCAPE:
                        return
                    if event.key ==pg.K_s:
                        self.start()
                    if event.key == pg.K_d:
                        self.generic()
    def updatemap(self,count = 0):
        for e in self.maparray:
            e.update()
        self.drawscore()
    def drawscore(self,count=int(0)):
        x = pm.map_count_x*  pm.map_size_x*pm.box_size
        life_score = int(0)
        for e in self.maparray:
            life_score += e.snake.life
        self.screen.blit(self.font.render("life_score : "+str(life_score),False,(255,255,255)),(x,0))
        self.screen.blit(self.font.render("find_value : "+str(self.find_mean)+" | "+str(self.find_std),False,(255,255,255)),(x,pm.font_size*1))
        self.screen.blit(self.font.render("count_value : "+str(self.count_mean)+" | "+str(self.count_std),False,(255,255,255)),(x,pm.font_size*2))
        self.screen.blit(self.font.render("distance_value : "+str(self.distance_mean)+" | "+str(self.distance_std),False,(255,255,255)),(x,pm.font_size*3))
        self.screen.blit(self.font.render("generic_count : "+str(self.generic_count),False,(255,255,255)),(x,pm.font_size*4))
        self.screen.blit(self.font.render("update_count : "+str(count),False,(255,255,255)),(x,pm.font_size*5))
    def generic(self):
        self.generic_count +=int(1)
        for e in self.maparray:
            e.generic(map1=self.mapgatcha(),map2=self.mapgatcha())
        for e in self.maparray:
            e.restart()
        self.valuescore()
        self.draw()
    def mapgatcha(self):
        sum = int(0)
        for e in self.maparray:
            sum +=e.snake.life**2
        gatcha = random.randrange(0,sum)
        for e in self.maparray:
            gatcha -=e.snake.life**2
            if gatcha<=0:
                return e
        return self.maparray[-1]
    def draw(self,count = int(0)):
        self.screen.fill((0,0,0))
        for e in self.maparray:
            e.draw()
        self.drawscore(count)
        pg.display.flip()
class Map:
    def __init__(self,x,y,world):
        self.genericfind = random.uniform(pm.snake_gerneric_min,pm.snake_gerneric_max)
        self.genericcount = random.uniform(pm.snake_gerneric_min,pm.snake_gerneric_max)
        self.genericdistance = random.uniform(pm.snake_gerneric_min,pm.snake_gerneric_max)
        self.genericfindbuffer = float(0)
        self.genericcountbuffer = float(0)
        self.genericdistancebuffer = float(0)
        self.world = world
        self.x = x
        self.y = y
        self.node = [[Node(x=row,y=col) for col in range(pm.map_size_x)] for row in range(pm.map_size_y)]
        self.food = Food(map=self)
        self.snake = Snake(x=random.randrange(0,pm.map_size_x),y=random.randrange(0,pm.map_size_y),map=self)
        self.stop = False
    def generic(self,map1,map2):
        self.genericfindbuffer = random.uniform(map1.genericfind,map2.genericfind)
        self.genericcountbuffer = random.uniform(map1.genericcount,map2.genericcount)
        self.genericdistancebuffer = random.uniform(map1.genericdistance,map2.genericdistance)
    def restart(self):
        self.genericfind = self.genericfindbuffer
        self.genericcount = self.genericcountbuffer
        self.genericdistance = self.genericdistancebuffer
        self.food = Food(map=self)
        self.snake = Snake(x=random.randrange(0,pm.map_size_x),y=random.randrange(0,pm.map_size_y),map=self)
        self.nodereset(value=True)
        self.stop = False
    def nodereset(self,find = True,value = False):
        for e in self.node:
            for a in e:
                if find :
                    a.find = int(0)
                if value:
                    a.value = int(0)
    def drawbox(self,x,y,color):
        position_x = (self.x*pm.map_size_x + x)*pm.box_size
        position_y = (self.y*pm.map_size_y + y)*pm.box_size
        block = pg.Rect((position_x, position_y),(pm.box_size, pm.box_size))
        pg.draw.rect(self.world.screen,color,block)
    def update(self):
        if self.stop:
            return
        if (self.snake.update()):
            self.stop = True
    def draw(self):
        self.snake.draw()
        self.food.draw()
    def inside(self,x,y):
        if pm.map_size_x<=x:
            return False
        if x<0:
            return False
        if pm.map_size_y<=y:
            return False
        if y<0:
            return False
        return True
    def possible(self, x ,y,count):
        if self.inside(x=x, y=y)==False:
            return False
        if self.node[x][y].value>count:
            return False
        else:
            return True

class Food:
    def __init__(self,map):                             
        self.map = map
        self.x = 0
        self.y = 0
        self.replace()
    def replace(self):
        nodearray = []
        for col in range(pm.map_size_x):
            for row in range(pm.map_size_y):
                currentnode = self.map.node[col][row]
                if currentnode.value == int(0):
                    nodearray.append(currentnode)
        currentnode = nodearray[random.randrange(0,len(nodearray))]
        self.x = currentnode.x
        self.y = currentnode.y
    def inside(self,x,y):
        if self.y ==y and self.x == x:
            return True
        else :
            return False
    def distance(self,x,y):
        return (abs(x-self.x)+abs(y-self.y))
    def string(self):
        return ('vector:' +str(self.x)+','+ str(self.y))
    def draw(self):
        self.map.drawbox(x=self.x,y=self.y,color=(255,0,0))

class Snake:
    def __init__(self,x,y,map):
        self.life = int(0)
        self.energy = int(0)
        self.map = map
        self.way = Way(map=map,node=map.node[x][y],count=0)
        self.state = 'move'
        self.findway = None
        self.openway = []
        self.closeway = []
        self.expandway = []
    def update(self):
        self.energy += pm.snake_energy
        while self.energy>0:
            if self.state == 'find':
                if self.find():
                    return True
            elif self.state == 'move':
                if self.move():
                    return True
        return False
    def move(self):
        if self.way.nextway == None:
            self.life +=int(1)
            self.way.node.value = self.life
            self.map.food.replace()
            self.findchange()
            return False
        else:
            tail = self.way.list(length=self.life)
            self.way = self.way.nextway
            self.way.node.value = self.life
            self.energy -= pm.snake_move_energy
            for e in tail:
                if e.node.value > int(0):
                    e.node.value -=int(1)
                else:
                    e.remove()
            return False
    def find(self):
        if len(self.openway)>0:
            self.findway = self.openway[0]
            for e in self.openway:
                if e.value < self.findway.value:
                    self.findway= e
            self.closeway.append(self.findway)
            self.openway.remove(self.findway)
            if self.map.food.inside(x=self.findway.node.x,y=self.findway.node.y):
                self.movechange()
            else:
                self.energy -= pm.snake_find_energy
                self.expandway = self.findway.expand()
                self.openway.extend(self.expandway)
            return False
        else:
            return True

    def movechange(self):
        self.state = 'move'
        self.findway.nextset(endway = self.way)
        self.openway.clear()
        self.closeway.clear()
    def findchange(self):
        self.state = 'find'
        self.way.reset()
        self.findway = self.way
        self.openway.append(self.findway)
        self.map.nodereset()
    def draw(self):
        tail = self.way.list(length=self.life)
        for e in tail:
            value = int(1)
            if self.life >0:
                value = 100*e.node.value/self.life+100
            self.map.drawbox(color=(value,value,value),x=e.node.x ,y=e.node.y)
        if self.state =='find':
            if not(self.findway ==None):
                findway = self.findway.list(endway=self.way)
                for e in findway:
                    self.map.drawbox(color=(0,255,0),x=e.node.x, y=e.node.y)
            for e in self.expandway:
                self.map.drawbox(color=(0,0,255),x=e.node.x,y=e.node.y)
        self.map.drawbox(color=(255,255,255),x=self.way.node.x,y=self.way.node.y)

class Node:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.node = None
        self.value = int(0)
        self.find = int(0)
class Way:
    def string(self):
        return '['+str(self.node.x)+','+str(self.node.y)+']'
    def __init__(self,map,node,count):
        self.node = node
        self.map = map
        self.count = count
        self.backway = None
        self.nextway = None
        self.distance = map.food.distance(x=node.x,y=node.y)
        self.value = self.distance * self.map.genericdistance +count*self.map.genericcount + node.find*self.map.genericfind
        node.find +=int(1)
    def reset(self):
        self.count = 0
        self.value = self.distance * self.map.genericdistance +self.count*self.map.genericcount + self.node.find*self.map.genericfind
    def list(self,length=int(10000),endway=None):
        result = []
        currentway = self
        result.append(currentway)
        for e in range(length):
            if currentway.backway==None:
                break
            elif currentway == endway:
                break
            else:
                currentway = currentway.backway
                result.append(currentway)
        result.append(currentway)
        return result
    def expand(self):
        x= self.node.x
        y = self.node.y
        count = self.count+1
        vectorarray = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
        nodearray = []
        tailway = self.list(length = self.map.snake.life)
        result = []
        self.node.find += int(1)
        for e in vectorarray:
            if self.map.possible(x=e[0],y=e[1],count=self.count):
                nodearray.append(self.map.node[e[0]][e[1]])
        for e in tailway:
            remove = None
            for a in nodearray:
                if a==e.node:
                    remove = a
                    break
            if not remove == None:
                nodearray.remove(remove)
        for e in nodearray:
            newway = Way(map=self.map,node=e,count=count)
            newway.backway = self
            result.append(newway)
        
        return result
    def nextset(self, endway = None):
        currentway = self
        while not (currentway.backway ==None):
            currentway.backway.nextway = currentway
            currentway = currentway.backway
    def remove(self):
        if not(self.nextway ==None):
            self.nextway.backway = None
        self.nextway = None
        self.backway = None

if __name__ == "__main__":
    world = World()