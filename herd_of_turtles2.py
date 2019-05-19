import turtle
wn = turtle.Screen()             # Set up the window and its attributes
wn.bgcolor("lightgreen")


tess = turtle.Turtle()           # create tess and set his pen width
tess.pensize(5)

alex = turtle.Turtle()           # create alex
alex.color("hotpink")            # set his color
alex.pensize(3)

tess.forward(80)                 # Let tess draw an equilateral triangle
alex.forward(50)                 # make alex draw a square
tess.left(120)
alex.left(90)
tess.forward(80)
alex.forward(50)
tess.left(120)
alex.left(90)
tess.forward(80)
alex.forward(50)
tess.left(120)                   # complete the triangle
alex.left(90)
tess.right(180)                  # turn tess around
alex.forward(50)
tess.forward(80)                 # move her away from the origin so we can see alex
alex.left(90)

wn.exitonclick()
