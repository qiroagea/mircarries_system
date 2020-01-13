from pyfirmata import Arduino, util
import time


class Control:
    def __init__ (self):
        self.board = Arduino('/dev/ttyACM0')
        self.motorL = self.board.get_pin('d:8:o')
        self.motorR = self.board.get_pin('d:12:o')
        self.pwmL = self.board.get_pin('d:9:p')
        self.pwmR = self.board.get_pin('d:11:p')
        self.motorL.write(0)
        self.motorR.write(0)
        self.pwmL.write(0.5)
        self.pwmR.write(0.5)
        self.battery = self.board.get_pin('a:5:i')
        self.it = util.Iterator(self.board)
        self.it.start()

    def stop(self):
        self.motorL.write(0)
        self.motorR.write(0)
        self.pwmL.write(0.5)
        self.pwmR.write(0.5)

    def run(self):
        self.motorL.write(1)
        self.motorR.write(1)
        self.pwmL.write(1)
        self.pwmR.write(1)

    def set(self, l, r):
        setL = l + 100
        setR = r - 100

        if setL != 0:
            setL = setL/200

        if setR != 0:
            setR = setR/-200

        if l==0:
            self.motorL.write(0)
        else:
            self.motorL.write(1)

        if r==0:
            self.motorR.write(0)
        else:
            self.motorR.write(1)

        self.pwmL.write(setL)
        self.pwmR.write(setR)

    def check(self):
        time.sleep(0.01)
        self.battery.enable_reporting()
        voltage = self.battery.read() / 321 * 5500
        return voltage









