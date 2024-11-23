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
table.add_column("IG", justify="right", style="blue")
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
                    #console.print(f"[green]Η τιμή της στήλης 'Best' για το '{filename}' είναι: {best_value}[/green]")
                    break
                         
        n,m,F,p,d = lf.read_dpfsp_dataset(arxeia[i+1])
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
        for i in range(100000):
            bestTT, bestSeq2 = ils.ils(d,n,m,p, startSequence, bestTT)
            if bestTT < bestTTnewI:
                bestTTnewI = bestTT
                bestSequence = copy.deepcopy(startSequence) 
        bestILS = bestTT

#************************************ SOLUTION RSLS ******************************************************************
#              Αλγόριθμος τοπικής αναζήτησης με τυχαίες υποακολουθίες
# 1. Επιλέγεται τυχαίο εργοστάσιο ή 2 τυχαία εργοστάσια
# 2.1 Επιλέγεται υποακολουθία η οποία μετατίθεται σε άλλο σημείο του ίδιου εργοστασίου ή αντιστρέφεται η υποακολουθία
# 2.2 Επιλέγονται υποακολουθίες ίδιου μεγέθους και εναλλάσοντια μεταξύ δυο εργοστασίων ή αντιστρέφονται και εναλλάσονται
#********************************************************************************************************************
        startSequenceRSLS = copy.deepcopy(startNEHedd) 
        bestTTRSLS = float("inf")
        bestTTnewIRSLS = float("inf")
        
        for i in range(10000):
            bestTTRSLS, startSequenceRSLS = rsls.rsls(d,n,m,p,startSequenceRSLS, bestTTRSLS)
            if bestTTRSLS < bestTTnewIRSLS:
                bestTTnewIRSLS = bestTTRSLS
                bestSequenceRSLS = copy.deepcopy(startSequenceRSLS) 
        bestRSLS = bestTTRSLS
        
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

        for i in range(10000):
            checkSeqRS_II = copy.deepcopy(startNEHedd) 
            bestTTRSLSII, startSequenceRSLSII = rs2.rsls_II(d,n,m,p,checkSeqRS_II, bestTTRSLSII)
            if bestTTRSLSII < bestTTnewIRSLSII:
                bestTTnewIRSLSII = bestTTRSLSII
                bestSequenceRSLSII = copy.deepcopy(startSequenceRSLSII) 
        bestRSLS_II = bestTTRSLSII
        
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
        for i in range(100000):
            sequence_InsertionJob, bestTTnew=copy.deepcopy(ls_ij.ls_insertion_job(d,n,m,p,startSequenceLS_INSERTION_JOB))  
            if bestTTnew < bestTT:
                bestTT = bestTTnew
                sequence_BestTime = copy.deepcopy(sequence_InsertionJob)
        bestLSinsert = bestTT

#************************************ SUB SOLUTION LOCAL SEARCH II ******************************************************************
#                                       ls_move_job.py
# Τοπική αναζήτηση. Επιλέγουμε το εργοστάσιο με την μεγαλύτερη καθυστέρηση και το εργοστάσιο με την μικρότερη καθυστέρηση.
# Αφαιρούμε εργασία από το εργοστάσιο με την μεγαλύτερη καθυστέρηση και εξεταζουμε τις θέσεις στο εργοστάσιο με την μικρότερη καθυστέρηση
#************************************************************************************************************************************
        startSequenceLS_MOVE_JOB = copy.deepcopy(startNEHedd)
        sequence_moveJob = {}
        sequence_BestTime_move = {}
        bestTTmove = float("inf")
        for i in range(1000):
            bestTTnewLSmove, startSequenceLSmove = ls_mv.ls_move_job(d,n,m,p,F,startSequenceLS_MOVE_JOB)
            if bestTTnewLSmove < bestTTmove:
                bestTTmove = bestTTnewLSmove
                bestSequenceLSmove = copy.deepcopy(startSequenceLSmove) 
        bestLSmove = bestTTmove

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
        for i in range(1000):
            bestTTnewLSexchange, startSequenceLSexchange = ls_xc.ls_exchange_job(d,n,m,p,F,startSequenceLS_EXCHANGE_JOB)
            if bestTTnewLSexchange < bestTTexchange:
                bestTTexchange = bestTTnewLSexchange
                bestSequenceLSexchange = copy.deepcopy(startSequenceLSexchange) 
        bestLSexchange = bestTTexchange

#************************************ IG solution******************************************************************
#                                       ig.py
# Εφαρμογή του αλγόριθμου Iterated Greedy Algorithm των RUIZ και STUETZLE προσαρμοσμένος σε Due dates
#******************************************************************************************************************
        startSeq_IG = copy.deepcopy(startNEHedd)
        sequence_IG = {}
        bestTTIG = float("inf")
        bestTTnewIG = float("inf")

        
        startSeq_IG, bestTTIG = ig.ig(d,n,m,p,F,startSeq_IG)
        
        # for i in range(10000):
        #     startSeq_IG, bestTTIG = ig.ig(d,n,m,p,F,startSeq_IG)
        #     if bestTTIG < bestTTnewIG:
        #         bestTTnewIG = bestTTIG
        #         bestSequenceIG = copy.deepcopy(startSeq_IG) 
        



#-------------------------------------------------------------------------------------------------------------------------------------------

        if float(best_value) != 0:
            #sumAll = bestNEHedd + bestILS + bestRSLS + bestRSLS_II + bestLSinsert + bestLSmove + bestLSexchange
            min_value = min(bestNEHedd, bestILS, bestRSLS, bestRSLS_II, bestLSinsert, bestLSmove, bestLSexchange, bestTTIG)
            #avgSum = sumAll / 7
            RPD = (float(min_value) - float(best_value)) / float(best_value) * 100 
            RPD = round(RPD,2)

        table.add_row(filename,str(F), str(n), str(m), str(bestNEHedd), str(bestILS), str(bestRSLS), str(bestRSLS_II), str(bestLSinsert), str(bestLSmove), str(bestLSexchange), str(bestTTIG), str(best_value), str(RPD))
        progress.update(task, advance=1)
    end_time = time.time()
    execution_time = end_time - start_time
#-------------------------------------------------------------------------------------------------------------------------------------------


console = Console()

print()
console.print(table)
console.print(f"ΣΥΝΟΛΙΚΟΣ ΧΡΟΝΟΣ ΕΚΤΕΛΕΣΗΣ {execution_time:.2f} δευτερόλεπτα.")