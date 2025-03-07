import loadfile as lf
import nehedd_new as nhd_n
import calcShedule as cS
import ils
import rsls
import rsls_II as rs2
import ls_insertion_job as ls_ij
import ls_move_job as ls_mv
import ls_exchange_job as ls_xc
import ig
import ga_ls as ga

#
import copy
import os
import csv
import time

#rich console
from rich.console import Console
from rich.table import Table
from rich import print
from rich import box

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
fileCnt = len(arxeia)

#rich table title
table = Table(title="DPFSP ALGORITHM ARENA", style="bold")
table.add_column("FILE", justify="center", style="cyan", no_wrap=True)
table.add_column("FACTORIES", justify="center", style="gold1", no_wrap=True)
table.add_column("JOBS", justify="center", style="gold1")
table.add_column("MACHINES", justify="center", style="gold1")
table.add_column("NEHEDD", justify="right", style="blue")
table.add_column("ILS", justify="right", style="blue")
table.add_column("RSLS", justify="right", style="blue")
table.add_column("RSLS II", justify="right", style="blue")
table.add_column("LS insert", justify="right", style="blue")
table.add_column("LS move", justify="right", style="blue")
table.add_column("LS exchange", justify="right", style="blue")
table.add_column("HYLG", justify="right", style="medium_spring_green")
table.add_column("GA_LS", justify="right", style="medium_spring_green")
table.add_column("Best Result", justify="right", style="red", no_wrap=False)
table.add_column("RPD", justify="right", style="bright_green", no_wrap=False)

#ΦΟΡΤΩΣΗ DATASET
with Progress() as progress:
    print()
    #Έναρξη εκτέλεσης progressbar
    task = progress.add_task("[cyan]ΕΚΤΕΛΕΣΗ ΑΛΓΟΡΙΘΜΩΝ για DPSFSP...", total=fileCnt)
    
    #Εκτελουμε τους αλγόριθμους για κάθε αρχείο
    start_time = time.time()  
    for i in range(fileCnt):

        file = arxeia[i+1]
        filename = os.path.basename(arxeia[i+1])

        print("fileName =", filename)

        if filename.startswith("I_"):
            csv_file = "Best_Result_small.csv"
        elif filename.startswith("Ta"):
            csv_file = "Best_Result_large.csv"
        else:
            print(f"[red]Το αρχείο {filename} δεν είναι έγκυρο για αυτή τη διαδικασία![/red]")
            continue

        with open(csv_file, mode='r', newline='', encoding='utf-8') as csv_file_obj:
            reader = csv.DictReader(csv_file_obj)
            for row in reader:
                if row['Instance'] == filename:
                    best_value = row['Best']
                    break
                         
        n,m,F,p,d = lf.read_dpfsp_dataset(arxeia[i+1])
        startSequence = {}

        runTimer = n*m*0.25


#************************************ SOLUTION neh update ******************************************************************
#               ΥΠΟΛΟΓΙΣΜΟΣ ΤΗΣ ΚΑΛΥΤΕΡΗΣ ΑΚΟΛΟΥΘΙΑΣ ΣΥΜΦΩΝΑ ΜΕ ΤΟΝ NEHEDD όπως περιγράφεται στην εργασία
# 1. Δημιουργείται η ακολουθία startSeq σύμφωνα με την ταξινόμηση με το duedate. 
# 2. Αρχικοποιούμε για κάθε εργοστάσιο με αρχικές ακολουθίες (στην αρχή μηδενικές)
# 3. Για κάθε εργασία j της ακολουθίας -> 
# 4. Για κάθε εργοστάσιο δοκιμάζουμε την εργασία j σε όλες τις πιθανές θέσεις υπολογίζοντας κάθε φορά την καθυστέρηση
# 5. Βρίσκουμε το εργοστάστιο με την μικρότερη καθυστέρηση
# 6. Τοποθετούμε την εργασία στο εργοστάσιο με την μικρότερη καθυστέρηση στην κατάλληλη θέση
#********************************************************************************************************************
        startNEHedd = nhd_n.nehedd(d,n,m,p,F) 
        bestTT = cS.calcTT(d,n,m,p,startNEHedd)
        bestNEHedd = bestTT

