import time
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import randint
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

import SettlementMap as sm
import utilityFunctions as uf
from collections import defaultdict
from Ship import Ship

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
    start_time = time.time()
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
    print('################### Print bodies of water that are above minimum threshold ##############################')
    threshold = 1000
    for body, count in bodies.items():
        if count > threshold:
            print(body, count)
    
    print('Finding water bodies took ' + str(time.time() - start_time) + ' seconds')

    print('Finding points for ship generation')
    add_ships(level,box,bodies,water_blocks)


def add_ships(level, box, bodies, water_blocks):
    materials = {
		'plank': (5,0),
		'log': (17,0),
		'slab': (126,0),
		'top_stairs': [(53,4),(53,5),(53,6),(53,7)],
		'bot_stairs':[(53,0),(53,1),(53,2),(53,3)],
		'wool': (35,0),
		'fence': (85,0)
	}

    threshold = 1000
    for body, count in bodies.items():
        if count >= threshold:
            offset = 10
            length = random.randint(10,15)
            len_directions = [(-length, 0, 0), (length, 0, 0), (0, 0, -length), (0, 0, length)]
            offset_directions = [(-offset, 0, 0), (offset, 0, 0), (0, 0, -offset), (0, 0, offset), (-offset, 0, -offset), (-offset, 0, offset), (offset, 0, offset),(offset, 0, -offset)]

            start_points = find_water_points(level,box,offset_directions, body)
            coords = {}
            
            # generate possible end points for each startpoint
            for start in start_points:
                end_points = find_water_points(level,box,len_directions, start)
                coords[start] = end_points

            while not start_points:
                # use a smaller offset
                offset_directions = [(-offset // 2, 0, 0), (offset // 2, 0, 0), (0, 0, -offset //2), (0, 0, offset//2), (-offset//2, 0, -offset//2), (-offset//2, 0, offset//2), (offset//2, 0, offset//2),(offset//2, 0, -offset//2)]
                start_points = find_water_points(level,box,offset_directions, body)
                #start_points.append(body)

            start_index = 0

            # pick random start point if len(startpoints) > 1
            if len(start_points) > 1:
                start_index = random.randint(0, len(start_points) - 1)
            
            start = start_points[start_index]

            for end in coords[start]:
                # if x is the same, ship is in z direction
                if end[0] == start[0]:
                    
                    print('Using these points: {0}, {1}'.format(start, end))
                    # start z has to be bigger than end z
                    # increase altitude by 1
                    s = Ship(level, (start[0],start[1]+1,start[2]), (end[0],end[1]+1,end[2]), materials)
                    s.build()
                    break
                # else it's in x direction
                elif end[2] == start[2]:
                    print('Using these points: {0}, {1}'.format(start, end))
                    s = Ship(level, (start[0],start[1]+1,start[2]), (end[0],end[1]+1,end[2]), materials, 3, 'x')
                    s.build()
                    break


def find_water_points(level, box, directions, point):
    points = []
    for d in directions:
        x1,y1,z1 = (point[0]+d[0],point[1]+d[1],point[2]+d[2])
        if (sm.get_block(level,x1,y1,z1) == 8 or sm.get_block(level,x1,y1,z1) == 9) and isValid(x1,y1,z1,box) :
            points.append((x1,y1,z1))
    return points

