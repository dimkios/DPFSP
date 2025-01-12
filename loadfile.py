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


# def load_files():
#     i=1
#     #Δημιουργούμε μια δομή λεξικού της python στην οποία θα αποθηκεύσουμε τα ονόματα των αρχείων
#     arxeia={}
#     #Διαβάζουμε και ταξινομούμε όλα τα αρχεία που ξεκινούν με ta και βρίσκονται στον φάκελο Tailars-PFSP
#     for fn in sorted(glob.glob('./dataSet/I_*')):
#         arxeia[i]=fn
#         print("File:[%i](%s)"%(i,arxeia[i]) )
#         i=i+1
#     arxeio = 0    
#     #Ο χρήστης καλείται να πληκτρολογήσει έναν αριθμό για να επιλέξει ένα από τα αρχεία που εμφανίζονται στην οθόνη
#     arxeio=input("ΔΙΑΛΕΞΕ ΕΝΑ ΑΡΧΕΙΟ:")    

#     #επιστρέγει το αρχείο που επιλέγει ο χρήστης
#     return arxeia[int(arxeio)]


def load_files():
    i=1
    #Δημιουργούμε μια δομή λεξικού της python στην οποία θα αποθηκεύσουμε τα ονόματα των αρχείων
    arxeia={}
    #Διαβάζουμε και ταξινομούμε όλα τα αρχεία που ξεκινούν με ta και βρίσκονται στον φάκελο Tailars-PFSP


    files_ta = glob.glob('./dataSet/Ta*')
    files_i = glob.glob('./dataSet/I_*')

    all_files = sorted(files_ta + files_i)

    for fn in all_files:
        arxeia[i]=fn
        i=i+1
    #επιστρέγει το αρχείο που επιλέγει ο χρήστης
    #print(len(arxeia))
    return arxeia



def read_dpfsp_dataset(txtfile):
    p={}
    d={}
    with open(txtfile, 'r') as fl:
        lines = fl.readlines()
    n, m = map(int, lines[0].split()) 
    F = int(lines[1]) 
    for j in range(n+1):
        for i, t in enumerate(map(int, lines[j+1].split()[1::2])):
            p[j-1,i]=int(t)
                     
    #print("----------------------------")
    for j in range(n):
        for i, duetime in enumerate(map(int, lines[j+3+n].split())):
            d[j]=int(duetime)
                    
    
    return n, m, F, p, d
