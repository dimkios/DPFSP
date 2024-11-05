import loadfile as lf

import neh as nh
import nehedd as nhd
import tmp.nehedd_2 as nhd2
import ect_solution as ect
import dd_solution as dd
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
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_8_5_1.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_6_2_1.txt')


#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_3_4_4_4.txt')

#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_5_1.txt')
n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_5_4.txt')

#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/test.txt')

startSeq = {}
print(n)
print(m)
print(F)
print(p)
print(d)

print("============ dataset loaded ===============")
for j in range(n):
    print("job=[",j,"]",  end="", flush=True)
    for i in range(m):
        print("machine=[", i,"] -> ", p[j,i], "-", end="", flush=True)
    print("duedate = ",j, d[j], "", end="", flush=True) 
    print() 
print("============================================")   


#************************************ SOLUTION 001 **********************************************
#               ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΚΑΛΥΤΕΡΗΣ ΑΚΟΛΟΥΘΙΑΣ ΣΥΜΦΩΝΑ ΜΕ ΤΟΝ NEH
# Υπολογίζεται μια ακολουθία με τον αλγόριθμο NEH σύμφωνα με το makespan 
# Στην συνέχεια εκτελείται ο αλγόριθμος ect ο οποίος μοιράζει τις εργασίες στα εργοστάσια
# σύμφωνα με τον κανόνα earlier completion time.
# Τέλος υπολογίζεται το σφάλμα σχετικά με το duedate
#************************************************************************************************

print("------------------------- solution 001 NEH + ECT ------------------------------------------------")
startSeq = nh.neh(d,n,m,p,F) 
print(startSeq)

####ΔΙΑΜΙΡΑΣΜΟΣ ΣΤΑ ΕΡΓΟΣΤΑΣΙΑ ΣΥΜΦΩΝΑ ΜΕ ΤΗΝ ΑΚΟΛΟΥΘΙΑ ΠΟΥ ΥΠΟΛΟΓΙΣΤΗΚΕ ΠΑΡΑΠΑΝΩ
ectSequence, ectC = ect.ect_solution(d,n,m,p,F,startSeq)
dueDateFaultSum = 0
dueDateFault = 0

for fctr in range(F):
       print("Job Sequence on Factory: [ ",fctr," ]", ectSequence[fctr]) #, ectC[ectSequence[fctr][-1], -1])
       for idx, seq in enumerate(ectSequence[fctr]):
            dueDateFault = 0
            dueDateFault = ectC[fctr][idx, m-1] - d[seq]
            if dueDateFault > 0:
                 dueDateFaultSum += dueDateFault
            print("[ JOB: {", ectSequence[fctr][idx], "} TOTAL EXECUTON TIME: {", ectC[fctr][idx, m-1],"}", "dUEdATE:", d[seq],"TT",dueDateFault )
       print("****************************************")         
print("=======================================================")
print("TOTAL TT = ", dueDateFaultSum)
#####************************************* END SOLUTION 001 *************************************************

#********************************** SOLUTION 002 *****************************************
#               ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΚΑΛΥΤΕΡΗΣ ΑΚΟΛΟΥΘΙΑΣ ΣΥΜΦΩΝΑ ΜΕ ΤΟΝ NEHedd
# Υπολογίζεται μια ακολουθία με τον αλγόριθμο NEHedd σύμφωνα με το duedate σφάλμα
# Στην συνέχεια εκτελείται ο αλγόριθμος ect ο οποίος μοιράζει τις εργασίες στα εργοστάσια
# σύμφωνα με τον κανόνα earlier completion time.
# Τέλος υπολογίζεται το σφάλμα σχετικά με το duedate. (Δείχνει καλύτερα αποτελέσματα από το solution 001)
#************************************************************************************************
# print("------------------------- solution 002 NEHEDD + ECT ------------------------------------------------")
# startSeq = nhd.nehedd(d,n,m,p,F) 
# print(startSeq)
# #ΔΙΑΜΙΡΑΣΜΟΣ ΣΤΑ ΕΡΓΟΣΤΑΣΙΑ ΣΥΜΦΩΝΑ ΜΕ ΤΗΝ ΑΚΟΛΟΥΘΙΑ ΠΟΥ ΥΠΟΛΟΓΙΣΤΗΚΕ ΠΑΡΑΠΑΝΩ
# ectSequence, ectC = ect.ect_solution(d,n,m,p,F,startSeq)
# dueDateFaultSum = 0
# dueDateFault = 0
# for fctr in range(F):
#         print("Job Sequence on Factory: [ ",fctr," ]", ectSequence[fctr]) #, ectC[ectSequence[fctr][-1], -1])
#         for idx, seq in enumerate(ectSequence[fctr]):
#             dueDateFault = 0
#             dueDateFault = ectC[fctr][idx, m-1] - d[seq]
#             if dueDateFault > 0:
#                 dueDateFaultSum += dueDateFault
#             print("[ JOB: {", ectSequence[fctr][idx], "} TOTAL EXECUTON TIME: {", ectC[fctr][idx, m-1],"}", "dUEdATE:", d[seq],"TT",dueDateFault )
#         print("****************************************")         
# print("=======================================================")
# print("TOTAL TT = ", dueDateFaultSum)



