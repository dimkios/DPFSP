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
#                                           ls_exchange_job.py
# Επιλέγουμε το εργοστάσιο με την μεγαλύτερη καθυστέρηση (maxFact) και το εργοστάσιο με την μικρότερη 
# καθυστέρηση (minFact) Εξετάζουμε κάθε εργασία του maxFact σε όλες τις θέσεις του minFact
# Εάν η καθυστέρηση στο minFact είναι μικρότερη από την καθυστέρηση στο maxFact ddMax αλλάζουμε θέση στην 
# εργασία.
#********************************************************************************************************

def ls_exchange_job(d,n,m,p,Factories,startSeqls):
    #print(startSeqls)
    flag = True
    flag2 = True
    TTvalues = {}
       
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
            #print("each JOB:", j)
            for i in range(len(startSeqls[min_index])):
                originalMAX = startSeqls[max_index][j]
                originalMIN = startSeqls[min_index][i]  # Αποθηκεύουμε το αρχικό στοιχείο (αν χρειάζεται)
                startSeqls[min_index][i] = originalMAX
                startSeqls[max_index][j] = originalMIN

                #print(f"Λίστα μετά την αντικατάσταση στη θέση {i}: {startSeqls[min_index][i]}")
                #print("MAX Fact:", startSeqls[max_index], "MIN Fact:", startSeqls[min_index])

                timiTTMAX = cS.calcTToneFact(d,n,m,p, startSeqls[max_index])
                timiTTMIN = cS.calcTToneFact(d,n,m,p, startSeqls[min_index])

                if (timiTTMAX < max_value) and (timiTTMIN < max_value):
                    #print("BEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEST")
                    #print("timiTTMAX =",timiTTMAX, "timiTTMIN =",timiTTMIN,"maxValue:", max_value)
                    max_value = max(timiTTMAX, timiTTMIN)
                    break
                # Επαναφορά για να συνεχιστεί ο βρόχος (προαιρετικό)
                startSeqls[min_index][i] = originalMIN  # Αν θέλετε να κρατάτε μόνο μία αλλαγή τη φορά
                startSeqls[max_index][j] = originalMAX
             
    #print(startSeqls)
    bestTTnewMOVE = cS.calcTT(d,n,m,p,startSeqls)
    return bestTTnewMOVE, startSeqls
