import utils
import numpy as np
import calcShedule as cS
#=======================================================================================================
#                    ΠΡΟΓΡΑΜΜΑ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΣΠΟΥΔΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΔΙΚΤΥΩΝ
#                                    ΠΑΝΕΠΙΣΤΗΜΙΟ ΙΩΑΝΝΙΝΩΝ
#
#                      Distributed Permutation Flow-Shop Scheduling Problem
#
#********************************************************************************************************
#                                   ΚΙΟΣΣΕΣ ΔΗΜΗΤΡΙΟΣ ΑΜ 163
#********************************************************************************************************
#                                           nehedd.py
# Ταξινομούμε τις εργασίες σύμωνα με το duedate.
# 1 - Παίρνουμε την πρώτη εργασία και την τοποθετούμε σε όλες τις πιθανές θέσεις του εργοστασίου 1
# 2 - Κρατάμε το καλύτερο ζευγάρι στο εργοστάσιο 1.
# 3 - Βρίσκουμε το επόμενο καλύτερο ζευγάρι και το τοποθετούμε στο εργοστάσιο 2
# 4 - Κάθε επόμενη εργασία εξετάζεται και στα δύο εργοστάσια και τοποθετείται στο εργοστάσιο με το 
#     μικρότερο duedate error.  
#********************************************************************************************************

def nehedd_2(duedate, jobs, machines, p, Factories):
    startSeq = utils.sort_by_dueDates(duedate) #ΤΑΞΙΝΟΜΗΣΗ ΜΕ ΒΑΣΗ ΤΙΣ ΤΙΜΕΣ DUEDATES
    FactorySeq={}
    FactoryC={}  
    WorkSeq={}
    bestSequense={}

    for j in range(Factories):
        FactorySeq[j] = []



   
    workSequense = [startSeq[0]]


    bestTime=float("inf") #Δίνουμε αρχική τιμή στον καλύτερο χρόνο μια πολύ μεγάλη τιμή 
    for i in range(0, jobs):      
        for f in range(Factories):
            tmpTime=0
            for n in range(0, jobs):
                tmpTime=0
                if i != n:
                    print("i=",i, "n=", n)
                    WorkSeq = [i,n]
                    FactoryC = cS.schedule(jobs, machines, p, WorkSeq)
                    #print(FactoryC)
                    for idx, s in enumerate(WorkSeq):
                        sTime = 0
                        #print("FACTORY C makespan=", FactoryC[s,machines-1], "DUEDATE=", duedate[s]) 
                        sTime = FactoryC[s,machines-1] - duedate[s]
                        if sTime > 0:
                            tmpTime = tmpTime + sTime
                            #print("tmpTime =", tmpTime)
                        #print("tmpTime = ", tmpTime)
                        #print('makespan = ', tmpTime, duedate[j])
                    #print("Total Time =", tmpTime)
                    if bestTime > tmpTime:
                        bestTime = tmpTime
                        bestSequense = WorkSeq
                    #print("BEST TIME", bestTime)    
                FactorySeq[f] =  bestSequense          
    return FactorySeq