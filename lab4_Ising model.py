import numpy as np
import matplotlib.pyplot as plt
import random as rd

#function random generator
def generate_random_spin(n):
    random_signs = [rd.choice([-1, 1]) for _ in range(n)]
    return random_signs

def Visualize(Spin):
    for a in range(len(Spin)+1):
        plt.plot([0,len(Spin[0])],[a,a],'k')
    for b in range(len(Spin[0])+1):
        plt.plot([b,b],[0,len(Spin)], 'k')
    
    for j in range(len(Spin)):
        print(j)
        for i in range(len(Spin[j])):
            if Spin[len(Spin)-1-j][i] == 1:
                plt.quiver(i+0.5,j+0.25,0,0.1,color = 'r')
            else:
                plt.quiver(i+0.5,j+0.75,0,-0.1,color = 'b')
    plt.show()

def Visualize2(Spin):
    plt.imshow(Spin,cmap='Greys')
    plt.show()

def GNC(y,x,array):
    if x+1 == len(array[0]):
        xp1 = 0
    else:
        xp1 = x + 1
    if x-1 == -1:
        xm1 = len(array[0]) - 1
    else:
        xm1 = x - 1
    if y+1 == len(array):
        yp1 = 0
    else:
        yp1 = y + 1
    if y-1 == -1:
        ym1 = len(array) - 1
    else:
        ym1 = y - 1
    
    return [[yp1,x],[ym1,x],[y,xp1],[y,xm1]]

#rd.seed(100)


#Randomly select a location on the grid j with spin σj

#Calculate ∆H if you flip the spin to the other direction

def flip(times,Spin):
    for i in range(times):
        sum=0
        m=rd.randint(0,height-1) #y axis
        n=rd.randint(0,width-1) #x axis
        spinmn=Spin[m][n]  # look for the spin in that position
        neighborList=GNC(m,n,Spin)
     
        
        for j in range(4):
            m1,n1=neighborList[j]
            sum=sum+Spin[m1][n1]

        deltaH=2*spinmn*(J*sum+h)


        if deltaH < 0:
            flip = True
        else:
            P = np.exp(-deltaH/beta)
            n_rand = rd.random()
            flip = n_rand < P

        if flip:
            Spin[m][n]= -Spin[m][n]

def convergence(Spin):
    return(abs(sum(sum(Spin)))/(len(Spin)*len(Spin[0])))




J = 1
height = 100
width = 100
beta = 10

A = 0
B = 1000

Target = 0.95
Tolerance = 0.005
Cov_Torr = 0.001

while True:
    spin = np.empty((height,width),int)
    for j in range(height):
        for i in range(width):
            spin[j][i] = rd.choice([-1, 1])
            

    
    CurrentBest = (A + B)/2
    h = CurrentBest # This line defines which variable to bisect
    print(CurrentBest)
    conv = []
    
    while True:
        conv = np.append(conv,convergence(spin))
        #print(conv[-1])
        flip(height*width,spin)
        if len(conv) >= 100:
            Len = len(conv)
            if abs(sum(conv[Len-50:Len])-sum(conv[Len-100:Len-50])) <= Cov_Torr:
                break

    if abs(sum(conv[Len-100:Len])/100-Target)<Tolerance:
        print(CurrentBest)
        print('@: ' + str(abs(sum(conv[Len-100:Len])/100)))
        break
    elif sum(conv[Len-100:Len])/100 > (Target+Tolerance):
        print('too high: ' + str(sum(conv[Len-100:Len])/100))
        B = CurrentBest #Depending on if increaseing the variable increase of decrease the total magnetization, this line may be changed to A
    elif sum(conv[Len-100:Len])/100 < (Target-Tolerance):
        print('too low: ' + str(sum(conv[Len-100:Len])/100))
        A = CurrentBest #Vice versa.










