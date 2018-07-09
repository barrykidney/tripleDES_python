import math


def funct(hyp, ang):

    x = 1
    y = 1
    if 90 < ang < 180:
        ang = 180 - ang
        x = x * -1

    elif 180 < ang < 270:
        ang = ang - 180
        x = x * -1
        y = y * -1

    elif 270 < ang < 360:
        ang = 360 - ang
        y = y * -1

    y = y * math.sin(math.radians(ang)) * hyp
    x = x * math.sqrt(hyp ** 2 - y ** 2)

    return x, y


vx, vy = funct(7, 100)
wx, wy = funct(5, 290)

print("\nV = [x: {:.2f}, y: {:.2f}]".format(vx, vy))
print("W = [x: {:.2f}, y: {:.2f}]".format(wx, wy))
print("\nANS = [x: {:.2f}, y: {:.2f}]".format(vx + wx, vy + wy))
