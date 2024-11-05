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
# Συνάρτηση που βασίζεται στην λογική του αλγόριθμου NEH και υπολογίζει μια βέλτιστη ακολουθία εργασιών
#********************************************************************************************************

def nehedd(duedate, jobs, machines, p, Factories):
    startSeq = utils.sort_by_dueDates(duedate) #ΤΑΞΙΝΟΜΗΣΗ ΜΕ ΒΑΣΗ ΤΙΣ ΤΙΜΕΣ DUEDATES
    #print(" ====== START SEQUENSE =", startSeq)
    FactorySeq={}
    FactoryC={}  
    WorkSeq={}
    bestSequense={}
    TmpSeq={}                   #Χρόνοι εκτέλεσης των εργασιών σε ένα εργοστάστιο για μια συγκεκριμένη εργασία

    workSequense = [startSeq[0]]

    for i in range(1, jobs):      
        bestTime=float("inf") #Δίνουμε αρχική τιμή στον καλύτερο χρόνο μια πολύ μεγάλη τιμή 
        tmpTime=0
        for j in range(0, i + 1):  
            tmpTime=0
            #print("workSequense : [", workSequense,"] j=", j, " - startSeq[i] : ",  startSeq[i])
            WorkSeq = utils.insertion(workSequense, j, startSeq[i])
            #print(WorkSeq)
            FactoryC = cS.schedule(jobs, machines, p, WorkSeq)
            #print("FactoryC:", FactoryC)
            for idx, s in enumerate(WorkSeq):
                sTime = 0
                #print("FACTORY C makespan=", FactoryC[s,machines-1], "DUEDATE=", duedate[s]) 
                sTime = FactoryC[s,machines-1] - duedate[s]
                if sTime > 0:
                    tmpTime = tmpTime + sTime

            #print("tmpTime = ", tmpTime)
            #print('makespan = ', tmpTime, duedate[j])
            if bestTime > tmpTime:
                bestTime = tmpTime
                bestSequense = WorkSeq
        workSequense =  bestSequense       

    #Sprint(workSequense)
    
    #return workSequense
    return startSeq