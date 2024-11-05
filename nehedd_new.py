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
#                                           nehedd_new.py
# Συνάρτηση που βασίζεται στην λογική του αλγόριθμου NEH και υπολογίζει μια βέλτιστη ακολουθία εργασιών
#********************************************************************************************************

def nehedd(duedate, jobs, machines, p, Factories):

    FactorySeq ={}
    FactoryWorkSeq ={}
    FactoryWorkTime ={}
    FactoryC ={}
    
    #ΤΑΞΙΝΟΜΗΣΗ ΜΕ ΒΑΣΗ ΤΙΣ ΤΙΜΕΣ DUEDATES
    startSeq = utils.sort_by_dueDates(duedate) 
    print("ΤΑΞΙΝΟΜΗΣΗ ΕΡΓΑΣΙΩΝ ΣΥΜΦΩΝΑ ΜΕ ΤΑ DUE DATES", startSeq)

    #workSequense = [startSeq[0]]

    #ΑΡΧΙΚΟΠΟΙΗΣΗ ΕΡΓΟΣΤΑΣΙΩΝ
    for f in range(Factories):
        FactoryC[f] = np.zeros((jobs, machines))                #Αρχικοποίηση πίνακα με τους χρόνους τερμαρισμού ακολουθιών 
        FactorySeq[f] = []                                      #Αρχικοποίηση πίνακα με τις ακολουθίες κάθε εργοστασίου
        FactoryWorkSeq[f] = [startSeq[f]]                       #Αρχικοποίηση βοηθητικού πίνακα με ακολουθίες για ενδιάμεσες τιμές 
        FactoryWorkTime[f] = 0                                  #Αρχικοποίηση βοηθητικού πίνακα για ενδιάμεσες τιμές καθυστερήσεων
        startpoint = f+1                                        #Σημείο έναρξης τοποθέτησης επιπλέον εργασιών. Οι πρώτες εργασίες τοποθετούνται
                                                                #μια μια στα εργοστάσια μέχρι κάθε εργοστάσιο να έχει από μια εργασία.
        #print("Intitial Factory [", f ,"] :", FactorySeq[f])
        #print("startpoint = ", startpoint)

    # Τοποθέτηση πρώτων εργασιών στα εργοστάσια
    for f in range(Factories):                                  
        FactorySeq[f] = FactoryWorkSeq[f]
        print(FactoryWorkSeq[f])

    x=1
    pointer2 = 2
    #print("pointer", pointer2)

    print("----start calc NEHedd----") 
    #Ξεκινάμε να επεξεργαζόμαστε τις εργασίες από το startpoint και μετά
    for i in range(startpoint, jobs):
        bestTime=float("inf") #Δίνουμε αρχική τιμή στον καλύτερο χρόνο μια πολύ μεγάλη τιμή
        bestFactoryTime = float("inf")
        
        for fnew in range(Factories):
            #print("==== F A C T O R Y : [", fnew, "] ====" )
            FactoryWorkSeq[fnew] = FactorySeq[fnew]
            #print("FACTORY:", FactorySeq[fnew])
            pointer2 = len(FactorySeq[fnew])+1
            #print("length")
            #print(len(FactorySeq[fnew]))
            #print()
            #print( FactoryWorkSeq[fnew])
            #print()
            for x in range(0, pointer2): 
                #print("JOB ΤΟ POSITIONING: [", startSeq[i], "]" )
                #print("FactoryWorkSeq[f] : [", FactoryWorkSeq[fnew],"] x=", x, " - startSeq[i] : ",  startSeq[i]) 
                WorkSeq = utils.insertion(FactoryWorkSeq[fnew] , x, startSeq[i])
                #print("WorkSeq : ", WorkSeq)
                FactoryC = cS.schedule(jobs, machines, p, WorkSeq)
                inTT = 0
                sumTT = 0
                for idJob, job in enumerate(WorkSeq):
                    inTT = FactoryC[WorkSeq[idJob],-1] -  duedate[job]
                    #print("inTT :", inTT)
                    if(inTT > 0):
                        sumTT = sumTT + inTT
                #print("SUMTT :", sumTT)
                if bestTime > sumTT:
                    bestTime = sumTT
                    bestSequense = WorkSeq
            FactoryWorkTime[fnew] = bestTime            
            FactoryWorkSeq[fnew] = bestSequense

            #print("BEST TIME", bestTime, "---- BEST SEQUENSE:" , bestSequense)

            if bestFactoryTime > FactoryWorkTime[fnew]:
                bestFactoryTime = FactoryWorkTime[fnew]
                bestPointer = fnew
            #print("factorySeq[fnew] = ", FactoryWorkSeq[bestPointer] ,[bestPointer])
            #print("factoryWork = ", FactoryWorkSeq[bestPointer], "with TT = [", FactoryWorkTime[bestPointer], "]")
            #FactorySeq[fnew] = FactoryWorkSeq[fnew]
        pointer2=pointer2+1
        #print("bestPointer :", bestPointer)
        FactorySeq[bestPointer] = FactoryWorkSeq[bestPointer]
        #print("---------------------------------")
        #print("-----[", bestPointer ,"]----", FactoryWorkSeq[bestPointer], "-----")
        #print("---------------------------------")
    #print("++++==========================================================================++++++")
    return FactorySeq