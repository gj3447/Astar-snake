import pygame as pg
import random
import time

class Map:
    def __init__(self,x,y,box_size):
        self.screen = pg.display.set_mode
        self.screen = pg.display.set_mode
        self.x = x
        self.y = y
        self.box_size = box_size
        self.screen = pg.display.set_mode([self.box_size * (x+int(1)), self.box_size * (y+int(1))])
        self.node = [[Node(x=row,y=col) for col in range(self.x)] for row in range(self.y)]
        self.food = Food(map=self)
        self.snake = Snake(x=int(0),y=int(0),map=self)
        self.snake.waycreate()
        self.display()
        self.stop = False

    def update(self):
        if self.stop:
            return
        if (self.snake.move()):
            self.stop = True
        self.display()
    def display(self,openway=None,closeway=None,currentway=None):
        self.screen.fill((0,0,0))

        if not(openway==None):
            for e in openway:
                block = pg.Rect((e.node.x*self.box_size, e.node.y*self.box_size), (self.box_size, self.box_size))
                pg.draw.rect(self.screen, (0,0,100), block)
        
        if not(closeway==None):
            for e in closeway:
                block = pg.Rect((e.node.x*self.box_size, e.node.y*self.box_size), (self.box_size, self.box_size))
                pg.draw.rect(self.screen, (50,50,50), block)
        
        if not(currentway==None):
            block = pg.Rect((currentway.node.x*self.box_size, currentway.node.y*self.box_size), (self.box_size, self.box_size))
            pg.draw.rect(self.screen, (255,0,0), block)
        self.snake.draw()
        self.food.draw()
        pg.display.flip()
    def inside(self,x,y):
        if self.x<=x:
            return False
        if x<0:
            return False
        if self.y<=y:
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
        for col in range(self.map.x):
            for row in range(self.map.y):
                currentnode = self.map.node[col][row]
                if currentnode.value == int(0):
                    nodearray.append(currentnode)
        currentnode = nodearray[random.randrange(0,len(nodearray))]
        self.x = currentnode.x
        self.y = currentnode.y
    def inside(self,x,y):
        if self.x != x:
            return False
        if self.y !=y:
            return False
        return True
    def distance(self,x,y):
        return(abs(x-self.x)+abs(y-self.y))
    def string(self):
        return ('vector:' +str(self.x)+','+ str(self.y))
    def draw(self):
        block = pg.Rect((self.x*self.map.box_size, self.y*self.map.box_size), (self.map.box_size, self.map.box_size))
        pg.draw.rect(self.map.screen, (255,0,0), block)
class Snake:
    def __init__(self,x,y,map):
        self.life = int(1)
        self.x = x
        self.y = y
        self.map = map
        self.tail = []
        self.way = None
        self.tailcreate()
    def move(self):
        if not (self.way.nextway == None):
            self.way = self.way.nextway
            self.tailremove()
            self.tailcreate()
        else:
            self.life +=int(1)
            self.map.food.replace()
            if self.waycreate():
                print("긴급종료")
                return True
            self.way = self.way.nextway
            self.tailcreate()
    def tailcreate(self):
        if not(self.way ==None):
            self.x = self.way.node.x
            self.y = self.way.node.y
        if self.map.inside(x=self.x,y=self.y) :
            currentnode = self.map.node[self.x][self.y]
            currentnode.value = self.life
            if self.tail.__contains__(currentnode) == False:
                self.tail.append(currentnode)
    def tailremove(self):
        remove = None
        for e in self.tail:
            e.value =e.value- int(1)
            if e.value ==0:
                remove = e
        if not (remove == None):
            self.tail.remove(remove)
    def draw(self):
        for e in self.tail:
            block = pg.Rect((e.x*self.map.box_size, e.y*self.map.box_size), (self.map.box_size, self.map.box_size))
            pg.draw.rect(self.map.screen, (255,255,255), block)
    def waycreate(self):
        self.way = Way(map=self.map,node=self.map.node[self.x][self.y],count=0)
        wayarray = []
        wayarray.append(self.way)
        wayclose =[]
        while len(wayarray)<100000:
            min = None
            if len(wayarray) ==0:
                return True
            for e in wayarray:
                if min ==None:
                    min = e
                else:
                    if min.value == e.value:
                        if min.distance >e.distance:
                            min = e
                    if min.value> e.value:
                        min = e
            expandarray = min.expand()
            if not (min.backway==None):
                min.backway.nextway = min
            printstring ='list'
            for e in wayarray:
                printstring += " "+str(e.distance)
            wayarray.remove(min)
            wayclose.append(min)
            wayarray.extend(expandarray)
            self.map.display(currentway=min,openway=expandarray,closeway=wayclose)
            print(e.value,end='')
            if self.map.food.inside(min.node.x,min.node.y):
                break

class Node:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.node = None
        self.value = int(0)
class Way:
    def string(self):
        return '['+str(self.node.x)+','+str(self.node.y)+'] C'+str(self.count)+' D'+str(self.distance)+' V'+str(self.value)
    def __init__(self,map,node,count):
        self.node = node
        self.map = map
        self.count = count
        self.backway = None
        self.nextway = None
        self.distance = map.food.distance(x=node.x,y=node.y)
        self.value = self.distance+count
    def expand(self):
        x= self.node.x
        y = self.node.y
        count = self.count+1
        vectorarray = [[x+1,y],[x-1,y],[x,y+1],[x,y-1]]
        nodearray = []
        tailwayarray = []
        result = []
        tailway= self
        for e in range(self.map.snake.life-1):
            if tailway.backway==None:
                break;
            else:
                tailway = self.backway
                tailwayarray.append(tailway)
        for e in vectorarray:
            if self.map.possible(x=e[0],y=e[1],count=self.count):
                nodearray.append(self.map.node[e[0]][e[1]])
        for e in tailwayarray:
            remove = None
            for a in nodearray:
                if a == tailway.node:
                    remove = a
                    break
            if not remove == None:
                nodearray.remove(remove)
        for e in nodearray:
            newway = Way(map=self.map,node=e,count=count)
            newway.backway = self
            result.append(newway)
        return result

if __name__ == "__main__":
    time_ = int(1)
    map_ = Map(x = 10 , y = 10 ,box_size=50)

    end_ = False
    while not end_:
        time.sleep(0.05)
        map_.update()
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key ==pg.K_ESCAPE:
                    end_ = True