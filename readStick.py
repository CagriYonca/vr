import serial
import sys
import string
import subprocess

if len(sys.argv) == 1:
    device = "/dev/ttyUSB0"
    stickType = 0
if len(sys.argv) == 2:
    device = sys.argv[1]
if len(sys.argv) == 3:
    device = sys.argv[1]
    stickType = int(sys.argv[2])

ser = serial.Serial(device, baudrate=115200, timeout=1)

def moveMouse(stickX, stickY):
    if (abs(stickX) > 1) or (abs(stickY) > 1):
        a =  subprocess.check_output(["bash", "-c", "xdotool mousemove_relative -- " + str(stickX) + " " + str(stickY)])


def movePlayer(aX, aY):
    if (aX < -9):
        a =  subprocess.check_output(["bash", "-c", "xdotool key a"])
    
    if (aX > 9):
        a =  subprocess.check_output(["bash", "-c", "xdotool key d"])
 
    if (aY < -9):
        a =  subprocess.check_output(["bash", "-c", "xdotool key s"])

    if (aY > 9):
        a =  subprocess.check_output(["bash", "-c", "xdotool key w"])
   

def clickMouse(signal):
    if (signal == 1):
        a = subprocess.check_output(["bash", "-c", "xdotool mousedown 1"])
    if (signal == 0):
        a = subprocess.check_output(["bash", "-c", "xdotool mouseup 1"])
        
    return signal


def getData(connection):
    try:
        data = str(connection.readline().decode("utf-8"))
        
        """ Rotation """
        aX = int(data[data.find("mapAX") + 5 : data.find("mapAY")])
        aY = int(data[data.find("mapAY") + 5 : data.find("mapAZ")])
        aZ = int(data[data.find("mapAZ") + 5 : data.find("mapGX")])
    
        """ Acceleration"""
        gX = int(data[data.find("mapGX") + 5 : data.find("mapGY")])
        gY = int(data[data.find("mapGY") + 5 : data.find("mapGZ")])
        gZ = int(data[data.find("mapGZ") + 5 : data.find("x")])
    
        """ Joystick """
        x = int(data[data.find("x") + 1 : data.find("y")])
        y = int(data[data.find("y") + 1 : data.find("s")])
        z = int(data[data.find("s") + 1])

    # Calibrate  - ler silindi
        aX *= -1
        aY *= -1
        gX *= -1
        gZ *= -1

        return aX, aY, aZ, gX, gY, gZ, x, y, z
    
    except:
        return 0, 0, 0, 0, 0, 0, 0, 0, 1

pressedDown = 0

while True:
    aX, aY, aZ, gX, gY, gZ, sX, sY, sZ = getData(ser)
    # Mouse'u hareket ettir
    if(stickType == 0):
        moveMouse(-1 * sY, sX)         
#        movePlayer(aX, aZ)
    else:
        moveMouse(int(aX/10), -int(aY/10))         
    if (sZ == 0) and (pressedDown == 0):
        pressedDown = 1
        clickMouse(pressedDown)
    if (sZ == 1) and (pressedDown == 1):
        pressedDown = 0
        clickMouse(pressedDown)
    
    print(chr(27) + "[2J")
    print("X \t Y \t Z \tEgim\n{} \t {} \t {}\n".format(aX, aY, aZ))
    print("X \t Y \t Z \tIvme\n{} \t {} \t {}\n".format(gX, gY, gZ))
    print("X \t Y \t Z \tJoystick\n{} \t {} \t {}\n".format(-sY, -sX, sZ))   
