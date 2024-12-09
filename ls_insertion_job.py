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
#                                      ls_insertion_job.py
# Επιλέγουμε τυχαία ένα εργοστάσιο και αφαιρούμε 2 εργασίες. Στην συνέχεια τοποθετούμε τις εργασίες στις 
# καλύτερες θέσεις
#********************************************************************************************************

def ls_insertion_job(d,n,m,p,startSeqls):
    #print(startSeqls)

    #startSeqls = copy.deepcopy(startSeq)
    selJobs = {}                    #ΘΕΣΕΙΣ ΜΕ ΕΡΓΑΣΙΕΣ ΠΟΥ ΘΑ ΑΦΑΙΡΕΘΟΥΝ
    inJobs = {}                     #ΟΙ ΤΙΜΕΣ ΤΩΝ ΕΡΓΑΣΙΩΝ ΠΟΥ ΠΡΕΠΕΙ ΝΑ ΠΡΟΣΤΕΘΟΎΝ
    workSequensels = {}             #ΑΚΟΛΟΥΘΙΑ ΠΟΥ ΕΠΕΞΕΡΓΑΖΟΜΑΣΤΕ
    f=len(startSeqls)               #ΣΥΝΟΛΟ ΕΡΓΟΣΤΑΣΙΩΝ
    fact = rand.randint(0, f-1)     #Select one factory randomly

    #Εαν το εργοστάσιο έχει περισσότερες επό δυο εργασίες προχωράμε στην τοπική αναζήτηση
    #Διαφορετικά δεν έχει νόημα η τοπική αναζήτηση
    startSeqls = insertion_Job_OneFact(d,n,m,p,startSeqls,fact)

    #print("START SEQLS", startSeqls)

    bestTTnew = cS.calcTT(d,n,m,p,startSeqls)
    return startSeqls, bestTTnew



def insertion_Job_OneFact(d,n,m,p,startSeqls,Factory):
    selJobs = {} 
    inJobs = {}   
    fact = Factory
    #print(startSeqls)
    #print("startsqls", startSeqls[fact], fact, len(startSeqls[fact]))
    if len(startSeqls[fact])>2:     
        #print("selected FACTORIE > 2 jobs:", startSeqls[fact])
        selJobs[0] = rand.randint(0, len(startSeqls[fact])-1)
        inJobs[0] = startSeqls[fact][selJobs[0]]
        startSeqls[fact].pop(selJobs[0])
        #print("POP JOB:",selJobs[0], "value",inJobs[0], "NEW SEQUENCE", startSeqls[fact])

        selJobs[1] = rand.randint(0, len(startSeqls[fact])-1)
        inJobs[1] = startSeqls[fact][selJobs[1]]
        startSeqls[fact].pop(selJobs[1])
        #print("POP JOB:",selJobs[1], "value",inJobs[1], "NEW SEQUENCE", startSeqls[fact])   
     
        workSequensels = startSeqls[fact]
        #print(workSequensels)

        jobsToInsert = len(inJobs)
        
        #print("sequence=", startSeqls[fact], "SELECTED JOBS", selJobs[0], "value:", inJobs[0], "-", selJobs[1], "value", inJobs[1])
        
        for i in range(jobsToInsert):
            #print("-----------------")
            jobstoCH = len(workSequensels)
            bestTT = float("inf")
            for g in range(0, jobstoCH+1):
                #print("g =", g)
                tmp_seqls = utils.insertion(workSequensels, g, inJobs[i])

                timiTT = cS.calcTToneFact(d,n,m,p, tmp_seqls)
                if(timiTT<bestTT):
                    bestTT = timiTT
                    bestSequence = tmp_seqls
                    #print("in")
                #FactoryC = cS.schedule(n,m,p, tmp_seqls)
                #print(tmp_seqls, timiTT)
                #print(i, g)   
            workSequensels = bestSequence 
            #print("workSeq", workSequensels)
        startSeqls[fact] = workSequensels
    return startSeqls 
#===============================================================================================================
