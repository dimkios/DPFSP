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

def rsls(d,n,m,p,startSeq, bestTT):

    startBest = bestTT      #best Starting Time = bestTT
    bestTTnew = bestTT      #best TT new = bestTT
    helpSeq ={}
    bestRSLSseq = {}
    subSeq = {}
    subSeq1 = {}
    subSeq2 = {}
    tempVal = 0
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
            fact = rand.randint(0, f-1)     #Select one factory randomly

            # Choose a subSequence and insert it in a randomly startpoint
            if w < 0.5:   
                #print("FACTORY:", startSeq[fact]) 
                if(len(startSeq[fact])<2):
                    subseqLen = 1
                else:              
                    subseqLen = rand.randint(1, len(startSeq[fact])-1)
                #print("SUBSEQLEN", subseqLen)
                startpoint = rand.randint(0, len(startSeq[fact])-subseqLen)
                #print("STARTPOINT =", startpoint)
                subSeq = startSeq[fact][startpoint:subseqLen+startpoint]
                del startSeq[fact][startpoint:subseqLen+startpoint]

                #print("SUBSEQ:", subSeq, len(startSeq[fact]))


                if len(startSeq[fact]) < 2:
                    newInsertPoint = 1
                else:
                    newInsertPoint = rand.randint(0, len(startSeq[fact])-1)
                new_list = startSeq[fact][:newInsertPoint] + subSeq + startSeq[fact][newInsertPoint:]
                #print("FACTORIE : ", fact, "***",startSeq[fact]," *** SUBSEQLEN ----------->", subseqLen, "STARTPOINT:", startpoint , "SUBSEQUENCE =", subSeq, "NEWINSERTPOINT= ", newInsertPoint)
                startSeq[fact] = new_list  
                #print("NEW startSEQ", startSeq)  
            # Choose a subSequence and reverse it    
            else:
                #print("select subsequence and update sequence") 
                if len(startSeq[fact]) < 2:
                    subseqLen = 1
                else:
                    subseqLen = rand.randint(1, len(startSeq[fact])-1)
                startpoint = rand.randint(0, len(startSeq[fact])-subseqLen)
                startSeq[fact][startpoint:subseqLen+startpoint+1] = startSeq[fact][startpoint:subseqLen+startpoint+1][::-1] 
                #print("startSeq", startSeq)
        # Choose two factories randomly        
        else:
            #print("Select 2 factories")
            fact1 = rand.randint(0, f-1)
            fact2 = rand.randint(0, f-1)
            while (fact1 == fact2):
                fact2 = rand.randint(0, f-1) 

            
            #print("Choose subsequence and Starting point on each Factory [", fact1, "] - [", fact2 , "]")  
            #Select the less nr of jobs
            if(len(startSeq[fact1]) > len(startSeq[fact2])):
                subMaxLength = len(startSeq[fact2])
            else:
                subMaxLength = len(startSeq[fact1])     
                #print("MAXLENGTH = ", subMaxLength)   
            if  subMaxLength < 2:                                               #The nr of Jobs to be moved
                subseqLen = 1
            else:
                subseqLen = rand.randint(1, subMaxLength-1)                         #Length of Sub Sequence
            startpoint = rand.randint(0, subMaxLength-subseqLen)                #Start point to cut the sub sequence

            subSeq1 = startSeq[fact1][startpoint:subseqLen+startpoint]          #Select Subsequence of factory 1
            subSeq2 = startSeq[fact2][startpoint:subseqLen+startpoint]          #Select Subsequence of factory 2

            #print("subSeq1", subSeq1)
            #print("subSeq2", subSeq2)


            if w < 0.5:
            #print("SWAP SUB SEQUENCE BETWEEN FACTORIES")
                del startSeq[fact1][startpoint:subseqLen+startpoint]            #delete the subsequence of fact1
                del startSeq[fact2][startpoint:subseqLen+startpoint]            #delete the subsequence of fact1
                new_list1 = startSeq[fact1][:startpoint] + subSeq2 + startSeq[fact1][startpoint:]   #move the subsequence 2 in a temporary variable list 1
                new_list2 = startSeq[fact2][:startpoint] + subSeq1 + startSeq[fact2][startpoint:]   #move the subsequence 1 in a temporary variable list 2
                startSeq[fact1] = new_list1                                     #update the lists. Move the sequence from factory 1 to factory 2
                startSeq[fact2] = new_list2                                     #update the lists. Move the sequence from factory 2 to factory 1
                #print("NEW FACTORY = ", fact1, "--> [", startSeq[fact1], "]")
                #print("NEW FACTORY = ", fact2, "--> [", startSeq[fact2], "]")
            else:
                #print("SWAP AND REVERSE THE SUBSEQUENCE")
                subSeq1.reverse()
                subSeq2.reverse()

                del startSeq[fact1][startpoint:subseqLen+startpoint]            #delete the subsequence of fact1
                del startSeq[fact2][startpoint:subseqLen+startpoint]            #delete the subsequence of fact1
                new_list1 = startSeq[fact1][:startpoint] + subSeq2 + startSeq[fact1][startpoint:]   #move the subsequence 2 in a temporary variable list 1
                new_list2 = startSeq[fact2][:startpoint] + subSeq1 + startSeq[fact2][startpoint:]   #move the subsequence 1 in a temporary variable list 2
                startSeq[fact1] = new_list1                                     #update the lists. Move the sequence from factory 1 to factory 2
                startSeq[fact2] = new_list2                                     #update the lists. Move the sequence from factory 2 to factory 1
                #print("NEW FACTORY = ", fact1, "--> [", startSeq[fact1], "]")
                #print("NEW FACTORY = ", fact2, "--> [", startSeq[fact2], "]")
        bestTTnew = cS.calcTT(d,n,m,p,startSeq)
        if bestTTnew < bestTT:
            #print("SEQUENCE", startSeq,"START BEST:",startBest,"NEW BEST: ", bestTTnew)
            bestTT = bestTTnew
            bestRSLSseq = copy.deepcopy(startSeq) 
            flag = True
    return bestTT, bestRSLSseq