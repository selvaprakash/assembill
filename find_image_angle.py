import math

def find_angle(x1,y1,x2,y2):
    x1=int(x1)
    x2=int(x2)
    y1=int(y1)
    y2=int(y2)
    m=float(y2-y1)/float(x2-x1)
    angle=math.degrees(math.atan(m))
    print ('angle',angle)
    return angle


if __name__=='__main__':
    find_angle(0,0,3,2)
