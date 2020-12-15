import time # for timing
from math import sqrt, tan, sin, cos, pi, ceil, floor, acos, atan, asin, degrees, radians, log, atan2, acos, asin
from random import *
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox
from mcplatform import *

import SettlementMap as sm
import utilityFunctions as utilityFunctions
import detect_water as detectWater

inputs = (
	("Lighthouse", "label"),
	("Material", alphaMaterials.Stone), # the material we want to use to build the mass of the structures
	("Creator: Steven Guan", "label"),
	)
    
def perform(level, box, options):
    bodies = detectWater.perform(level, box, {})
    print bodies
    radius = 5
    for i in bodies:
        if bodies[i] > 1000:
            tmpx = i[0]+random.randint(-10,10)
            tmpz = i[2]+random.randint(-10,10)
            chk = 0
            bool_chk = True
            while bool_chk == True:
                bool_chk = False
                
                # Check if base will generate on water
                for j in range(tmpx-radius-2, tmpx+radius+3):
                    for k in range(tmpz-radius-2, tmpz+radius+3):
                    
                        # if not water, keep running while loop with new value
                        if sm.get_block(level,j, i[1], k) != 8 and sm.get_block(level, j, i[1], k) != 9:
                            bool_chk = True
                            break
                    if bool_chk == True:
                        break
                if bool_chk == True:
                    tmpx = i[0]+random.randint(-10-chk,10+chk)
                    tmpz = i[2]+random.randint(-10-chk,10+chk)
                    chk += 1
                    
                # if loop runs more than 250 times, assume there is no free spot and no lighthouse will be generated
                if chk >= 250:
                    break
            if chk < 250:
                create(level, tmpx, i[1], tmpz, radius, 15, 30, options)

# This create function uses a single point(x,y,z) with radius(r) and random height between min_height and max_height
def create(level, x, y, z, r, min_height, max_height, options):
    centerx = x
    centerz = z
    radius = r
    
    # Create Base
    for i in range(centerx-radius-2, centerx+radius+3):
        for j in range(centerz-radius-2, centerz+radius+3):
            utilityFunctions.setBlock(level, (options["Material"].ID,0), i, y-1, j)
            utilityFunctions.setBlock(level, (options["Material"].ID,0), i, y-2, j)
            utilityFunctions.setBlock(level, (options["Material"].ID,0), i, y, j)
            
    # Create Floor
    for i in range(centerx-radius, centerx+radius):
        for j in range(centerz-radius, centerz+radius):
            if radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0:
                utilityFunctions.setBlock(level, (options["Material"].ID,0), i, y, j)    
    
    # Create Wall
    base_height = random.randint(min_height,max_height)
    print base_height
    for k in range(y,y+base_height):
        for i in range(centerx-radius, centerx+radius):
            for j in range(centerz-radius, centerz+radius):        
                if radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0 and (radius-1)**2 - ((centerx-i)**2 + (centerz-j)**2) <= 0:
                    utilityFunctions.setBlock(level, (options["Material"].ID,0), i, k, j)
    
    # Create Top Base and roof
    top_radius = radius + 2
    for i in range(centerx-top_radius, centerx+top_radius):
        for j in range(centerz-top_radius, centerz+top_radius):
            if top_radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0:
                utilityFunctions.setBlock(level, (options["Material"].ID,0), i, y+base_height, j)
                utilityFunctions.setBlock(level, (options["Material"].ID,0), i, y+base_height+8, j)
    
    # Create Fence Wall
    fence_radius = radius - 1
    for k in range(y+base_height+1,y+base_height+8):
        for i in range(centerx-fence_radius, centerx+fence_radius):
            for j in range(centerz-fence_radius, centerz+fence_radius):        
                if fence_radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0 and (fence_radius-1)**2 - ((centerx-i)**2 + (centerz-j)**2) <= 0:
                    utilityFunctions.setBlock(level, (85,0), i, k, j)
            
    # Create center (lights)
    light_radius = radius - 3
    for i in range(centerx-light_radius, centerx+light_radius):
        for j in range(centerz-light_radius, centerz+light_radius):
            if light_radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0:
                utilityFunctions.setBlock(level, (89,0), i, y+base_height+3, j)
                utilityFunctions.setBlock(level, (89,0), i, y+base_height+4, j)
                utilityFunctions.setBlock(level, (89,0), i, y+base_height+5, j)


# This create method uses the box obtained from perform (user selected box)
# def create(level, box):
    # width, height, depth = utilityFunctions.getBoxSize(box)
    # centerx = box.minx + int(width/2)
    # centerz = box.minz + int(depth/2)
    # radius = min(int(width/2), int(depth/2), 10)
    # radius = max(radius, 5)
    # print radius
    
    # # Create Base
    # for i in range(centerx-radius-3, centerx+radius+2):
        # for j in range(centerz-radius-3, centerz+radius+2):
            # utilityFunctions.setBlock(level, (1,0), i, box.miny-1, j)
            # utilityFunctions.setBlock(level, (1,0), i, box.miny-2, j)
            # utilityFunctions.setBlock(level, (1,0), i, box.miny, j)
            
    # # Create Floor
    # for i in range(centerx-radius, centerx+radius):
        # for j in range(centerz-radius, centerz+radius):
            # if radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0:
                # utilityFunctions.setBlock(level, (1,0), i, box.miny, j)    
    
    # # Create Wall
    # max_height = height
    # if height < 10:
        # max_height = 40
    # base_height = random.randint(9,max_height)
    # print base_height
    # for k in range(box.miny,box.miny+base_height):
        # for i in range(centerx-radius, centerx+radius):
            # for j in range(centerz-radius, centerz+radius):        
                # if radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0 and (radius-1)**2 - ((centerx-i)**2 + (centerz-j)**2) <= 0:
                    # utilityFunctions.setBlock(level, (1,0), i, k, j)
    
    # # Create Top Base and roof
    # top_radius = radius + 2
    # for i in range(centerx-top_radius, centerx+top_radius):
        # for j in range(centerz-top_radius, centerz+top_radius):
            # if top_radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0:
                # utilityFunctions.setBlock(level, (1,0), i, box.miny+base_height, j)
                # utilityFunctions.setBlock(level, (1,0), i, box.miny+base_height+8, j)
    
    # # Create Fence Wall
    # fence_radius = radius - 1
    # for k in range(box.miny+base_height+1, box.miny+base_height+8):
        # for i in range(centerx-fence_radius, centerx+fence_radius):
            # for j in range(centerz-fence_radius, centerz+fence_radius):        
                # if fence_radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0 and (fence_radius-1)**2 - ((centerx-i)**2 + (centerz-j)**2) <= 0:
                    # utilityFunctions.setBlock(level, (85,0), i, k, j)
            
    # # Create center (lights)
    # light_radius = radius - 3
    # for i in range(centerx-light_radius, centerx+light_radius):
        # for j in range(centerz-light_radius, centerz+light_radius):
            # if light_radius**2 - ((centerx-i)**2 + (centerz-j)**2) > 0:
                # utilityFunctions.setBlock(level, (89,0), i, box.miny+base_height+3, j)
                # utilityFunctions.setBlock(level, (89,0), i, box.miny+base_height+4, j)
                # utilityFunctions.setBlock(level, (89,0), i, box.miny+base_height+5, j)
                
     
    


