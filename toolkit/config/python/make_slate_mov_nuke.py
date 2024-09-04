import nuke
import os

# path = "/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/CMP/pub/nuke/images/ABC_0010_CMP_v001/ABC_0010_CMP_v001.####.exr"
# first = 1001
# last = 1096

"""
이 코드는 nuke -t로 실행됩니다
아래는 터미널에서 수행되는 실행문 예시
nuke -t make_slate_mov_nuke.py -path "/home/rapa/baked/show/baked/SEQ/ABC/ABC_0010/CMP/pub/nuke/images/ABC_0010_CMP_v001/ABC_0010_CMP_v001.####.exr" -first "1001" -last "1096" 
"""

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-input_path", help=" : input file path")
parser.add_argument("-output_path", help=" : output file path")
parser.add_argument("-first", help=" : input first frame")
parser.add_argument("-last", help=" : input last frame")
args = parser.parse_args()

print(f"{args.input_path}\n{args.first}\n{args.last}\n")


def make_mov_with_slate_data(input_path, output_path, first_frame, last_frame):
    """
    경로와 frame 시작과 끝 정보를 가지고 자동으로 경로상의 파일을 읽어와
    슬레이트를 포함한 mov를 뽑아내는 함수입니다
    """
    print(f"Making Slate MOV with {input_path}")

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    nuke.root().knob("colorManagement").setValue("OCIO")
    nuke.root().knob("OCIO_config").setValue("fn-nuke_cg-config-v1.0.0_aces-v1.3_ocio-v2.1")
    
    read_node = nuke.nodes.Read()
    read_node.knob("file").setValue(input_path)
    read_node.knob("first").setValue(first_frame)
    read_node.knob("last").setValue(last_frame)

    color_node = nuke.createNode("OCIOColorSpace")
    color_node.knob("in_colorspace").setValue("ACEScg")
    color_node.knob("out_colorspace").setValue("data")
    
    slate_node = nuke.createNode("slate_baked")
    slate_node.setInput(0, read_node)
    slate_node.knob("top_center").setValue("BAKED") # 후에 Shotgrid에서 가져온 데이터로 수정
    slate_node.knob("bottom_center").setValue("추예린")

    write_node = nuke.createNode("Write")
    write_node.setInput(0, slate_node)
    write_node.knob("file_type").setValue("mov")
    write_node.knob("colorspace").setValue("Gamma 2.2 Rec.709 - Texture")
    write_node.knob("file").setValue(output_path)



    nuke.execute(write_node, start=first_frame, end=last_frame, incr=1)

    print(f"Finished Making Slate MOV : {output_path}")



make_mov_with_slate_data(args.input_path, args.output_path, int(args.first), int(args.last))
