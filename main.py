import loadfile as lf

import nehedd_new as nhd_n
import calcShedule as cS
import ils
import rsls
import rsls_II as rs2
import copy
import time
import ls_insertion_job as ls_ij
import ls_move_job as ls_mv
import ls_exchange_job as ls_xc

from rich.console import Console
from rich.table import Table

from rich.progress import Progress

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

arxeia = lf.load_files()
#print(arxeia)
#n,m,F,p,d = lf.read_dpfsp_dataset(arxeio)
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Large/Ta012_6.txt')

fileCnt = len(arxeia)
#print(fileCnt)

print("start ALGORITHM ARENA")

table = Table(title="DPFSP ALGORITHM ARENA")
table.add_column("FILE", justify="center", style="cyan", no_wrap=True)
table.add_column("FACTORIES", justify="center", style="cyan", no_wrap=True)
table.add_column("JOBS")
table.add_column("MACHINES")
table.add_column("NEHEDD", justify="right", style="blue")
table.add_column("ILS", justify="right", style="blue")
table.add_column("RSLS", justify="right", style="blue")
table.add_column("RSLS II", justify="right", style="blue")
table.add_column("LS insert", justify="right", style="blue")
table.add_column("LS move", justify="right", style="blue")
table.add_column("LS exchange", justify="right", style="blue")

