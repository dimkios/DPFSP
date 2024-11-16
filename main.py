import loadfile as lf

import nehedd_new as nhd_n
import calcShedule as cS
import ils
import rsls
import rsls_II as rs2
import copy
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
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_1.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_2.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_3.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_4.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_5.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_1.txt')


#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_5_2.txt') #62
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_5_4.txt') #104
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_5_3.txt') #52
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_5_5.txt') #22

#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_6_2_1.txt') #164
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_6_2_2.txt') #151
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_6_2_3.txt') #224
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_6_2_4.txt') #97
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_6_2_5.txt') #414
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_6_3_1.txt') #146












#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Large/Ta001_2.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Large/Ta083_4.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Large/Ta012_6.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_1.txt')
n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_8_5_1.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_6_2_1.txt')


#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_3_4_4_4.txt')

#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_5_1.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_5_4.txt')

#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/test.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_16_3_3.txt')


startSequence = {}
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

print("Factories:[", F, "] - Jobs: [", n, "] - machines: [", m ,"]")
print()

#************************************ SOLUTION neh update ******************************************************************
#               ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΚΑΛΥΤΕΡΗΣ ΑΚΟΛΟΥΘΙΑΣ ΣΥΜΦΩΝΑ ΜΕ ΤΟΝ NEHEDD όπως περιγράφεται στην εργασία
# 1. Δημιουργείται η ακολουθία startSeq σύμφωνα με την ταξινόμηση με το duedate. 
# 2. Αρχικοποιούμε για κάθε εργοστάσιο με αρχικές ακολουθίες (στην αρχή μηδενικές)
# 3. Για κάθε εργασία j της ακολουθίας -> 
# 4. Για κάθε εργοστάσιο δοκιμάζουμε την εργασία j σε όλες τις πιθανές θέσεις υπολογίζοντας κάθε φορά την καθυστέρηση
# 5. Βρίσκουμε το εργοστάστιο με την μικρότερη καθυστέρηση
# 6. Τοποθετούμε την εργασία στο εργοστάσιο με την μικρότερη καθυστέρηση στην κατάλληλη θέση
#********************************************************************************************************************
print("<---------  ΑΛΓΟΡΙΘΜΟΣ   N E H e d d --------->")
startNEHedd = nhd_n.nehedd(d,n,m,p,F) 

bestTT = cS.calcTT(d,n,m,p,startNEHedd)
print("FINAL BEST for N E H e d d : [", bestTT , "]", startNEHedd)
print()
# print("------------------------------------------------")


#************************************ SOLUTION ΙLS ******************************************************************
#               Αλγόριθμος τυχαίων υπο ακολουθιών με τοπική αναζήτηση
# 1. Η πιο απλή μορφή τοπικής αναζήτησης. Επιλέγει δύο τυχαίες εργασίες από δυο τυχαία εργοστάσια και κάνει swap
# Ο αλγόριθμος βρίσκει την καλύτερη λύση σε μικρά προβλήματα. Στα μεγαλύτερα προβλήματα δεν καταλήγει στην βέλτιστη λύση
#********************************************************************************************************************
print("<---------  ΑΛΓΟΡΙΘΜΟΣ   I L S --------->")
startSequence = copy.deepcopy(startNEHedd) 
#print("startSequence", startSequence)
bestTT = float("inf")
bestTTnewI = float("inf")

bestTT = cS.calcTT(d,n,m,p,startSequence)
if bestTT < bestTTnewI:
        bestTTnewI = bestTT
        bestSequence = copy.deepcopy(startSequence) 
        #print("BEST SEQ", bestSequence)

#bestSequence = copy.deepcopy(startSequence)
for i in range(100000):

    bestTT = ils.ils(d,n,m,p, startSequence, bestTT)
    if bestTT < bestTTnewI:
        bestTTnewI = bestTT
        bestSequence = copy.deepcopy(startSequence) 
        #print("BEST SEQ", bestSequence)

print("FINAL BEST for I L S : [", bestTT , "]" , "SEQUENCE:", bestSequence)    
print()

