from tkinter import *
from matplotlib import pyplot as plt
import numpy
import random

root = Tk()
mat = Text(root)
aprev = []
bprev = []
def Submit():
    global aprev, bprev
    aprev.reverse()
    bprev.reverse()
    T = 0.01
    t = [0.0] * 1000
    for i in range(1000): t[i] = i*T
    #I mixed up m with n, sorry
    m = N.get()
    a = [0.0] * (m+1)
    b = [0.0] * (m+1)
    i = 0
    x = []
    y = [0.0] * 1000
    #derivatives
    x_ = [0.0] * m
    #u.get = 1 -> impulse
    k = U.get()
    if k == 1: label = "impulse"
    else: label = "step"
    u = [k] * 100
    u = u + [abs(k - 1)] * 900
    i = 0
    for i in range(m): x.append([0.0] * 1000)
    i = 0
    if r.get() ==1:
        a = random.sample(range(1, 15), m+1)
        b = random.sample(range(1, 15), M.get()+1)
        b = [0.0] * (m-M.get()) + b
    elif aprev and not As.get():
        a = aprev
        b = bprev
    else:
        for word in As.get().split():
            a[i] = float(word)
            i += 1
        i = m-M.get()
        for word in Bs.get().split():
            b[i] = float(word)
            i += 1
        i = 0
    
    aprev = a
    bprev = b
    a.reverse()
    b.reverse()
    # state-space matrices
    A = [0.0] * m
    B = [0.0] * m
    C = [0.0] * m
    C[m-1] = 1
    D = [b[m]/a[m]]
    i = 0
    for i in range(m):
        A[i] = [0.0] * m
        A[i][m-1] = -a[i]/a[m]
        if i > 0: A[i][i-1] = 1
        B[i] = b[i]/a[m] - a[i]*b[m]/(a[m]*a[m])
#formatting matrices
    A = str(A)
    A = A.replace("[[", "[")
    A = A.replace("], [", "; ")
    A = A.replace("]]", "]")
    B = str(B)
    B = B.replace(",", ";")
    mat.delete(0.0, END)
    mat.insert(INSERT, "A = " + A + "\nB = " + B + "\nC = " + str(C) + "\nD = " + str(D))
    mat.pack(fill=BOTH)
    #automatically copying the state-space matrices for the report:
    root.clipboard_clear()
    root.clipboard_append("A = " + A + "\nB = " + B + "\nC = " + str(C) + "\nD = " + str(D))
    i = 0
    #calculating output, states
    for n in range(999):
        x_[0] = -a[0]/a[m] * x[m-1][n] + (b[0]/a[m] - (a[0]*b[m])/(a[m]*a[m])) * u[n]
        x[0][n+1] = x[0][n] + T * x_[0]
        for i in range(1, m):
            x_[i] = x[i-1][n] - a[i]/a[m] * x[m-1][n] + (b[i]/a[m] - (a[i]*b[m])/(a[m]*a[m])) * u[n]
            x[i][n+1] = x[i][n] + T * x_[i]
        y[n] = x[m-1][n] + b[m]/a[m] * u[n]
        y[n+1] = x[m-1][n+1] + (b[m]/a[m]) * u[n+1]

    p = P.get()
    if p == 4: plt.plot(t, y, label = label)
    elif p == 5: plt.plot(t, u, label = label)
    else: plt.plot(t, x[p], label = label)
    plt.xticks(numpy.arange(t[0], t[999]+1, 1))
    plt.grid(True)
    plt.legend()
    plt.show()

M = IntVar()
labelM = Label(root, text="Enter m")
entryM = Entry(root, textvariable=M)
N = IntVar()
labelN = Label(root, text="Enter n")
entryN = Entry(root, textvariable=N)
r = IntVar()
rand = Checkbutton(root, text="Random parameters", variable=r, onvalue=1, offvalue=0)

As = StringVar()
Bs = StringVar()
labelA = Label(root, text="Enter a's: an an-1 an-2...")
labelB = Label(root, text="Enter b's: bm bm-1 bm-2...")
entryA = Entry(root, textvariable=As)
entryB = Entry(root, textvariable=Bs)

labelP = Label(root, text="plot: ")
P = IntVar()
p0 = Radiobutton(root, text="y", variable=P, value=4)
p1 = Radiobutton(root, text="u", variable=P, value=5)
p2 = Radiobutton(root, text="x1", variable=P, value=0)
p3 = Radiobutton(root, text="x2", variable=P, value=1)
p4 = Radiobutton(root, text="x3", variable=P, value=2)
p5 = Radiobutton(root, text="x4", variable=P, value=3)

U = IntVar()
u1 = Radiobutton(root, text="step", variable=U, value=0)
u2 = Radiobutton(root, text="impulse", variable=U, value=1)

submit = Button(root, text="Submit", command=Submit)

labelN.pack()
entryN.pack(fill=BOTH)  
labelM.pack()
entryM.pack(fill=BOTH)
labelA.pack()
entryA.pack(fill=BOTH)
labelB.pack()
entryB.pack(fill=BOTH)
rand.pack()
u1.pack()
u2.pack()
labelP.pack()
p0.pack()
p1.pack()
p2.pack()
p3.pack()
p4.pack()
p5.pack()
submit.pack()

root.mainloop()