#************************************ SOLUTION 003 ******************************************************************
#    ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΚΑΛΥΤΕΡΗΣ ΑΚΟΛΟΥΘΙΑΣ ΣΥΜΦΩΝΑ ΜΕ ΤΟΝ NEHEDD και διαμοιρασμός στα εργοστάσια σύμφωνα
#   με το μικρότερο duedate error
# Ταξινομούνται οι εργασίες σύμφωνα με το duedate. 
# 1. Υπολογίζουμε την ακολουθία με το καλύτερο duedate error (Όπως ο NEH και αντί του καλύτερου makespan λαμβάνουμε υπόψιν 
# το μικρότερο σφάλμα duedate)
# 2. Επιστρέφουμε την ακολοθία και μοιράζουμε την ακολουθία στα εργοστάσια σύμφωνα με το μικρότερο duedate error.
#********************************************************************************************************************
# print("------------------------- solution 003 NEHEDD + dd ------------------------------------------------")
startSeq = nhd.nehedd(d,n,m,p,F) 
print(startSeq)

ddSequence, ddC = dd.dd_solution(d,n,m,p,F,startSeq)

dueDateFaultSum = 0
dueDateFault = 0
for fctr in range(F):
        print("Job Sequence on Factory: [ ",fctr," ]", ddSequence[fctr]) #, ectC[ectSequence[fctr][-1], -1])
      
        for idx, seq in enumerate(ddSequence[fctr]):
            dueDateFault = 0
            dueDateFault = ddC[fctr][idx, m-1] - d[seq]
            if dueDateFault > 0:
                dueDateFaultSum += dueDateFault
            print("[ JOB: {", ddSequence[fctr][idx], "} TOTAL EXECUTON TIME: {", ddC[fctr][idx, m-1],"}", "dUEdATE:", d[seq],"TT",dueDateFault )
        print("****************************************")         
print("=======================================================")
print("TOTAL TT = ", dueDateFaultSum)


#************************************ SOLUTION 004 ******************************************************************
#               ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΚΑΛΥΤΕΡΗΣ ΑΚΟΛΟΥΘΙΑΣ ΣΥΜΦΩΝΑ ΜΕ ΤΟΝ NEHEDD με ταυτόχρονο διαμοιρασμό σε εργοστάσια
# Ταξινομούνται οι εργασίες σύμφωνα με το duedate. 
# 1. Παίρνουμε την πρώτη εργασία και την τοποθετούμε στο πρώτο εργοστάσιο
# 2. Παίρνουμε την δεύτερη εργασία και την τοποθετούμε στο δεύτερο εργοστάσιο
# 3. Παίρνουμε την τρίτη εργασία και την τοποθετούμε στο εργοστάσιο που έχουμε καλύτερο duedate error
#********************************************************************************************************************
#startSeq = nhd2.nehedd_2(d,n,m,p,F) 
#print(startSeq)


#************************************ SOLUTION neh update ******************************************************************
#               ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΚΑΛΥΤΕΡΗΣ ΑΚΟΛΟΥΘΙΑΣ ΣΥΜΦΩΝΑ ΜΕ ΤΟΝ NEHEDD όπως περιγράφεται στην εργασία
# 1. Δημιουργείται η ακολουθία startSeq σύμφωνα με την ταξινόμηση με το duedate. 
# 2. Αρχικοποιούμε για κάθε εργοστάσιο με αρχικές ακολουθίες (στην αρχή μηδενικές)
# 3. Για κάθε εργασία j της ακολουθίας -> 
# 4. Για κάθε εργοστάσιο δοκιμάζουμε την εργασία j σε όλες τις πιθανές θέσεις υπολογίζοντας κάθε φορά την καθυστέρηση
# 5. Βρίσκουμε το εργοστάστιο με την μικρότερη καθυστέρηση
# 6. Τοποθετούμε την εργασία στο εργοστάσιο με την μικρότερη καθυστέρηση στην κατάλληλη θέση
#********************************************************************************************************************
#startSeq = nhd2.nehedd_2(d,n,m,p,F) 






#ΕΞΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ


