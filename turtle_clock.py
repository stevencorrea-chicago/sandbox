import turtle

wn = turtle.Screen()
t = turtle.Turtle()
print(type(t))
t.speed(0) 
t.pencolor('white') 
wn.bgcolor('black') 

x = 0 
t.up()

t.rt(45) 
t.fd(90) 
t.rt(135) 

t.down() 
while x < 120: 
    for i in range(6):
        t.fd(200)
        t.rt(61)

    t.rt(11.1111) 
    x = x+1 
wn.exitonclick()
