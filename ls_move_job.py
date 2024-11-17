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
#                                           ls_move_job.py
# Επιλέγουμε το εργοστάσιο με την μεγαλύτερη καθυστέρηση (maxFact) και το εργοστάσιο με την μικρότερη 
# καθυστέρηση (minFact) Εξετάζουμε κάθε εργασία του maxFact σε όλες τις θέσεις του minFact
# Εάν η καθυστέρηση στο minFact είναι μικρότερη από την καθυστέρηση στο maxFact ddMax αλλάζουμε θέση στην 
# εργασία.
#********************************************************************************************************

def ls_move_job(d,n,m,p,Factories,startSeqls):
    #print(startSeqls)
    flag = True
    flag2 = True
    maxTT = 0
    minTT = 0
    maxFact = None
    minFact = None 
    TTvalues = {}


    selJobs = {}                    #ΘΕΣΕΙΣ ΜΕ ΕΡΓΑΣΙΕΣ ΠΟΥ ΘΑ ΑΦΑΙΡΕΘΟΥΝ
    inJobs = {}                     #ΟΙ ΤΙΜΕΣ ΤΩΝ ΕΡΓΑΣΙΩΝ ΠΟΥ ΠΡΕΠΕΙ ΝΑ ΠΡΟΣΤΕΘΟΎΝ
    workSequensels = {}             #ΑΚΟΛΟΥΘΙΑ ΠΟΥ ΕΠΕΞΕΡΓΑΖΟΜΑΣΤΕ
    
    while flag:
        flag = False
        for f1 in range(Factories):
            TTnew = cS.calcTToneFact(d,n,m,p,startSeqls[f1])
            TTvalues[f1] = TTnew
            #print("FACTORY:", f1, "sequence:", startSeqls[f1], "TT" ,TTnew)

        TTvaluesList = list(TTvalues.values())
        min_value = min(TTvaluesList)
        max_value = max(TTvaluesList)
        min_index = TTvaluesList.index(min_value)
        max_index = TTvaluesList.index(max_value)
        #print("MAX FACT =", max_index, "me timi ddMAX", max_value)
        #print("MIN FACT =", min_index, "me timi ddMAX", min_value)
        flag2 = True
        for j in range(len(startSeqls[max_index])):
            if flag2:
                #print("each JOB:", j)
                jobstoCH = len(startSeqls[min_index])
                #bestTT = float("inf")
                for g in range(0, jobstoCH+1):
                    #print("g =", g)
                    tmp_seqlsMOVE = utils.insertion(startSeqls[min_index], g, startSeqls[max_index][j])
                    #print(tmp_seqlsMOVE)
                    timiTTmove = cS.calcTToneFact(d,n,m,p, tmp_seqlsMOVE)
                    #print(timiTTmove)
                    if(timiTTmove<max_value):
                        #print()
                        #print("BEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEESt")
                        #print(tmp_seqlsMOVE)
                        bestSequence = tmp_seqlsMOVE
                        startSeqls[min_index].insert(g, startSeqls[max_index][j])
                        startSeqls[max_index].remove(startSeqls[max_index][j])
                        #print(startSeqls[min_index])
                        #print(startSeqls[max_index])
                        max_value = timiTTmove
                        flag = True
                        flag2 = False
                        break
                

    #print(startSeqls)
    bestTTnewMOVE = cS.calcTT(d,n,m,p,startSeqls)
    return bestTTnewMOVE, startSeqls

            #workSequensels = bestSequence 