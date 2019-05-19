import turtle
wn = turtle.Screen()
wn.bgcolor("lightgreen")
steve = turtle.Turtle()

steve.speed(0)

steve.backward(125)

for i in range(39):
    steve.forward(250)
    steve.right(175)
    
wn.exitonclick()
