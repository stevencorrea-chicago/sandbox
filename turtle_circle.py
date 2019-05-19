import turtle
wn = turtle.Screen()
wn.bgcolor("lightgreen")
jose = turtle.Turtle()
jose.shape("turtle")
jose.penup()

jose.speed (1)
jose.goto(0,0)
jose.stamp()

jose.goto(-20,75)

for size in range(10):    # start with size = 5 and grow by 2
    jose.forward(50)
    jose.stamp()
    jose.right(36)
    
    
wn.exitonclick()
