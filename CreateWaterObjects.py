import time # for timing
from pymclevel import alphaMaterials, MCSchematic, MCLevel, BoundingBox

import CreateShips  as cs
import lighthouse as lh

inputs = (
	("Ship and Lighthouse", "label"),
	("Material", alphaMaterials.Stone), # the material we want to use to build the mass of the structures
	("Creator: Sunshine Chong and Steven Guan", "label"),
	)
 
def perform(level, box, options):
    cs.perform(level, box, options)
    lh.perform(level, box, options)