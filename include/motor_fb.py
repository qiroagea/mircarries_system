from include.motor_control import Control
import time


class FeedBack:
    def __init__(self):
        self.control = Control()

    def straight(self, speed, dist):
        v = self.control.check()
        print(v)
        v = v - 6.2
        ini = v * 11
        sp = speed - ini * speed / 100
        corre = 1.2
        if sp - 40 < 0:
            spl = sp - (40 - sp) / 10 * corre
        else:
            spl = sp - (sp - 40) / 10 * corre

        spr = sp
        self.control.set(spl, spr)
        wait = dist * 1.364 / speed
        time.sleep(wait)

        self.control.stop()

    def carp_straight(self, speed, dist):
        v = self.control.check()
        print(v)
        v = v - 6.2
        ini = v * 11
        sp = speed - ini * speed / 100
        corre = 1.25
        if sp - 40 < 0:
            spl = sp - (40 - sp) / 10 * corre
        else:
            spl = sp - (sp - 40) / 10 * corre

        spr = sp
        self.control.set(spl, spr)
        if speed < 50:
            wait = dist * 1.55 / speed
        else:
            wait = dist * 1.364 / speed
        time.sleep(wait)

        self.control.stop()

    def rotate(self, deg):
        speedL = 15
        speedR = -15
        self.control.set(speedL, speedR)
        wait = 1.65 / 90 * deg

        time.sleep(wait)

        self.control.stop()

    def carp_rotate(self, deg):
        v = self.control.check()
        print(v)
        # v = v - 6.2
        # b = 8.2 - b
        # ini = v *
        # dg = 1.65 *
        # corre = 1.25
        speedL = 25
        speedR = -25
        self.control.set(speedL, speedR)
        # wait = 1.18 / 90 * deg
        wait = 1.4 / 90 * deg

        time.sleep(wait)

        self.control.stop()

    def stop(self):
        self.control.stop()
        time.sleep(2)
