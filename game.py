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
round = 4
score = 0
kolon = 0
canHplay = True

pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()

pen2 = turtle.Turtle()
pen2.speed(0)
pen2.color("black")
pen2.penup()
pen2.goto(60,190)
pen2.hideturtle()

wn.tracer(False)
controlarea = turtle.Turtle()
controlarea.begin_fill()
controlarea.color("Goldenrod")
controlarea.penup()
controlarea.goto(50,190)
controlarea.pendown()
controlarea.goto(50,30)
controlarea.goto(20,30)
controlarea.goto(20,190)
controlarea.goto(50,190)
controlarea.penup()
controlarea.end_fill()
controlarea.hideturtle()
wn.tracer(True)



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

def fin():
    turtle.clearscreen()
    wn = turtle.Screen()
    wn.bgcolor("blue")
    pen3 = turtle.Turtle()
    pen3.speed(0)
    pen3.color("white")
    pen3.penup()
    pen3.goto(70,100)
    pen3.hideturtle()
    pen3.write("Good job! Your Score = {}".format(score), font=("Courier", 12, "normal"))


def draw():
    #print(states)
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

    pen2.clear()
    pen2.write("left:{} score:{} column:{}".format(round,score,kolon), font=("Courier", 15, "normal"))


    pen.clear()
    if chosed == "none":
        if canHplay:
            pen.write("Press on X,H,C,S or R", font=("Courier", 20, "normal"))
        else:
            pen.write("Press on X,C,S or R (wait next column for H)", font=("Courier", 20, "normal"))
    if chosed == "x":
        pen.write("Not Gate (choose column)", font=("Courier", 12, "normal"))
    if chosed == "h":
        pen.write("H Gate (choose qubit - only once for each column) ", font=("Courier", 12, "normal"))
    if chosed == "s":
        pen.write("Swap with the right qubit (choose qubit)", font=("Courier", 12, "normal"))
    if chosed == "r":
        pen.write("Reset (choose qubit - only grey ones)", font=("Courier", 12, "normal"))
    if chosed == "c":
        pen.write("Controlled Not gate (choose target qubit,control the qubit on the right)", font=("Courier", 12, "normal"))
    wn.tracer(True)

    if round == 0 and (states[0] != states[1] or states[1] != states[2] or states[2] != states[3] or states[3] != states[4]):
        fin()


def clicked(x,y):
    global states
    global chosed
    global round
    global score
    global kolon
    global canHplay
    #print(x," ",y)
    for i in range(5):
        for j in range(5):
            if math.sqrt(math.pow(35+i*30-x,2) + math.pow(50+j*30-y,2)) <=5:

                if chosed == "x":
                    round = round - 1
                    for j in range(5):
                        circuit.x(qr[24-(i*5+j)])

                if chosed == "h":
                    canHplay = False
                    round = round - 1
                    circuit.h(qr[24-(i*5+j)])

                if chosed == "r" and states[i*5+j] == "g":
                    round = round - 1
                    circuit.reset(qr[24-(i*5+j)])

                if chosed == "s" and i != 4:
                    round = round - 1
                    circuit.swap(qr[24-(i*5+j)],qr[24-((i+1)*5+j)])

                if chosed == "c" and i != 4:
                    round = round - 1
                    circuit.cx(qr[24-((i+1)*5+j)],qr[24-(i*5+j)])

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

    if statesT[0] == statesT[1] and statesT[1] == statesT[2] and statesT[2] == statesT[3] and statesT[3] == statesT[4]:
         for i in range(1,5):
            for j in range(5):
                balls[i*5+j].speed(2)
                balls[i*5+j].goto(35+(i-1)*30,50+j*30)
         score = score + 20 + round*10
         round = 4
         kolon = kolon + 1
         canHplay = True
         circuit.reset(qr[24])
         circuit.reset(qr[23])
         circuit.reset(qr[22])
         circuit.reset(qr[21])
         circuit.reset(qr[20])
         statesT[0] = "b"
         statesT[1] = "b"
         statesT[2] = "b"
         statesT[3] = "b"
         statesT[4] = "b"
         for i in range(4):
             for j in range(5):
                 circuit.swap(qr[24-(i*5+j)],qr[24-((i+1)*5+j)])
                 statesT[i*5+j],statesT[(i+1)*5+j] = statesT[(i+1)*5+j],statesT[i*5+j]

         for i in range(4):
             r= random.randint(0, 3)
             if r == 1:
                 statesT[20+i]="w"
                 circuit.x(qr[24-(20+i)])
             if r == 2:
                 statesT[20+i]="g"
                 circuit.h(qr[24-(20+i)])

    states = statesT
    draw()


def xgate():
    global chosed
    chosed = "x"
    draw()


def hgate():
    if canHplay:
        global chosed
        chosed = "h"
        draw()

def swapq():
    global chosed
    chosed = "s"
    draw()

def resetq():
    global chosed
    chosed = "r"
    draw()

def cxgate():
    global chosed
    chosed = "c"
    draw()

draw()
wn.onclick(clicked)
wn.onkey(xgate, "x")
wn.onkey(hgate, "h")
wn.onkey(swapq, "s")
wn.onkey(resetq, "r")
wn.onkey(cxgate, "c")

wn.listen()
wn.mainloop()