#************************************ SOLUTION ΙLS ******************************************************************
#               Αλγόριθμος τυχαίων υπο ακολουθιών με τοπική αναζήτηση
# 1. Η πιο απλή μορφή τοπικής αναζήτησης. Επιλέγει δύο τυχαίες εργασίες από δυο τυχαία εργοστάσια και κάνει swap
# Ο αλγόριθμος βρίσκει την καλύτερη λύση σε μικρά προβλήματα. Στα μεγαλύτερα προβλήματα δεν καταλήγει στην βέλτιστη λύση
#********************************************************************************************************************
        startSequence = copy.deepcopy(startNEHedd) 
        bestTT = float("inf")
        bestTTnewI = float("inf")
        bestTT = cS.calcTT(d,n,m,p,startSequence)
        if bestTT < bestTTnewI:
                bestTTnewI = bestTT
                bestSequence = copy.deepcopy(startSequence) 

        startTimerILS = time.time()
        timerILS = 0
        i=0
        #for i in range(10000):
        while timerILS < runTimer:    
            i = i+1
            #print("ILS :", i)
            bestTT, bestSeq2 = ils.ils(d,n,m,p, startSequence, bestTT)
            if bestTT < bestTTnewI:
                bestTTnewI = bestTT
                bestSequence = copy.deepcopy(startSequence) 
            endTimerILS = time.time()
            timerILS = endTimerILS - startTimerILS    
        bestILS = bestTT
        print("ILS :", i, "timer:", timerILS)

#************************************ SOLUTION RSLS ******************************************************************
#              Αλγόριθμος τοπικής αναζήτησης με τυχαίες υποακολουθίες
# 1. Επιλέγεται τυχαίο εργοστάσιο ή 2 τυχαία εργοστάσια
# 2.1 Επιλέγεται υποακολουθία η οποία μετατίθεται σε άλλο σημείο του ίδιου εργοστασίου ή αντιστρέφεται η υποακολουθία
# 2.2 Επιλέγονται υποακολουθίες ίδιου μεγέθους και εναλλάσοντια μεταξύ δυο εργοστασίων ή αντιστρέφονται και εναλλάσονται
#********************************************************************************************************************
        startSequenceRSLS = copy.deepcopy(startNEHedd) 
        bestTTRSLS = float("inf")
        bestTTnewIRSLS = float("inf")
        
        startTimerRSLS = time.time()
        timerRSLS = 0
        i=0
        #for i in range(10000):
        while timerRSLS < runTimer:     
            i = i+1
            bestTTRSLS, startSequenceRSLS = rsls.rsls(d,n,m,p,startSequenceRSLS, bestTTRSLS)
            if bestTTRSLS < bestTTnewIRSLS:
                bestTTnewIRSLS = bestTTRSLS
                bestSequenceRSLS = copy.deepcopy(startSequenceRSLS) 
            endTimerRSLS = time.time()
            timerRSLS = endTimerRSLS - startTimerRSLS       
        bestRSLS = bestTTRSLS
        print("RSLS :", i, "timer:", timerRSLS)
#************************************ SOLUTION RSLS II******************************************************************
#           Αλγόριθμος τοπικής αναζήτησης με τυχαία σημεία
# 1. Επιλέγεται τυχαίο εργοστάσιο ή 2 τυχαία εργοστάσια
# 2.1 Επιλέγεται σημείο το οποίο μετατίθεται σε άλλη θέση του ίδιου εργοστασίου ή εναλλάσεται με άλλο τυχαίο σημείο
# 2.2.1 Επιλέγεται σημείο το οποίο αφαιρείται από ένα εργοστάσιο και προστίθεται στο δεύτερο εργοστάσιο
# 2.2.2 Επιλέγεται σημείο το οποίο εναλλάσεται με σημείο στο δεύτερο εργοστάσιο 
#********************************************************************************************************************
        
        startSequenceRSLSII = copy.deepcopy(startNEHedd)
        bestTT = float("inf")
        bestTTRSLSII = float("inf")
        bestTTnewIRSLSII = float("inf")
        bestTTRSLSII = cS.calcTT(d,n,m,p,startSequenceRSLSII)
        if bestTTRSLSII < bestTTnewIRSLSII:
                bestTTnewIRSLSII = bestTTRSLSII
                bestSequenceRSLSII = copy.deepcopy(startSequenceRSLSII) 

        startTimerRSLS2 = time.time()
        timerRSLS2 = 0
        i=0


        #for i in range(10000):
        while timerRSLS2 < runTimer:
            i = i+1 
            checkSeqRS_II = copy.deepcopy(startNEHedd) 
            bestTTRSLSII, startSequenceRSLSII = rs2.rsls_II(d,n,m,p,checkSeqRS_II, bestTTRSLSII)
            if bestTTRSLSII < bestTTnewIRSLSII:
                bestTTnewIRSLSII = bestTTRSLSII
                bestSequenceRSLSII = copy.deepcopy(startSequenceRSLSII) 
            endTimerRSLS2 = time.time()
            timerRSLS2 = endTimerRSLS2 - startTimerRSLS2    
        bestRSLS_II = bestTTRSLSII
        print("RSLS2 :", i, "timer:", timerRSLS2)