#************************************ SOLUTION RSLS ******************************************************************
#              Αλγόριθμος τοπικής αναζήτησης με τυχαίες υποακολουθίες
# 1. Επιλέγεται τυχαίο εργοστάσιο ή 2 τυχαία εργοστάσια
# 2.1 Επιλέγεται υποακολουθία η οποία μετατίθεται σε άλλο σημείο του ίδιου εργοστασίου ή αντιστρέφεται η υποακολουθία
# 2.2 Επιλέγονται υποακολουθίες ίδιου μεγέθους και εναλλάσοντια μεταξύ δυο εργοστασίων ή αντιστρέφονται και εναλλάσονται
#********************************************************************************************************************
print("<---------  ΑΛΓΟΡΙΘΜΟΣ   R S L S --------->")
startSequenceRSLS = copy.deepcopy(startNEHedd) 
#print("startSequence", startSequenceRSLS)
bestTTRSLS = float("inf")
bestTTnewIRSLS = float("inf")
bestTTRSLS = cS.calcTT(d,n,m,p,startSequenceRSLS)
if bestTTRSLS < bestTTnewIRSLS:
        bestTTnewIRSLS = bestTTRSLS
        bestSequenceRSLS = copy.deepcopy(startSequenceRSLS) 
        #print("BEST SEQ", bestSequenceRSLS, bestTTRSLS)

for i in range(100000):
    bestTTRSLS, startSequenceRSLS = rsls.rsls(d,n,m,p,startSequenceRSLS, bestTTRSLS)
    if bestTTRSLS < bestTTnewIRSLS:
        bestTTnewIRSLS = bestTTRSLS
        bestSequenceRSLS = copy.deepcopy(startSequenceRSLS) 
        #print("BEST SEQ", bestSequenceRSLS, bestTTRSLS)
print("FINAL BEST for R S L S : [", bestTTRSLS , "]", bestSequenceRSLS)    
print()    
#************************************ SOLUTION RSLS II******************************************************************
#           Αλγόριθμος τοπικής αναζήτησης με τυχαία σημεία
# 1. Επιλέγεται τυχαίο εργοστάσιο ή 2 τυχαία εργοστάσια
# 2.1 Επιλέγεται σημείο το οποίο μετατίθεται σε άλλη θέση του ίδιου εργοστασίου ή εναλλάσεται με άλλο τυχαίο σημείο
# 2.2.1 Επιλέγεται σημείο το οποίο αφαιρείται από ένα εργοστάσιο και προστίθεται στο δεύτερο εργοστάσιο
# 2.2.2 Επιλέγεται σημείο το οποίο εναλλάσεται με σημείο στο δεύτερο εργοστάσιο 
#********************************************************************************************************************
print("<---------  ΑΛΓΟΡΙΘΜΟΣ   R S L S  II --------->")
startSequenceRSLSII = copy.deepcopy(startNEHedd)

#print("startSequence", startSequenceRSLSII)
bestTT = float("inf")

bestTTRSLSII = float("inf")
bestTTnewIRSLSII = float("inf")
bestTTRSLSII = cS.calcTT(d,n,m,p,startSequenceRSLSII)
if bestTTRSLSII < bestTTnewIRSLSII:
        bestTTnewIRSLSII = bestTTRSLSII
        bestSequenceRSLSII = copy.deepcopy(startSequenceRSLSII) 
        #print("BEST SEQ", bestSequenceRSLSII, bestTTRSLSII)

for i in range(10000):
    checkSeqRS_II = copy.deepcopy(startNEHedd) 
    bestTTRSLSII, startSequenceRSLSII = rs2.rsls_II(d,n,m,p,checkSeqRS_II, bestTTRSLSII)
    if bestTTRSLSII < bestTTnewIRSLSII:
        bestTTnewIRSLSII = bestTTRSLSII
        bestSequenceRSLSII = copy.deepcopy(startSequenceRSLSII) 
        #print("BEST SEQ", bestSequenceRSLSII, bestTTRSLSII)
print("FINAL BEST for R S L S    I I: [", bestTTRSLSII , "]", bestSequenceRSLSII)    
print()    
#************************************ SOLUTION HYBRID GA WITH LS******************************************************************
#               
#
#********************************************************************************************************************
print("<---------  ΑΛΓΟΡΙΘΜΟΣ   GALS --------->")

#-

# print(": TEEEEEEEEEEEEEEEEEEST :")
# factCheck = {}
# factCheck[0] = [12,15,10,0,6,3,7,5]
# factCheck[1] = [14,1,11,13,4,2,9,8]

# checkTT = cS.calcTT(d,n,m,p,factCheck)

# print("SEQUENCE", factCheck, "CHECK TTTT", checkTT)