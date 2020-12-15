import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import randint, choice
from numpy import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox

import utilityFunctions as uf
import SettlementMap as sm

# can be of any length given two points, but currently only works with fixed width of 3 or 4
class Ship:
    def __init__(self, level, start, end, materials, width=3, direction='z'):
        self.level = level
        self.start = start # tip
        self.end = end
        self.pole_length = 10
        self.materials = materials
        self.width = width # size of boat/ship can be changed
        self.direction = direction # default facing north direction

        # post process - for z direction, start z > end z or else switch values for start and end
        # for x direction, start x < start x
        if (direction == 'z' and start[2] < end[2]) or (direction == 'x' and start[0] > end[0]):
            self.start, self.end = self.end, self.start
     
        

        self.x, self.y, self.z = self.start
    def build(self):
        # ship in z direction - build with east/west stairs
        # x direction build with north/south
        # build base
        # upside down stairs, slabs, planks
        self._build_base()

        # build sails
        # logs, wool for sails
        self._build_sails()

        # optional: boathouse vs non-boathouse

        pass
    def _build_base(self):
        east, west, south, north = self.materials['top_stairs']
        east2, west2, south2, north2 = self.materials['bot_stairs']
        log = self.materials['log']
        plank = self.materials['plank']
        slab = self.materials['slab']
        fence = self.materials['fence']
        x1,y1,z1 = self.start
        x2,y2,z2 = self.end
        floor_width = (self.width-1) * 2 + 1 - 2 # exclude side walls of ship from floor width
        w = 0
        if self.direction == 'z':
            self.length = abs(z1-z2)
            
            # hull shape
            # front hull
            uf.setBlock(self.level,south,x1,y1,z1)
            uf.setBlock(self.level,south2,x1,y1,z1-1)
            # underbelly part
            uf.setBlock(self.level,plank,x1,y1-1,z1-1)
            uf.setBlock(self.level,north,x1,y1-2,z1-1)
            uf.setBlock(self.level,plank,x1,y1-2,z1-2)
            
            
            for w in range(1,self.width):
                for i in range(abs((x1+w)-(x1-w))+1):
                    uf.setBlock(self.level,slab,x1+w-i,y1,z1-w)
                
                # frame 
                uf.setBlock(self.level,plank,x1+w,y1,z1-w)
                uf.setBlock(self.level,plank,x1-w,y1,z1-w)
                # underbelly part
                uf.setBlock(self.level,plank,x1+w,y1-1,z1-w)
                uf.setBlock(self.level,plank,x1-w,y1-1,z1-w)
                uf.setBlock(self.level,plank,x1+w-1,y1-2,z1-w)
                uf.setBlock(self.level,plank,x1-w+1,y1-2,z1-w)
                uf.setBlock(self.level,plank,x1-w+1,y1-2,z1-w)

                # if w < self.width-1:
                #     uf.setBlock(self.level,plank,x1-w,y1-1,z1-1)
                #     uf.setBlock(self.level,plank,x1+w,y1-1,z1-1)
                
            # floor/walking area
            for z in range(self.length-self.width): # don't include length of the tips
                # side walls of ship
                uf.setBlock(self.level,plank,x1+w,y1,z1-w-z)
                uf.setBlock(self.level,plank,x1-w,y1,z1-w-z)

                # building floor in x direction
                for floor in range(1, floor_width+1):
                    uf.setBlock(self.level,slab,x1+w-floor,y1,z1-w-z)
                    # underbelly
                    uf.setBlock(self.level,slab,x1+w-floor,y1-2,z1-w-z)

                # underbelly of ship 
                # sides are stair blocks
                uf.setBlock(self.level,west,x1+w,y1-1,z1-w-z) 
                uf.setBlock(self.level,east,x1-w,y1-1,z1-w-z)
                uf.setBlock(self.level,west,x1+w-1,y1-2,z1-w-z) 
                uf.setBlock(self.level,east,x1-w+1,y1-2,z1-w-z)

            # raise pole here
            self.pole_start = (x1,y1,z1-self.width) 

            for h in range(self.pole_length):
                uf.setBlock(self.level,log,x1,y1+h,z1-self.width)  

            uf.setBlock(self.level,fence,x1,y1+h+1,z1-self.width) 
            self.pole_end = (x1,y1+h,z1-self.width)

            # back hull (reverse front hull pattern)
            uf.setBlock(self.level,north,x2,y2,z2)
            uf.setBlock(self.level,north2,x2,y2,z2+1)
            # underbelly part
            uf.setBlock(self.level,plank,x2,y2-1,z2+1)
            uf.setBlock(self.level,south,x2,y2-2,z2+1)

            for w in range(self.width-1, 0, -1):
                # frame
                uf.setBlock(self.level,plank,x2+w,y2,z2+w)
                uf.setBlock(self.level,plank,x2-w,y2,z2+w)  
                # underbelly part 
                uf.setBlock(self.level,plank,x2+w,y2-1,z2+w)
                uf.setBlock(self.level,plank,x2-w,y2-1,z2+w)
                uf.setBlock(self.level,plank,x2+w-1,y2-2,z2+w)
                uf.setBlock(self.level,plank,x2-w+1,y2-2,z2+w)
                uf.setBlock(self.level,plank,x2-w+1,y2-2,z2+w)
                # if w < self.width-1:
                #     uf.setBlock(self.level,plank,x2-w,y2-1,z2+1)
                #     uf.setBlock(self.level,plank,x2+w,y2-1,z2+1)
            
        else:
            self.length = abs(x1-x2)
            # z direction
            # hull shape
            # front hull
            uf.setBlock(self.level,west,x1,y1,z1)
            uf.setBlock(self.level,west2,x1+1,y1,z1)
            # underbelly part
            uf.setBlock(self.level,plank,x1+1,y1-1,z1)
            uf.setBlock(self.level,east,x1+1,y1-2,z1)
     
            for w in range(1,self.width):
                # fill in middle floor
                for i in range(abs((z1+w)-(z1-w))+1):
                    uf.setBlock(self.level,slab,x1+w,y1,z1+w-i)
                # frame    
                uf.setBlock(self.level,plank,x1+w,y1,z1+w)
                uf.setBlock(self.level,plank,x1+w,y1,z1-w)

                # underbelly
                uf.setBlock(self.level,plank,x1+w,y1-1,z1+w)
                uf.setBlock(self.level,plank,x1+w,y1-1,z1-w)
                uf.setBlock(self.level,plank,x1+w,y1-2,z1+w-1)
                uf.setBlock(self.level,plank,x1+w,y1-2,z1-w+1)
                uf.setBlock(self.level,plank,x1+w,y1-2,z1-w+2)
                
                # underbelly part
                # if w < self.width-1:
                #     uf.setBlock(self.level,plank,x1+1,y1-1,z1-w)
                #     uf.setBlock(self.level,plank,x1+1,y1-1,z1+w)
            
            # floor/walking area
            for z in range(self.length-self.width): # don't include length of the tips
                # side walls of ship
                uf.setBlock(self.level,plank,x1+w+z,y1,z1+w)
                uf.setBlock(self.level,plank,x1+w+z,y1,z1-w)

                # building floor in x direction
                for floor in range(1, floor_width+1):
                    uf.setBlock(self.level,slab,x1+w+z,y1,z1+w-floor)
                    # underbelly
                    uf.setBlock(self.level,slab,x1+w+z,y1-2,z1+w-floor)

                # underbelly of ship 
                # sides are stair blocks
                uf.setBlock(self.level,north,x1+w+z,y1-1,z1+w) 
                uf.setBlock(self.level,south,x1+w+z,y1-1,z1-w)
                uf.setBlock(self.level,north,x1+w+z,y1-2,z1+w-1) 
                uf.setBlock(self.level,south,x1+w+z,y1-2,z1-w+1)
                

            # raise pole here
            self.pole_start = (x1+self.width,y1,z1) 

            for h in range(self.pole_length):
                uf.setBlock(self.level,log,x1+self.width,y1+h,z1)  
                
            uf.setBlock(self.level,fence,x1+self.width,y1+h+1,z1)
            self.pole_end = (x1+self.width,y1+h,z1)

            # back hull (reverse front hull pattern)
            uf.setBlock(self.level,east,x2,y2,z2)
            uf.setBlock(self.level,east2,x2-1,y2,z2)
            # underbelly part
            uf.setBlock(self.level,plank,x2-1,y2-1,z2)
            uf.setBlock(self.level,west,x2-1,y2-2,z2)

            for w in range(self.width-1, 0, -1):
                # fill in middle floor
                for i in range(abs((z1+w)-(z1-w))):
                    uf.setBlock(self.level,slab,x2-w,y2,z2+w-i)
                # frame
                uf.setBlock(self.level,plank,x2-w,y2,z2+w)
                uf.setBlock(self.level,plank,x2-w,y2,z2-w) 

                # underbelly
                uf.setBlock(self.level,plank,x2-w,y2-1,z2+w)
                uf.setBlock(self.level,plank,x2-w,y2-1,z2-w)
                uf.setBlock(self.level,plank,x2-w,y2-2,z2+w-1)
                uf.setBlock(self.level,plank,x2-w,y2-2,z2-w+1) 
                # underbelly part 
                # if w < self.width-1:
                #     uf.setBlock(self.level,plank,x2-1,y2-1,z2-w)
                #     uf.setBlock(self.level,plank,x2-1,y2-1,z2+w)

    def _build_sails(self):
        # pole
        wool = self.materials['wool']
        # wool for sails
        x1,y1,z1 = self.pole_start 
        x2,y2,z2 = self.pole_end
        length = abs(y1-y2)

        if self.direction == 'z':
            # wool that is of roughly of length tall and with a width of self.width + 1
            # only top and bottom of sail
            for l in range(2, length):
                if l == 2 or l == length -1:
                    for w in range((self.width + 1) // 2 + 1):
                        uf.setBlock(self.level,wool,x1,y1+l,z1-1)
                        uf.setBlock(self.level,wool,x1+w,y1+l,z1-1)
                        uf.setBlock(self.level,wool,x1-w,y1+l,z1-1)

            # add curavature of sails
            for l in range(3, length-1):
                for w in range((self.width + 1) // 2 + 1):
                    uf.setBlock(self.level,wool,x1+w,y1+l,z1-2)
                    uf.setBlock(self.level,wool,x1-w,y1+l,z1-2)
        else:
            # wool that is of roughly of length tall and with a width of self.width + 1
            # only top and bottom of sail
            for l in range(2, length):
                if l == 2 or l == length -1:
                    for w in range((self.width + 1) // 2 + 1):
                        uf.setBlock(self.level,wool,x1+1,y1+l,z1)
                        uf.setBlock(self.level,wool,x1+1,y1+l,z1+w)
                        uf.setBlock(self.level,wool,x1+1,y1+l,z1-w)

            # add curavature of sails
            for l in range(3, length-1):
                for w in range((self.width + 1) // 2 + 1):
                    uf.setBlock(self.level,wool,x1+2,y1+l,z1+w)
                    uf.setBlock(self.level,wool,x1+2,y1+l,z1-w)