#************************************ SOLUTION HYBRID GA WITH LS******************************************************************
#                                       ΓΕΝΕΤΙΚΟΣ ΑΛΓΟΡΙΘΜΟΣ
#
#********************************************************************************************************************

#************************************ SUB SOLUTION LOCAL SEARCH I ******************************************************************
#                                       ls_insertion_job.py
# Τοπική αναζήτηση. Επιλέγουμε τυχαία ένα εργοστάσιο και στην συνέχεια επιλέγουμε τυχαία 2 εργασίες
# Εξετάζουμε όλες τις πιθανές θέσεις και επανατοποθετούμε τις εργασίες στις θέσεις που μειώνουν περισσότερο την καθυστέρηση
#*********************************************************************************************************************************
        startSequenceLS_INSERTION_JOB = copy.deepcopy(startNEHedd)
        sequence_InsertionJob = {}
        sequence_BestTime = {}
        bestTT = float("inf")


        startTimerLSIN = time.time()
        timerLSIN = 0
        i=0
        #for i in range(10):
        while timerLSIN < runTimer:
            i = i+1     
            sequence_InsertionJob, bestTTnew=copy.deepcopy(ls_ij.ls_insertion_job(d,n,m,p,startSequenceLS_INSERTION_JOB))  
            if bestTTnew < bestTT:
                bestTT = bestTTnew
                sequence_BestTime = copy.deepcopy(sequence_InsertionJob)
            endTimerLSIN = time.time()
            timerLSIN = endTimerLSIN - startTimerLSIN 
        bestLSinsert = bestTT
        print("LSIN :", i, "timer:", timerLSIN)
#************************************ SUB SOLUTION LOCAL SEARCH II ******************************************************************
#                                       ls_move_job.py
# Τοπική αναζήτηση. Επιλέγουμε το εργοστάσιο με την μεγαλύτερη καθυστέρηση και το εργοστάσιο με την μικρότερη καθυστέρηση.
# Αφαιρούμε εργασία από το εργοστάσιο με την μεγαλύτερη καθυστέρηση και εξεταζουμε τις θέσεις στο εργοστάσιο με την μικρότερη καθυστέρηση
#************************************************************************************************************************************
        startSequenceLS_MOVE_JOB = copy.deepcopy(startNEHedd)
        sequence_moveJob = {}
        sequence_BestTime_move = {}
        bestTTmove = float("inf")


        startTimerLSMV = time.time()
        timerLSMV = 0
        i=0

        #for i in range(10):
        while timerLSMV < runTimer:
            i = i+1     
            bestTTnewLSmove, startSequenceLSmove = ls_mv.ls_move_job(d,n,m,p,F,startSequenceLS_MOVE_JOB)
            if bestTTnewLSmove < bestTTmove:
                bestTTmove = bestTTnewLSmove
                bestSequenceLSmove = copy.deepcopy(startSequenceLSmove) 
            endTimerLSMV = time.time()
            timerLSMV = endTimerLSMV - startTimerLSMV 
        bestLSmove = bestTTmove
        print("LSMV :", i, "timer:", timerLSMV)
