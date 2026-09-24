import math
import turtle

#not quite symetrical??

convex = False
topDegree = 90
drawNormal = True
parallelLights = False

#refractive index of substance coming from (n1) and going into (n2)
n1 = 1
n2 = 1.5

lenseStartY = 281
lenseEndY = -1
lightStartX = -200
lightEndX = 600
lightStartY = -300
lightEndY = 350
turnNum = 20
sideLen = 15
normalLen = 2

if topDegree >= 180:
    exit
#degrees the turtles turns each time
deg = topDegree / (2 * turnNum)


def getSegment():
    totalSegmentNum = turnNum * 4 + 2

    for i in range(totalSegmentNum):
      segmentMP = midPoints[i]
      if abs( turtle.xcor() - ((segmentMP[2] * turtle.ycor()) + segmentMP[3]) ) <= 1:
        return i
    return -1

def drawNorm(normAng):
  turtle.right(normAng)
  
  turtle.backward(normalLen * 10)
  for x in range(normalLen * 2):
    turtle.pendown()
    turtle.forward(5)
    turtle.penup()
    turtle.forward(5)
  turtle.backward(normalLen * 10)
  turtle.left(normAng)


def inLense():
    if (turtle.ycor() >= lenseStartY) or (turtle.ycor() <= lenseEndY):
        return False
    halfTotalSegmentNum = turnNum * 2 + 1

    if convex:
        for i in range(halfTotalSegmentNum): #first check left side of lense
            segmentMP = midPoints[i]
            if turtle.xcor() <= segmentMP[2] * turtle.ycor() + segmentMP[3]: #uses x = my + c to check if the turtle is to the left of this segment
                return False

        for i in range(halfTotalSegmentNum): #then check right side of lense
          segmentMP = midPoints[i + (halfTotalSegmentNum)]
          if convex and (turtle.xcor() >= segmentMP[2] * turtle.ycor() + segmentMP[3]): #uses x = my + c to check if the turtle is to the right of this segment
            return False

        return True
    
    else:
        right = False
        for i in range(halfTotalSegmentNum): #first check left side of lense
            segmentMP = midPoints[i]
            if turtle.xcor() >= segmentMP[2] * turtle.ycor() + segmentMP[3]: #uses x = my + c to check if the turtle is to the right of this segment
                right = True
                break

        if not right:
            return False
        
        for i in range(halfTotalSegmentNum): #then check right side of lense
            segmentMP = midPoints[i + (halfTotalSegmentNum)]
            if turtle.xcor() <= segmentMP[2] * turtle.ycor() + segmentMP[3]: #uses x = my + c to check if the turtle is to the left of this segment
                return True

        return False


def inBoundary():
    return ((turtle.xcor() >= lightStartX) and (turtle.xcor() <= lightEndX) and (turtle.ycor() >= lightStartY) and (turtle.ycor() <= lightEndY))

def createLight(angle, yStart):
  turtle.goto(lightStartX, yStart)
  turtle.pendown()
  turtle.right(angle)
  while((not inLense()) and inBoundary()):
    turtle.forward(1)
  turtle.penup()
  turtle.left(angle)

  if not inBoundary():
    return
  
  normAng = math.degrees(math.atan(midPoints[getSegment()][2]))
  if drawNormal:
    drawNorm(normAng)

  try:
    
    r = math.degrees(math.asin((n1 / n2) * math.sin(math.radians(normAng - angle))))
    turtle.right(normAng - r)
    turtle.pendown()
    while (inLense()):
      turtle.forward(1)
    turtle.penup()
    turtle.left(normAng - r)

    if (turtle.ycor() >= lenseStartY) or (turtle.ycor() <= lenseEndY):
        return
    
    normAng2 = math.degrees(math.atan(midPoints[getSegment()][2]))
    if drawNormal:
      drawNorm(normAng2)

    try:
    
        r2 = math.degrees(math.asin((n2 / n1) * math.sin(math.radians(normAng2 - normAng + r))))
        turtle.right(normAng2 - r2)
        turtle.pendown()
        while (inBoundary()):
          turtle.forward(20)
        turtle.left(normAng2 - r2)
        turtle.penup()
    except ValueError:
        #total internal reflection
        r2 = normAng2 - normAng + r
        turtle.right(normAng2 - 180 + r2)
        turtle.pendown()
        turtle.forward(80)
        turtle.penup()
        turtle.left(normAng2 - 180 + r2)
  except ValueError:
    #total internal reflection
    r = normAng-angle
    turtle.right(normAng-180+r)
    turtle.pendown()
    turtle.forward(80)
    turtle.penup()
    turtle.left(normAng-180+r)
  turtle.penup()


def half():
  global midPoints

  if convex:
      m = 1
  else:
      m = -1

  turtle.right(90 + m*topDegree/2)

  for x in range(turnNum * 2 + 1):
    x = turtle.xcor()
    y = turtle.ycor()
    turtle.forward(sideLen / 2)

    grad = (turtle.xcor() - x) / (turtle.ycor() - y)
    xIntercept = x - (y * grad)

    x = turtle.xcor()
    y = turtle.ycor()
    turtle.forward(sideLen / 2)

    midPoints.append([x, y, grad, xIntercept])

    turtle.right(-m*deg)
  turtle.right(270 + m*(topDegree/2 + deg))
  turtle.forward(sideLen * (10))
  if not convex:
      turtle.forward(sideLen * turnNum)


turtle.penup()
turtle.speed(10000)
if not convex:
    lightStartX += 100

midPoints = []
turtle.goto(0, lenseStartY)
turtle.pendown()

half()
lenseEndY = turtle.ycor()
turtle.right(180)
half()
turtle.left(180)
turtle.penup()

if parallelLights:
    for a in range(int(len(midPoints) / 2)):
        createLight(0, midPoints[a][1])
else:
    yStart = midPoints[turnNum][1]
    changeInAngle = 10
    angle = 45
    for i in range(int(90 / changeInAngle) + 1):
        createLight(angle, yStart)
        angle -= changeInAngle

turtle.goto(midPoints[turnNum * 3 + 1][0], midPoints[turnNum * 3 + 1][1])