#ΦΟΡΤΩΣΗ DATASET
with Progress() as progress:
    task = progress.add_task("[cyan]ΕΚΤΕΛΕΣΗ ΑΛΓΟΡΙΘΜΩΝ για DPSFSP...", total=fileCnt)
        # Do something here
      
    for i in range(fileCnt):
        #print(arxeia[i+1])
        file = arxeia[i+1]
        n,m,F,p,d = lf.read_dpfsp_dataset(arxeia[i+1])
        #n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
        #n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
        #n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_5_1.txt')
        # n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_5_4.txt')
        #n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/test.txt')
        #n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_16_3_3.txt')
        #n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_3_4_4_4.txt')

        startSequence = {}

    #************************************ LOAD DATASET ******************************************************************
    #               Φόρτωση δεδομένων από αρχεία. Αρχικώς χρησιμοποιούμε ένα ένα τα αρχεία
    #           Στην συνέχεια θα δοθούν επιλογές για το ποιά αρχεία θα φορτώσουμε καθώς επίσης και δυνατότητα
    #           φόρτωσης ενός συνόλου αρχείων.
    #********************************************************************************************************************

        #print("============ dataset loaded ===============")
        #for j in range(n):
            #print("job=[",j,"]",  end="", flush=True)
            #for i in range(m):
                #print("machine=[", i,"] -> ", p[j,i], "-", end="", flush=True)
            #print("duedate = ",j, d[j], "", end="", flush=True) 
            #print() 
        #print("============================================")   

        #print("Factories:[", F, "] - Jobs: [", n, "] - machines: [", m ,"]")
        #print()

    #************************************ SOLUTION neh update ******************************************************************
    #               ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΚΑΛΥΤΕΡΗΣ ΑΚΟΛΟΥΘΙΑΣ ΣΥΜΦΩΝΑ ΜΕ ΤΟΝ NEHEDD όπως περιγράφεται στην εργασία
    # 1. Δημιουργείται η ακολουθία startSeq σύμφωνα με την ταξινόμηση με το duedate. 
    # 2. Αρχικοποιούμε για κάθε εργοστάσιο με αρχικές ακολουθίες (στην αρχή μηδενικές)
    # 3. Για κάθε εργασία j της ακολουθίας -> 
    # 4. Για κάθε εργοστάσιο δοκιμάζουμε την εργασία j σε όλες τις πιθανές θέσεις υπολογίζοντας κάθε φορά την καθυστέρηση
    # 5. Βρίσκουμε το εργοστάστιο με την μικρότερη καθυστέρηση
    # 6. Τοποθετούμε την εργασία στο εργοστάσιο με την μικρότερη καθυστέρηση στην κατάλληλη θέση
    #********************************************************************************************************************
        #print("<---------  ΑΛΓΟΡΙΘΜΟΣ   N E H e d d --------->")
        startNEHedd = nhd_n.nehedd(d,n,m,p,F) 

        bestTT = cS.calcTT(d,n,m,p,startNEHedd)

        bestNEHedd = bestTT
        #print("FINAL BEST for N E H e d d : [", bestTT , "]", startNEHedd)
        #print()
        # print("------------------------------------------------")
    #************************************ SOLUTION ΙLS ******************************************************************
    #               Αλγόριθμος τυχαίων υπο ακολουθιών με τοπική αναζήτηση
    # 1. Η πιο απλή μορφή τοπικής αναζήτησης. Επιλέγει δύο τυχαίες εργασίες από δυο τυχαία εργοστάσια και κάνει swap
    # Ο αλγόριθμος βρίσκει την καλύτερη λύση σε μικρά προβλήματα. Στα μεγαλύτερα προβλήματα δεν καταλήγει στην βέλτιστη λύση
    #********************************************************************************************************************
        #print("<---------  ΑΛΓΟΡΙΘΜΟΣ   I L S --------->")
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
        bestILS = bestTT
        #print("FINAL BEST for I L S : [", bestTT , "]" , "SEQUENCE:", bestSequence)    
        #print()

    #************************************ SOLUTION RSLS ******************************************************************
    #              Αλγόριθμος τοπικής αναζήτησης με τυχαίες υποακολουθίες
    # 1. Επιλέγεται τυχαίο εργοστάσιο ή 2 τυχαία εργοστάσια
    # 2.1 Επιλέγεται υποακολουθία η οποία μετατίθεται σε άλλο σημείο του ίδιου εργοστασίου ή αντιστρέφεται η υποακολουθία
    # 2.2 Επιλέγονται υποακολουθίες ίδιου μεγέθους και εναλλάσοντια μεταξύ δυο εργοστασίων ή αντιστρέφονται και εναλλάσονται
    #********************************************************************************************************************
        #print("<---------  ΑΛΓΟΡΙΘΜΟΣ   R S L S --------->")
        startSequenceRSLS = copy.deepcopy(startNEHedd) 
        #print("startSequence", startSequenceRSLS)
        bestTTRSLS = float("inf")
        bestTTnewIRSLS = float("inf")
        # bestTTRSLS = cS.calcTT(d,n,m,p,startSequenceRSLS)
        # if bestTTRSLS < bestTTnewIRSLS:
        #         bestTTnewIRSLS = bestTTRSLS
        #         bestSequenceRSLS = copy.deepcopy(startSequenceRSLS) 
                #print("BEST SEQ", bestSequenceRSLS, bestTTRSLS)

        for i in range(10000):
            bestTTRSLS, startSequenceRSLS = rsls.rsls(d,n,m,p,startSequenceRSLS, bestTTRSLS)
            if bestTTRSLS < bestTTnewIRSLS:
                bestTTnewIRSLS = bestTTRSLS
                bestSequenceRSLS = copy.deepcopy(startSequenceRSLS) 
                #print("BEST SEQ", bestSequenceRSLS, bestTTRSLS)
        #print("FINAL BEST for R S L S : [", bestTTRSLS , "]", bestSequenceRSLS)    
        #print()    
        bestRSLS = bestTTRSLS
    #************************************ SOLUTION RSLS II******************************************************************
    #           Αλγόριθμος τοπικής αναζήτησης με τυχαία σημεία
    # 1. Επιλέγεται τυχαίο εργοστάσιο ή 2 τυχαία εργοστάσια
    # 2.1 Επιλέγεται σημείο το οποίο μετατίθεται σε άλλη θέση του ίδιου εργοστασίου ή εναλλάσεται με άλλο τυχαίο σημείο
    # 2.2.1 Επιλέγεται σημείο το οποίο αφαιρείται από ένα εργοστάσιο και προστίθεται στο δεύτερο εργοστάσιο
    # 2.2.2 Επιλέγεται σημείο το οποίο εναλλάσεται με σημείο στο δεύτερο εργοστάσιο 
    #********************************************************************************************************************
        #print("<---------  ΑΛΓΟΡΙΘΜΟΣ   R S L S  II --------->")
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
        #print("FINAL BEST for R S L S    I I: [", bestTTRSLSII , "]", bestSequenceRSLSII)    
        #print()    
        bestRSLS_II = bestTTRSLSII

    #************************************ SOLUTION HYBRID GA WITH LS******************************************************************
    #                                       ΓΕΝΕΤΙΚΟΣ ΑΛΓΟΡΙΘΜΟΣ
    #
    #********************************************************************************************************************
        #print("<---------  ΑΛΓΟΡΙΘΜΟΣ   GALS --------->")



    #************************************ SUB SOLUTION LOCAL SEARCH I ******************************************************************
    #                                       ls_insertion_job.py
    # Τοπική αναζήτηση. Επιλέγουμε τυχαία ένα εργοστάσιο και στην συνέχεια επιλέγουμε τυχαία 2 εργασίες
    # Εξετάζουμε όλες τις πιθανές θέσεις και επανατοποθετούμε τις εργασίες στις θέσεις που μειώνουν περισσότερο την καθυστέρηση
    #*********************************************************************************************************************************
        #print("<---- LOCAL SEARCH INSERTION JOB --->")

        startSequenceLS_INSERTION_JOB = copy.deepcopy(startNEHedd)
        sequence_InsertionJob = {}
        sequence_BestTime = {}
        #print("neh", startSequenceLS_INSERTION_JOB)
        bestTT = float("inf")
        for i in range(100000):
            sequence_InsertionJob, bestTTnew=copy.deepcopy(ls_ij.ls_insertion_job(d,n,m,p,startSequenceLS_INSERTION_JOB))  
            #print("START", startSequenceLS_INSERTION_JOB, "END", sequence_InsertionJob )
            if bestTTnew < bestTT:
                bestTT = bestTTnew
                sequence_BestTime = copy.deepcopy(sequence_InsertionJob)
                #print("START", startSequenceLS_INSERTION_JOB, "END", sequence_InsertionJob, "time:", bestTTnew)
        #print("FINAL BEST for ls_insertion_job: [", bestTT , "]", sequence_BestTime)   
        bestLSinsert = bestTT
        #print()

    #************************************ SUB SOLUTION LOCAL SEARCH II ******************************************************************
    #                                       ls_move_job.py
    # Τοπική αναζήτηση. Επιλέγουμε το εργοστάσιο με την μεγαλύτερη καθυστέρηση και το εργοστάσιο με την μικρότερη καθυστέρηση.
    # Αφαιρούμε εργασία από το εργοστάσιο με την μεγαλύτερη καθυστέρηση και εξεταζουμε τις θέσεις στο εργοστάσιο με την μικρότερη καθυστέρηση
    #************************************************************************************************************************************

        #print("<---- LOCAL SEARCH MOVE JOB --->")

        startSequenceLS_MOVE_JOB = copy.deepcopy(startNEHedd)
        sequence_moveJob = {}
        sequence_BestTime_move = {}
        #print("neh", startSequenceLS_INSERTION_JOB)
        bestTTmove = float("inf")
        #sequence_moveJob, bestTTmoveNew=copy.deepcopy(ls_mv.ls_move_job(d,n,m,p,F,startSequenceLS_MOVE_JOB))  
        for i in range(1000):
            bestTTnewLSmove, startSequenceLSmove = ls_mv.ls_move_job(d,n,m,p,F,startSequenceLS_MOVE_JOB)
            if bestTTnewLSmove < bestTTmove:
                bestTTmove = bestTTnewLSmove
                bestSequenceLSmove = copy.deepcopy(startSequenceLSmove) 
                #print("BEST SEQ", bestSequenceRSLS, bestTTRSLS)
        #print("FINAL BEST for L S move Job : [", bestTTmove , "]", bestSequenceLSmove)    
        #print()    
        bestLSmove = bestTTmove

    #************************************ SUB SOLUTION LOCAL SEARCH III ******************************************************************
    #                                       ls_move_job.py
    # Επιλέγουμε το εργοστάσιο με την μεγαλύτερη καθυστέρηση (maxFact) και το εργοστάσιο με την μικρότερη 
    # καθυστέρηση (minFact) Εξετάζουμε κάθε εργασία του maxFact σε όλες τις θέσεις του minFact
    # Εάν η καθυστέρηση στο minFact είναι μικρότερη από την καθυστέρηση στο maxFact ddMax αλλάζουμε θέση στην 
    # εργασία.
    #************************************************************************************************************************************

        #print("<---- LOCAL SEARCH MOVE JOB --->")

        startSequenceLS_EXCHANGE_JOB = copy.deepcopy(startNEHedd)
        sequence_exchangeJob = {}
        sequence_BestTime_exchange = {}
        #print("neh", startSequenceLS_INSERTION_JOB)
        bestTTexchange = float("inf")


        sequence_exchangeJob, bestTTexchangeNew=copy.deepcopy(ls_xc.ls_exchange_job(d,n,m,p,F,startSequenceLS_EXCHANGE_JOB))  
        for i in range(1000):
            bestTTnewLSexchange, startSequenceLSexchange = ls_xc.ls_exchange_job(d,n,m,p,F,startSequenceLS_EXCHANGE_JOB)
            if bestTTnewLSexchange < bestTTexchange:
                bestTTexchange = bestTTnewLSexchange
                bestSequenceLSexchange = copy.deepcopy(startSequenceLSexchange) 
                #print("BEST SEQ", bestSequenceRSLS, bestTTRSLS)
        #print("FINAL BEST for L S exchange Job : [", bestTTexchange , "]", bestSequenceLSexchange)    
        #print()    
        bestLSexchange = bestTTexchange

        table.add_row(file,str(F), str(n), str(m), str(bestNEHedd), str(bestILS), str(bestRSLS), str(bestRSLS_II), str(bestLSinsert), str(bestLSmove), str(bestLSexchange))
        #table.add_row(str(F), str(n), )
        #print("F=", F, "jobs=", n, "Machines=", m, "NEHEDD:", bestNEHedd, "ILS:", bestILS, "RSLS:", bestRSLS, "RSLS_II", bestRSLS_II, "LSinsert", bestLSinsert, "LSmove", bestLSmove, "LSexchange", bestLSexchange)
        progress.update(task, advance=1)

        #-

        # print(": TEEEEEEEEEEEEEEEEEEST :")
        # factCheck = {}
        # factCheck[0] = [12,15,6,3,7,5,0]
        # factCheck[1] = [14, 1, 11, 13, 9, 10, 4, 2, 8]

        # checkTT = cS.calcTT(d,n,m,p,factCheck)
        # print("SEQUENCE", factCheck, "CHECK TTTT", checkTT)

console = Console()
console.print(table)