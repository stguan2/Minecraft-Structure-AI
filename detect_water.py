import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import randint
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

from SettlementGenerator import Generator
import SettlementMap as sm
import utilityFunctions as uf
from collections import defaultdict

def isValid(x,y,z, box):
	return x >= box.minx and x <= box.maxx and y >= box.miny and y <= box.maxy and z >= box.minz and z <= box.maxz 

def dfs_iter(level,box, visited, x,y,z, bodies):
	stack = []
	directions = [(1,0,0),(-1,0,0),(0,0,1),(0,0,-1),(0,-1,0),(0,1,0)]
	stack.append((x,y,z))
	bodies[(x,y,z)] = 0
	blocks = 0
	while stack:
		water = stack.pop()
		if water in visited:
			continue
		
		visited[water] = 1
		blocks += 1
		for d in directions:
			x2,y2,z2 = water[0]+d[0],water[1]+d[1],water[2]+d[2]
			if not isValid(x2,y2,z2,box):
				continue
			if (x2,y2,z2) not in visited and (sm.get_block(level,x2,y2,z2) == 8 or sm.get_block(level,x2,y2,z2) == 9):
				stack.append((x2,y2,z2))

	bodies[(x,y,z)] = blocks


def perform(level, box, options):
    water_blocks = []
    visited = {}
    total_blocks = 0
    for x in xrange(box.minx, box.maxx):
        for z in xrange(box.minz, box.maxz):
            for y in xrange(box.maxy, box.miny, -1):
                total_blocks += 1
                if sm.get_block(level,x,y,z) == 8 or sm.get_block(level,x,y,z) == 9:
                    water_blocks.append((x,y,z))

    water_blocks.sort()
    bodies = {} # water coord : number of blocks 
    if water_blocks:
        for water in water_blocks:
            if water not in visited:
                dfs_iter(level,box,visited,water[0],water[1],water[2], bodies)

    # print the starting coord of the body of water along with the number blocks in that body
    print('Starting coords of water bodies in the map')
    for body, count in bodies.items():
        print(body, count)
    
    return bodies