#************************************ SUB SOLUTION LOCAL SEARCH III ******************************************************************
#                                       ls_exchange_job.py
# Επιλέγουμε το εργοστάσιο με την μεγαλύτερη καθυστέρηση (maxFact) και το εργοστάσιο με την μικρότερη 
# καθυστέρηση (minFact) Εξετάζουμε κάθε εργασία του maxFact σε όλες τις θέσεις του minFact
# Εάν η καθυστέρηση στο minFact είναι μικρότερη από την καθυστέρηση στο maxFact ddMax αλλάζουμε θέση στην 
# εργασία.
#************************************************************************************************************************************
        startSequenceLS_EXCHANGE_JOB = copy.deepcopy(startNEHedd)
        sequence_exchangeJob = {}
        sequence_BestTime_exchange = {}
        bestTTexchange = float("inf")

        sequence_exchangeJob, bestTTexchangeNew=copy.deepcopy(ls_xc.ls_exchange_job(d,n,m,p,F,startSequenceLS_EXCHANGE_JOB)) 

        startTimerLSXC = time.time()
        timerLSXC = 0
        i=0



        #for i in range(10):
        while timerLSXC < runTimer:
            i = i+1     
            bestTTnewLSexchange, startSequenceLSexchange = ls_xc.ls_exchange_job(d,n,m,p,F,startSequenceLS_EXCHANGE_JOB)
            if bestTTnewLSexchange < bestTTexchange:
                bestTTexchange = bestTTnewLSexchange
                bestSequenceLSexchange = copy.deepcopy(startSequenceLSexchange) 
            endTimerLSXC = time.time()
            timerLSXC = endTimerLSXC - startTimerLSXC     
        bestLSexchange = bestTTexchange
        print("LSXC :", i, "timer:", timerLSXC)
#************************************ IG solution******************************************************************
#                                       ig.py
# Εφαρμογή του αλγόριθμου Iterated Greedy Algorithm των RUIZ και STUETZLE προσαρμοσμένος σε Due dates
#******************************************************************************************************************
        startSeq_IG = copy.deepcopy(startNEHedd)
        sequence_IG = {}
        bestTTIG = float("inf")
        bestTTnewIG = float("inf")

        
        startSeq_IG, bestTTIG = ig.ig(d,n,m,p,F,startSeq_IG)

#************************************ GA LS solution******************************************************************
#                                       ig.py
# Εφαρμογή του αλγόριθμου Iterated Greedy Algorithm των RUIZ και STUETZLE προσαρμοσμένος σε Due dates
#******************************************************************************************************************
        startSeq_IG = copy.deepcopy(startNEHedd)
        sequence_IG = {}
        bestTTnewIG = float("inf")
        bestTTGA = None
        
        startSeq_GA, bestTTGA = ga.ga(d,n,m,p,F,startSeq_IG)
       
#-------------------------------------------------------------------------------------------------------------------------------------------
        RPD = 0
        if float(best_value) != 0:
            RPD = 0
            RPD_NEHEDD = 0
            RPD_ILS = 0
            RPD_RSLS = 0
            RPD_RSLS_II = 0
            RPD_LS_IN = 0
            RPD_LS_MV = 0
            RPD_LS_EX = 0
            RPD_HYLG = 0
            RPD_GA_LS = 0

            #sumAll = bestNEHedd + bestILS + bestRSLS + bestRSLS_II + bestLSinsert + bestLSmove + bestLSexchange
            min_value = min(bestNEHedd, bestILS, bestRSLS, bestRSLS_II, bestLSinsert, bestLSmove, bestLSexchange, bestTTIG, bestTTGA)
                #, bestTTGA            #avgSum = sumAll / 7
            RPD = (float(min_value) - float(best_value)) / float(best_value) * 100 
            RPD = round(RPD,2)

        table.add_row(filename,str(F), str(n), str(m), str(bestNEHedd), str(bestILS), str(bestRSLS), str(bestRSLS_II), str(bestLSinsert), str(bestLSmove), str(bestLSexchange), str(bestTTIG), str(bestTTGA), str(best_value), str(RPD))
        progress.update(task, advance=1)
    end_time = time.time()
    execution_time = end_time - start_time
#-------------------------------------------------------------------------------------------------------------------------------------------


console = Console()

print()
console.print(table)
console.print(f"ΣΥΝΟΛΙΚΟΣ ΧΡΟΝΟΣ ΕΚΤΕΛΕΣΗΣ {execution_time:.2f} δευτερόλεπτα.")