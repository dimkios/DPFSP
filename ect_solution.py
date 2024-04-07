import numpy as np
import random

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
#                           Solution based on earlier completion time 
#
#========================================================================================================

def ect_solution(duedate, jobs, machines, p, Factories):
    startSeq = {}
    startSeq = [4,3,2,1,0]
    #startSeq = [4,3,2,1,0]
    startSeq = [19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
    #startSeq = [0,1,2,3,4,5,6,7]
    FactorySeq={}
    FactoryRound={}
    FactoryPointer={}
    FactoryC={}
    timi = 0
    #FactoryMJ={}
    #best_Ect = float("inf")

    print(jobs,machines, Factories)

    C = np.zeros((jobs, machines))

    for j in range(Factories):
        FactoryC[j] = np.zeros((jobs, machines))
        FactorySeq[j] = []
        FactoryRound[j] = []

  

    for idx, j in enumerate(startSeq):
        for f in range(Factories):
            pointer = ((np. count_nonzero(FactoryC[f]))/machines)
            #print("pointer=", pointer)
            poi = int(pointer)
            #print("poi = ",poi)
            for i in range(machines):
                #FactoryC[f][p,i] = random.randint(1,20)
                if idx == 0: #Εάν εξετάζουμε την πρώτη εργασία της ακολουθίας
                    if i==0: #Εάν βρισκόμαστε στην πρώτη μηχανή
                        FactoryC[f][poi,i] = p[j,i] #Αντιστοιχούμε την αρχική τιμή  
                    else:
                        FactoryC[f][poi,i] = FactoryC[f][poi,i-1] + p[j,i] #Για τις επόμενες μηχανές και την πρώτη εργασία, αθροίζουμε την τρέχουσα τιμή με την προηγούμενη τιμή                     
                else:
                    if i == 0: #Εάν δεν βρισκόμαστε στην πρώτη εργασία της ακολουθίας αλλά στην πρώτη μηχανή
                        FactoryC[f][poi,i] = FactoryC[f][poi-1,i] + p[j,i] # Αθροίζουμε την τρέχουσα τιμή με την προηγούμενη εργασία στην ίδια μηχανή    
                        #print("FACTORY FactoryC[f][poi-1,i]",poi-1,"",i,"->",FactoryC[f][poi-1,i],"+ p[j,i]",j,i,p[j,i])               
                    else:
                        #Αλλιώς επιλέγουμε την μεγαλύτερη τιμή ανάμεσα στην τιμή του χρόνου της εργασίας στην προηγούμενη μηχανή και του χρόνου της προηγούμενης εργασίας στην ίδια μηχανή
                        #και το αθροίζουμε με τον τρέχων χρόνο εργασίας
                        FactoryC[f][poi,i] = max(FactoryC[f][poi,i-1], FactoryC[f][poi-1,i]) + p[j,i]    
                        #print("FACTORY  FactoryC[f][poi-1,i]----> max of",FactoryC[f][poi,i-1]," or",FactoryC[f][poi-1,i],"+",p[j,i] )  
            FactoryRound[f] = FactoryC[f][poi,i]
            FactoryPointer[f] = poi
            
        print("=================================================================================")
        print(FactoryRound)   
        print(min(FactoryRound, key=FactoryRound.get))
        
        bestinRound = min(FactoryRound, key=FactoryRound.get)
        print("best in round =",bestinRound)
        FactorySeq[bestinRound].append(j)
        for fctr in range(Factories):
            
            if fctr != bestinRound:
                for imach in range(machines):
                    FactoryC[fctr][FactoryPointer[fctr], imach] = 0
            print("Factory = ", fctr)
            print("job=", j)
            print(FactoryC[fctr])
        print("*************************** end of Factories round ******************************")   

    for fctr in range(Factories):
        print("Job Sequence on Factory: [ ",fctr," ]", FactorySeq[fctr])