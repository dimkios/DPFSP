import loadfile as lf

import nehedd_new as nhd_n
import calcShedule as cS
import time

#=======================================================================================================
#                    ΠΡΟΓΡΑΜΜΑ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΣΠΟΥΔΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΔΙΚΤΥΩΝ
#                                    ΠΑΝΕΠΙΣΤΗΜΙΟ ΙΩΑΝΝΙΝΩΝ
#
#                      Distributed Permutation Flow-Shop Scheduling Problem
#
#********************************************************************************************************
#                                   ΚΙΟΣΣΕΣ ΔΗΜΗΤΡΙΟΣ ΑΜ 163
#********************************************************************************************************
#                                           main.py
#********************************************************************************************************
#                         
#========================================================================================================

#ΕΠΙΛΟΓΗ DATASET

#ΦΟΡΤΩΣΗ DATASET
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Large/Ta012_6.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Large/Ta083_4.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Large/Ta012_6.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_1.txt')
n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_8_5_1.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_6_2_1.txt')


#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_3_4_4_4.txt')

#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_5_1.txt')
n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_5_4.txt')

#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/test.txt')

startSeq = {}
#print(n)
#print(m)
#print(F)
#print(p)
#print(d)

#************************************ LOAD DATASET ******************************************************************
#               Φόρτωση δεδομένων από αρχεία. Αρχικώς χρησιμοποιούμε ένα ένα τα αρχεία
#           Στην συνέχεια θα δοθούν επιλογές για το ποιά αρχεία θα φορτώσουμε καθώς επίσης και δυνατότητα
#           φόρτωσης ενός συνόλου αρχείων.
#********************************************************************************************************************

print("============ dataset loaded ===============")
for j in range(n):
    print("job=[",j,"]",  end="", flush=True)
    for i in range(m):
        print("machine=[", i,"] -> ", p[j,i], "-", end="", flush=True)
    print("duedate = ",j, d[j], "", end="", flush=True) 
    print() 
print("============================================")   

#************************************ SOLUTION neh update ******************************************************************
#               ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΚΑΛΥΤΕΡΗΣ ΑΚΟΛΟΥΘΙΑΣ ΣΥΜΦΩΝΑ ΜΕ ΤΟΝ NEHEDD όπως περιγράφεται στην εργασία
# 1. Δημιουργείται η ακολουθία startSeq σύμφωνα με την ταξινόμηση με το duedate. 
# 2. Αρχικοποιούμε για κάθε εργοστάσιο με αρχικές ακολουθίες (στην αρχή μηδενικές)
# 3. Για κάθε εργασία j της ακολουθίας -> 
# 4. Για κάθε εργοστάσιο δοκιμάζουμε την εργασία j σε όλες τις πιθανές θέσεις υπολογίζοντας κάθε φορά την καθυστέρηση
# 5. Βρίσκουμε το εργοστάστιο με την μικρότερη καθυστέρηση
# 6. Τοποθετούμε την εργασία στο εργοστάσιο με την μικρότερη καθυστέρηση στην κατάλληλη θέση
#********************************************************************************************************************

startSeq = nhd_n.nehedd(d,n,m,p,F) 
print("------------------------------------------------")

sumTT = 0
for fn in range(F):
    FactoryC = cS.schedule(n, m, p, startSeq[fn])
    print("FACTORY : [", fn ,"] -> ",startSeq[fn])
    inTT = 0
    for idJob, job in enumerate(startSeq[fn]):
        inTT = FactoryC[startSeq[fn][idJob],-1] -  d[job]
        if(inTT > 0):
            sumTT = sumTT + inTT
    sumTT - sumTT + sumTT
print("SUMTT :", sumTT)


#ΕΞΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ


