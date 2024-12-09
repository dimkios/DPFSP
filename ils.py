import utils
import numpy as np
import calcShedule as cS
import random as rand
import copy
#=======================================================================================================
#                    ΠΡΟΓΡΑΜΜΑ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΣΠΟΥΔΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΔΙΚΤΥΩΝ
#                                    ΠΑΝΕΠΙΣΤΗΜΙΟ ΙΩΑΝΝΙΝΩΝ
#
#                      Distributed Permutation Flow-Shop Scheduling Problem
#
#********************************************************************************************************
#                                   ΚΙΟΣΣΕΣ ΔΗΜΗΤΡΙΟΣ ΑΜ 163
#********************************************************************************************************
#                                           ILS.py
# Υπολογισμός Random Subsequence Local Search
#********************************************************************************************************

def ils(d,n,m,p,startSeq, bestTT):
    startSeqIls = copy.deepcopy(startSeq)
    startBest = bestTT
    bestTTnew = bestTT

    helpSeq ={}
    tempVal = 0
    fact1 = None
    fact2 = None

    f=0
    seqNr1 = 0
    seqNr2 = 0

    f=len(startSeqIls)

    fact1 = rand.randint(0, f-1)
    fact2 = rand.randint(0, f-1)
    while (fact1 == fact2):
           fact2 = rand.randint(0, f-1)  

    #print("FACTORY 1 =", fact1)
    #print("FACTORY 2 =", fact2)

    #print("------------------------------------------------")

    
    seqNr1 = len(startSeqIls[fact1])
    randomSeq1 = rand.randint(0, seqNr1-1)

    seqNr2 = len(startSeqIls[fact2])
    randomSeq2 = rand.randint(0, seqNr2-1)

    tempVal = startSeqIls[fact1][randomSeq1]
    startSeqIls[fact1][randomSeq1] =  startSeqIls[fact2][randomSeq2]
    startSeqIls[fact2][randomSeq2] =  tempVal

    bestTTnew = cS.calcTT(d,n,m,p,startSeqIls)
    
    if bestTTnew < bestTT:
        #print("START BEST:",startBest,"NEW BEST: ", bestTTnew)
        bestTT = bestTTnew
        return bestTTnew, startSeqIls
    else:
        return bestTT, startSeqIls