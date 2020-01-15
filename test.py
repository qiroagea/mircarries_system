from include.yolo_v3 import ObjectDetection
from include.motor_control import Control

od = ObjectDetection()
control = Control()

while 1:
    od.human()
    # control.set(20, 20)
