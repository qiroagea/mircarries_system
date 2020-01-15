from include.yolo_v3 import ObjectDetection
from include.motor_control import Control

od = ObjectDetection()
cl = Control()

while 1:
    x = od.human()
    print(x)
    if x == 0:
        cl.set(22, 25)
    else:
        cl.stop()
