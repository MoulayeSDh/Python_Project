import math
import turtle 
turtle.bgcolor("black")
turtle.shape("turtle")
turtle.speed(0)
turtle.fillcolor("brown")
Qi= 137.508 * (math.pi/180.0)
for i in range(160+40):
    r=4 * math.sqrt(i)
    phi = i*Qi
    x= r * math.cos(phi)
    y= r* math.sin(phi)
    turtle.penup()
    turtle.goto(x,y)
    turtle.setheading(i* 137.508)
    turtle.pendown()
    if i<160:
        turtle.stamp() 
    else :
        turtle.fillcolor("yellow ")
        turtle.begin_fill()
        turtle.right(400)
        turtle.forward(1700)
        turtle.left(800)
        turtle.forward(1700)
        turtle.left(800)
        turtle.forward(1700)
        turtle.left(800)
        turtle.forward(1700)
        turtle.end_fill()
turtle.hideturtle()
    