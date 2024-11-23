import calcShedule as cS
import ils
import rsls
import rsls_II as rs2
import ls_insertion_job as ls_ij
import ls_move_job as ls_mv
import ls_exchange_job as ls_xc

import copy
import os
import csv
import time
import math

import random
#=======================================================================================================
#                    ΠΡΟΓΡΑΜΜΑ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΣΠΟΥΔΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΔΙΚΤΥΩΝ
#                                    ΠΑΝΕΠΙΣΤΗΜΙΟ ΙΩΑΝΝΙΝΩΝ
#
#                      Distributed Permutation Flow-Shop Scheduling Problem
#
#********************************************************************************************************
#                                   ΚΙΟΣΣΕΣ ΔΗΜΗΤΡΙΟΣ ΑΜ 163
#********************************************************************************************************
#                                      ga_ls.py
#  Υβρισικό γενετικός αλγόριθμος για το πρόβλημα DPFSP
# 
#********************************************************************************************************

def ga(d,n,m,p,Factories,startSeqls):
    workingSeq_GA = copy.deepcopy(startSeqls)
    
    population_Size = 20
    generations = 50


    population = initialize_population(n, m, Factories, population_Size)
    
    
    
    
    
    
    bestTT = float("inf")
    minTT = float("inf")


    ttBegin = cS.calcTT(d,n,m,p,workingSeq_GA)
    print("sequense Before", workingSeq_GA, ttBegin)

    flag = True
    for factory in range(Factories):
        workingSeq_GA = ls_ij.insertion_Job_OneFact(d,n,m,p,workingSeq_GA,factory)

    while flag:
        workingSeq_GA_check = copy.deepcopy(workingSeq_GA)
        bestW, workingSeq_GA = ls_mv.ls_move_job(d,n,m,p,Factories,workingSeq_GA)
        bestW, workingSeq_GA = ls_xc.ls_exchange_job(d,n,m,p,Factories,workingSeq_GA)
        ttMid = cS.calcTT(d,n,m,p,workingSeq_GA)
        print("sequense Middle", workingSeq_GA, ttMid)
        for factory in range(Factories):
            if workingSeq_GA_check[factory] == workingSeq_GA[factory]:
                print ("same")
                flag = False
            else:
                workingSeq_GA = ls_ij.insertion_Job_OneFact(d,n,m,p,workingSeq_GA,factory)
                print ("not same")
                

    bestTTGA = cS.calcTT(d,n,m,p,workingSeq_GA)

    print("sequense After", workingSeq_GA, bestTTGA)


    parent1 = workingSeq_GA


    jobs = list(range(1, n + 1))
    random.shuffle(jobs)
    # Κατανομή εργασιών σε εργοστάσια
    split_points = sorted(random.sample(range(1, n), Factories - 1))
    parent2 = [jobs[i:j] for i, j in zip([0] + split_points, split_points + [len(jobs)])]


    # print("parent 1", parent1, "parent 2", parent2)



    # child1 = [[] for _ in range(Factories)]
    # child2 = [[] for _ in range(Factories)]
    
    # for factory in range(Factories):
    #     # Τυχαίο σημείο διαχωρισμού
    #     split_point = random.randint(0, len(parent2[factory]))

    #     # Εργασίες του δεύτερου γονέα
    #     left2 = parent2[factory][:split_point]
    #     right2 = parent2[factory][split_point:]
        
    #     # Δημιουργία παιδιού 1
    #     remaining1 = [job for job in parent1[factory] if job not in right2]
    #     child1[factory] = remaining1 + right2

    #     # Δημιουργία παιδιού 2
    #     left1 = parent1[factory][:split_point]
    #     right1 = parent1[factory][split_point:]
    #     remaining2 = [job for job in parent2[factory] if job not in right1]
    #     child2[factory] = remaining2 + right1

    # # Διόρθωση διπλότυπων και προσθήκη ελλείψεων
    # def repair_child(child):
    #     all_jobs = set(range(1, n-1))
    #     used_jobs = {job for factory_jobs in child for job in factory_jobs}
    #     missing_jobs = list(all_jobs - used_jobs)
    #     random.shuffle(missing_jobs)  # Ανακατεύουμε τις ελλείπουσες

    #     seen = set()
    #     for factory in child:
    #         for i, job in enumerate(factory):
    #             if job in seen:  # Αν υπάρχει διπλότυπο
    #                 if len(missing_jobs) > 0:
    #                     factory[i] = missing_jobs.pop()
    #             else:
    #                 seen.add(job)

    # repair_child(child1)
    # repair_child(child2)


    # print("child 1", child1, "child 2" , child2)


    return workingSeq_GA, bestTTGA



def initialize_population(num_jobs, machines, num_factories, pop_size):
    """
    Δημιουργία αρχικού πληθυσμού.
    """
    population = []
    for _ in range(pop_size):
        jobs = list(range(1, num_jobs + 1))
        random.shuffle(jobs)
        # Κατανομή εργασιών σε εργοστάσια
        split_points = sorted(random.sample(range(1, num_jobs), num_factories - 1))
        factories = [jobs[i:j] for i, j in zip([0] + split_points, split_points + [len(jobs)])]
        population.append(factories)
    return population