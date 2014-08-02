import sys, time
import RPi.GPIO as GPIO
import sys

if __name__ == '__main__':
    """Blinking GPIO_4 and GPIO_7"""

    interval = 0.5

    if len(sys.argv) > 1:
        print "argv is ", sys.argv[1:]
        interval = float(sys.argv[1])

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(7, GPIO.OUT)

    count = 1
    try:
        while True:
            count += 1
            print "GPIO4 on"
            GPIO.output(4, True)
            time.sleep(interval)
            print "GPIO4 off"
            GPIO.output(4, False)
            time.sleep(interval)
    except KeyboardInterrupt:
        print("detect key interrupt\n")
        GPIO.cleanup()
