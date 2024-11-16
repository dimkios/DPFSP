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
#                                           rsls.py
# Υπολογισμός Random Subsequence Local Search
#********************************************************************************************************

def rsls_II(d,n,m,p,startSeq, bestTT):

    startBest = bestTT      #best Starting Time = bestTT
    bestTTnew = bestTT      #best TT new = bestTT
    helpSeq ={}
    subSeq = {}
    bestRSLSseq = {}
    element1 = None
    element2 = None
    subseqLen = None
    fact = None
    fact1 = None
    fact2 = None
    flag = True
    #print(startSeq)
    bestRSLSseq = startSeq

    f=0
    seqNr1 = 0
    seqNr2 = 0

    v=rand.uniform(0, 1)
    w=rand.uniform(0, 1)
    
    f=len(startSeq)         #find the exact number of Factories

    while flag:
        flag = False
        if v < 0.5:
            #print("====")
            fact = rand.randint(0, f-1)     #Select one factory randomly

            # Choose a subSequence and insert it in a randomly startpoint
            if w < 0.5:     
                #print("EXTRACT 1 ELEMENT AND ADD IT ON OTHER POSITION") 
                if (len(startSeq[fact])>2):
                    position1 = rand.randint(1, len(startSeq[fact])-1)
                    position2 = rand.randint(1, len(startSeq[fact])-1)
                    while (position1 == position2):
                        position2 = rand.randint(1, len(startSeq[fact])-1)
                        #print("--------------- element 1", position1, "with value=", startSeq[fact][position1], "AND POSITION 1 =", position2)
                    element1 = startSeq[fact].pop(position1)
                    startSeq[fact].insert(position2, element1)
                    #print("move element",startSeq)
            else:
                #print("SWAP TWO ELEMENTS")
                if (len(startSeq[fact])>2):
                    position1 = rand.randint(1, len(startSeq[fact])-1)
                    position2 = rand.randint(1, len(startSeq[fact])-1)
                    while (position1 == position2):
                        position2 = rand.randint(1, len(startSeq[fact])-1)  
                    #print("element 1", position1, "with value=", startSeq[fact][position1], "AND POSITION 1 =", position2)
                    startSeq[fact][position1], startSeq[fact][position2] = startSeq[fact][position2], startSeq[fact][position1]
                    #print("swap elements",startSeq)
        else:
            #print("Select 2 factories, CHOOSE ELEMENT FROM FACTORY 1 AND PUT IT ON RANDOM POSITION IN FACTPORY 2")
            fact1 = rand.randint(0, f-1)
            fact2 = rand.randint(0, f-1)
            while (fact1 == fact2):
                fact2 = rand.randint(0, f-1)  
            if w < 0.5:
                #print("EXTRACT RANDOM ELEMENT FROM FACTORY 1 AND PUT IT IN RANDOM POSITION ON FACTORY 2")
                if len(startSeq[fact1]) < len(startSeq[fact2]):
                    value = fact1
                    fact1 = fact2
                    fact2 = value
                if (len(startSeq[fact1])>1) and (len(startSeq[fact2])>1):
                    position1 = rand.randint(0, len(startSeq[fact1])-1)
                    position2 = rand.randint(0, len(startSeq[fact2])-1)
                    #print("element 1", position1, "with value=", startSeq[fact1][position1], "AND POSITION 1 =", position2)
                    #print("element 1", position1, "AND POSITION 2 =", position2)
                    element1 = startSeq[fact1].pop(position1)
                    startSeq[fact2].insert(position2, element1)
                    #print("put from 1 fact to other", startSeq)
            else:
                #print("SWAP ONE ELEMENT FROM FACTORY 1 WITH ONE RANDOM ELEMENT IN FACTORY 2")
                #print("Fact1",startSeq[fact1])
                #print("Fact2",startSeq[fact2])
                if (len(startSeq[fact1])>1) and (len(startSeq[fact2])>1):
                    position1 = rand.randint(0, len(startSeq[fact1])-1)
                    position2 = rand.randint(0, len(startSeq[fact2])-1)
                    startSeq[fact1][position1], startSeq[fact2][position2] = startSeq[fact2][position2], startSeq[fact1][position1]
                    #print("swap 1 fact to other", startSeq)                                                                                                    
        bestTTnew = cS.calcTT(d,n,m,p,startSeq)
        if bestTTnew < bestTT:
            #print("START BEST:",startBest,"NEW BEST: ", bestTTnew)
            #print("SEQUENCE", startSeq,"START BEST:",startBest,"NEW BEST: ", bestTTnew)
            bestTT = bestTTnew
            bestRSLSseq = copy.deepcopy(startSeq) 
            flag = True
    return bestTT, bestRSLSseq 
