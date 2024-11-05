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
#                                           neh.py
# Συνάρτηση που βασίζεται στην λογική του αλγόριθμου NEH και υπολογίζει μια βέλτιστη ακολουθία εργασιών
#********************************************************************************************************

def neh(duedate, jobs, machines, p, Factories):
    startSeq = utils.sort_by_dueDates(duedate) #ΤΑΞΙΝΟΜΗΣΗ ΜΕ ΒΑΣΗ ΤΙΣ ΤΙΜΕΣ DUEDATES
    FactorySeq={}
    FactoryC={}  
    WorkSeq={}
    bestSequense={}
    TmpSeq={}                   #Χρόνοι εκτέλεσης των εργασιών σε ένα εργοστάστιο για μια συγκεκριμένη εργασία

    workSequense = [startSeq[0]]

    #for j in range(Factories):
        #FactorySeq[j] = []
        #WorkSeq[j]=[]
        #TmpSeq[j]=[]    
        #FactoryC[j] = np.zeros((jobs, machines))

    #print("test =>",startSeq)

    for i in range(1, jobs):      
        bestTime=float("inf") #Δίνουμε αρχική τιμή στον καλύτερο χρόνο μια πολύ μεγάλη τιμή 
        tmpTime=0
        for j in range(0, i + 1):  
            WorkSeq = utils.insertion(workSequense, j, startSeq[i])
            #print(WorkSeq)
            FactoryC = cS.schedule(jobs, machines, p, WorkSeq)
            tmpTime = cS.makespan(WorkSeq,  FactoryC)
            #print('makespan = ', tmpTime, duedate[j])
            if bestTime > tmpTime:
                bestTime = tmpTime
                bestSequense = WorkSeq
        workSequense =  bestSequense       

    #Sprint(workSequense)

    return workSequense