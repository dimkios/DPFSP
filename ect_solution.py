import numpy as np

#=======================================================================================================
#                    ΠΡΟΓΡΑΜΜΑ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΣΠΟΥΔΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΔΙΚΤΥΩΝ
#                                    ΠΑΝΕΠΙΣΤΗΜΙΟ ΙΩΑΝΝΙΝΩΝ
#
#                      Distributed Permutation Flow-Shop Scheduling Problem
#
#********************************************************************************************************
#                                   ΚΙΟΣΣΕΣ ΔΗΜΗΤΡΙΟΣ ΑΜ 163
#********************************************************************************************************
#                                           main.py
#********************************************************************************************************


def ect_solution(duedate, jobs, machines, p, Factories):
    startSeq = {}
    startSeq = [4,3,2,1,0]
    FactorySeq={}
    FactoryC={}
    FactoryMJ={}
    best_Ect = float("inf")

    print(jobs,machines, Factories)

    C = np.zeros((jobs, machines))

    for j in range(Factories):
        FactoryC[j] = np.zeros((jobs, machines))
        FactoryMJ[j] = [20,20]
        FactorySeq[j] = []


    print(FactoryMJ[0])
    print(C)
    print(p)

    for idx, j in enumerate(startSeq):
        for f in range(Factories):
            for i in range(machines):
                print("Factory=",f)
                print("idx=", idx)
                print("j=",j)
                print("i=", i)
                #print("p[j,i] =", p[j,i])

                if idx == 0: #Εάν εξετάζουμε την πρώτη εργασία της ακολουθίας
                    if i==0: #Εάν βρισκόμαστε στην πρώτη μηχανή
                        FactoryC[f][j,i] = p[j,i] #Αντιστοιχούμε την αρχική τιμή  
                    else:
                        FactoryC[f][j,i] = FactoryC[f][j,i-1] + p[j,i] #Για τις επόμενες μηχανές και την πρώτη εργασία, αθροίζουμε την τρέχουσα τιμή με την προηγούμενη τιμή                     
                else:
                    if i == 0: #Εάν δεν βρισκόμαστε στην πρώτη εργασία της ακολουθίας αλλά στην πρώτη μηχανή
                        FactoryC[f][j,i] = FactoryC[f][startSeq[idx-1],i] + p[j,i] # Αθροίζουμε την τρέχουσα τιμή με την προηγούμενη εργασία στην ίδια μηχανή    
                        #print("--------",C[j,i])               
                    else:
                        #Αλλιώς επιλέγουμε την μεγαλύτερη τιμή ανάμεσα στην τιμή του χρόνου της εργασίας στην προηγούμενη μηχανή και του χρόνου της προηγούμενης εργασίας στην ίδια μηχανή
                        #και το αθροίζουμε με τον τρέχων χρόνο εργασίας
                        FactoryC[f][j,i] = max(FactoryC[f][j,i-1], FactoryC[f][startSeq[idx-1],i]) + p[j,i]    
                        print("--------",FactoryC[f][j,i])                    
                print(FactoryC[f])
        print("*************************** end of Factories round ******************************")   
        for f in range(Factories):
            if (best_Ect > FactoryC[f][j,i]):
                best_Ect = FactoryC[f][j,i]
                bestFactory = f
                print("bestTime =", FactoryC[f][j,i])
        for f in range(Factories):
            if f != bestFactory:
                FactoryC[f][j,i] = 0


    print(C)