import nuke
import os

# path = "/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/CMP/pub/nuke/images/ABC_0010_CMP_v001/ABC_0010_CMP_v001.####.exr"
# first = 1001
# last = 1096

"""
nuke -t make_slate_mov_nuke.py -first 1001 -last 1096 -path "/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/CMP/pub/nuke/images/ABC_0010_CMP_v001/ABC_0010_CMP_v001.####.exr"
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-path", help=" : input file path")
parser.add_argument("-first", help=" : input first frame")
parser.add_argument("-last", help=" : input last frame")
args = parser.parse_args()

print(f"{args.path}\n{args.first}\n{args.last}\n")


def make_mov_with_slate_data(path, first, last):
    read_node = nuke.nodes.Read()
    read_node.knob("file").setValue(path)
    read_node.knob("first").setValue(first)
    read_node.knob("last").setValue(last)
    
    slate_node = nuke.createNode("slate_baked")
    slate_node.setInput(0, read_node)
    slate_node.knob("top_center").setValue("BAKED") # 후에 Shotgrid에서 가져온 데이터로 수정
    slate_node.knob("bottom_center").setValue("추예린")

    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    file_name = basename.split('.')[0] + ".mov"
    new_path = f"/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/CMP/pub/nuke/mov/"
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    new_path += file_name
    print(new_path)

    write_node = nuke.createNode("Write")
    write_node.setInput(0, slate_node)
    write_node.knob("file_type").setValue("mov")
    write_node.knob("file").setValue(new_path)

    nuke.execute(write_node, start=first, end=last, incr=1)
   


make_mov_with_slate_data(args.path, int(args.first), int(args.last))
# make_mov_with_slate_data(path, int(first), int(last))