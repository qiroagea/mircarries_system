from include.yolo_v3 import ObjectDetection
from include.motor_control import Control

od = ObjectDetection()
cl = Control()

print(cl.check())
# while 1:
#     x = od.human()
#     print(x)
#     if x == 0:
#         cl.set(21, 25)
#     else:
#         cl.stop()
