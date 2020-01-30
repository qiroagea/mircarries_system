from include.motor_control import Control
coco = Control()
doz = coco.set.encState()
coco.set(70,70)
if doz[0]:
    if doz[1]:
        print("2")
    else:
        print("0")
if doz[1]:
    if doz[0]:
        print("3")
    else:
        print("1")
