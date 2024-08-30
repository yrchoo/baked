print ("------------UserSetup------------")
import maya.utils as mu
import test_menu

mu.executeDeferred('test_menu.add_custom_menu()')

import sys
sys.path.append("/home/rapa/baked/toolkit/config/python/")
sys.path.append("/home/rapa/baked/toolkit/config/python/shotgrid")
