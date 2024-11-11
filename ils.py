import utils
import numpy as np
import calcShedule as cS
import random as rand
#=======================================================================================================
#                    ΠΡΟΓΡΑΜΜΑ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΣΠΟΥΔΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΔΙΚΤΥΩΝ
#                                    ΠΑΝΕΠΙΣΤΗΜΙΟ ΙΩΑΝΝΙΝΩΝ
#
#                      Distributed Permutation Flow-Shop Scheduling Problem
#
#********************************************************************************************************
#                                   ΚΙΟΣΣΕΣ ΔΗΜΗΤΡΙΟΣ ΑΜ 163
#********************************************************************************************************
#                                           rsls.py
# Υπολογισμός Random Subsequence Local Search
#********************************************************************************************************

def ils(d,n,m,p,startSeq, bestTT):

    startBest = bestTT
    bestTTnew = bestTT
    helpSeq ={}
    tempVal = 0
    fact1 = None
    fact2 = None

    f=0
    seqNr1 = 0
    seqNr2 = 0

    f=len(startSeq)

    fact1 = rand.randint(0, f-1)
    fact2 = rand.randint(0, f-1)
    while (fact1 == fact2):
           fact2 = rand.randint(0, f-1)  

    #print("FACTORY 1 =", fact1)
    #print("FACTORY 2 =", fact2)

    #print("------------------------------------------------")

    
    seqNr1 = len(startSeq[fact1])
    randomSeq1 = rand.randint(0, seqNr1-1)

    seqNr2 = len(startSeq[fact2])
    randomSeq2 = rand.randint(0, seqNr2-1)

    tempVal = startSeq[fact1][randomSeq1]
    startSeq[fact1][randomSeq1] =  startSeq[fact2][randomSeq2]
    startSeq[fact2][randomSeq2] =  tempVal

    bestTTnew = cS.calcTT(d,n,m,p,startSeq)
    
    if bestTTnew < bestTT:
        #print("START BEST:",startBest,"NEW BEST: ", bestTTnew)
        bestTT = bestTTnew
        return bestTTnew
    else:
        return bestTT
        
    

    # for fn in range(f):    
    #     print("idFact", fn)
    #     FactoryC = cS.schedule(n, m, p, startSeq[fn])
    #     #print("FACTORY : [", fn ,"] -> ",startSeq[fn])
    #     seqNr = 0
    #     for idSeq, seq in enumerate(startSeq[fn]):
    #         seqNr = seqNr+1
    #         #print("Seq =", idSeq ,"and Seq Nr =", seqNr)
    #         #print(startSeq[fn][idSeq])

    #     #randomSeq = rand.randint(0, seqNr-1)
    #     #print("random Nr = [", randomSeq , "]")



    #     inTT = 0
    #     for idJob, job in enumerate(startSeq[fn]):
    #         inTT = FactoryC[startSeq[fn][idJob],-1] -  d[job]
    #         if(inTT > 0):
    #             sumTT = sumTT + inTT
    #     sumTT - sumTT + sumTT
    # print("SUMTT :", sumTT)
    # print("Number Of Factories", f)
    subSequence = {}
