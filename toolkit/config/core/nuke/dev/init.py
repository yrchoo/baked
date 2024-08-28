"""
이 스크립트에는 Nuke 실행시 사전에 설정해야하는
스크립트나 플러그인, 기즈모들을 참조하는 스크립트가 작성되면 좋아요
"""


print("*" * 30)
print ("init.py")
print("Initialize Script is executed.")
print("*" * 30)

import nuke
import os


nuke.pluginAddPath("./gizmo")
nuke.pluginAddPath("./icons")
nuke.pluginAddPath("./lib/python3.9/site-packages")
nuke.pluginAddPath("./lut")
nuke.pluginAddPath("./python")
nuke.pluginAddPath("./plugins")

import sys
sys.path.append("/home/rapa/baked/toolkit/config/python/")
sys.path.append("/home/rapa/baked/toolkit/config/python/shotgrid")

