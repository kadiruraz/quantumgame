import turtle
import math
import random
from qiskit import *

qr = QuantumRegister(25)
cr = ClassicalRegister(25)
circuit = QuantumCircuit(qr,cr)

wn = turtle.Screen()
wn.bgcolor("Moccasin")
wn.title("quantum dots")
wn.setworldcoordinates(-1, -1, 200, 200)
balls = []
states = ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b', 'b']
chosed = "none"


pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("black")
pen.penup()
pen.hideturtle()


for i in range(25):
    balls.append(turtle.Turtle())

k=10
while k>0:
    r= random.randint(0, 24)
    if states[r] == "b":
        states[r] = "w"
        circuit.x(qr[24-r])
        k = k-1


k=5
while k>0:
    r= random.randint(0, 24)
    if states[r] == "b":
        states[r] = "g"
        circuit.h(qr[24-r])
        k = k-1


def draw():
    wn.tracer(False)
    for i in range(5):
        for j in range(5):
            balls[i*5+j].clear()
            balls[i*5+j].pensize(50)
            balls[i*5+j].shape("circle")
            balls[i*5+j].turtlesize(2,2)
            if states[i*5+j] == "b":
                balls[i*5+j].color("black")
            if states[i*5+j] == "w":
                balls[i*5+j].color("white")
            if states[i*5+j] == "g":
                balls[i*5+j].color("grey")
            balls[i*5+j].penup()
            balls[i*5+j].speed(0)
            balls[i*5+j].goto(35+i*30,50+j*30)

    pen.clear()
    if chosed == "none":
        pen.write("X or H", font=("Courier", 24, "normal"))
    if chosed == "x":
        pen.write("X Gate", font=("Courier", 24, "normal"))
    if chosed == "h":
        pen.write("H Gate", font=("Courier", 24, "normal"))


    wn.tracer(True)


def clicked(x,y):
    global states
    global chosed
    print(x," ",y)
    for i in range(5):
        for j in range(5):
            if math.sqrt(math.pow(35+i*30-x,2) + math.pow(50+j*30-y,2)) <=5:
                if chosed == "x":
                    circuit.x(qr[24-(i*5+j)])
                if chosed == "h":
                    circuit.h(qr[24-(i*5+j)])

    chosed = "none"

    circuit.measure(qr,cr)
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend = simulator ).result()
    hist = result.get_counts(circuit)

    statesT = ['n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n', 'n']
    for h in hist:
        for i in range(25):
            if statesT[i] == "n" and h[i] == "0":
                statesT[i]="b"
            elif statesT[i] == "n" and h[i] == "1":
                statesT[i]="w"
            elif statesT[i] == "b" and h[i] == "1":
                statesT[i]="g"
            elif statesT[i] == "w" and h[i] == "0":
                statesT[i]="g"

    states = statesT
    draw()


def xgate():
    global chosed
    chosed = "x"
    draw()


def hgate():
    global chosed
    chosed = "h"
    draw()


draw()
wn.onclick(clicked)
wn.onkey(xgate, "x")
wn.onkey(hgate, "h")


wn.listen()
wn.mainloop()
