import glob
import os
import numpy as np

#=======================================================================================================
#                    ΠΡΟΓΡΑΜΜΑ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΣΠΟΥΔΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΔΙΚΤΥΩΝ
#                                    ΠΑΝΕΠΙΣΤΗΜΙΟ ΙΩΑΝΝΙΝΩΝ
#
#                 Distributed Permutation Flow-Shop Scheduling Problem
#
#********************************************************************************************************
#                                   ΚΙΟΣΣΕΣ ΔΗΜΗΤΡΙΟΣ ΑΜ 163
#********************************************************************************************************
#                                           main.py
#********************************************************************************************************
#
#
#********************************************************************************************************
#txtfile = glob.glob('./dataSet/Small/I_2_10_2_1.txt')


def read_dpfsp_dataset(txtfile):
    p={}
    d={}
    


    with open(txtfile, 'r') as fl:
        lines = fl.readlines()
    n, m = map(int, lines[0].split()) 
    F = lines[1]
    for j in range(n+1):
        for i, t in enumerate(lines[j+1].split()[1::2]):
            p[j,i]=int(t)
            print(p[j,i])
    print("----------------------------")
    for j in range(n):
        for i, duetime in enumerate(lines[j+3+n].split()):
            d[i]=int(duetime)
            print(d[i])        
        #x = f.readlines()[2:12]
        #x2 = map(int, x.split())
    #print(x2)
    print("----------------------------")
    print(n)
    print(m)  
    print(F)    

    return n, m, F, p, d
