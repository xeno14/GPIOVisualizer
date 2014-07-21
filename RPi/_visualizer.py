import matplotlib
import matplotlib.pyplot as plt
import _common

REV = _common.REV
pintogpio = _common.pintogpio

class PinVisualizer():

    WIDTH = 1
    HEIGHT = 1

    is_setup = False

    def __init__(self, ax, pin):
        self.state = False
        self.ax = ax
        self.pos = ((pin-1)%2, (pin-1)/2 + 0.5)
        self.is_gpio = True if pintogpio[REV][pin] > 0 else False

    def setup(self):
        self.is_setup = True

    def draw(self, mode):
        #TODO visualize setuped pins
        if self.is_gpio:
            if mode:
                color = 'red'   #high
            else:
                color = 'blue'  #low
        else:
            color = 'gray'      #not a GPIO
        rect = matplotlib.patches.Rectangle(\
                self.pos, self.WIDTH-0.1, self.HEIGHT-0.1, color=color)
        self.ax.add_patch(rect)
        plt.draw()

class Visualizer():

    XMIN = -0.1
    XMAX = 2.1
    YMAX = 14.0
    YMIN = 0.0

    def __init__(self):
        self.fig, self.ax = plt.subplots()
        plt.xlim([self.XMIN, self.XMAX])
        plt.ylim([self.YMAX, self.YMIN])
        self.ax.set_aspect('equal')

        self.pins = [None] * 30
        for pin in range(1, len(pintogpio[REV])):
            gpio = pintogpio[REV][pin]

            self.pins[gpio] = PinVisualizer(self.ax, pin)

            self.draw(gpio, False)

    def setup(self, channel):
        self.pins[channel].setup()

    def draw(self, channel, mode):
        pin = self.pins[channel]
        if pin is not None:
            self.pins[channel].draw(mode)
        plt.show(block=False)
