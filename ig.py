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
#                                      ig.py
#  Ο αλγόριθμος Iterated greedy Algorithm για το πρόβλημα DPFSP
# 
#********************************************************************************************************

def ig(d,n,m,p,Factories,startSeqls):
    
    max_iterations = 1000
    djobs = 0.4
    T = 0.8
    bestTT = float("inf")
    minTT = float("inf")


    removed_jobs = []


    π = copy.deepcopy(startSeqls)
    bestTT = cS.calcTT(d,n,m,p,π)
    #print("NEHedd = ", π, "with best TT", bestTT)
    
    bestTT, π = rsls.rsls(d,n,m,p,π, bestTT)
    bestTT = cS.calcTT(d,n,m,p,π)
    #print("After Local Search",π, "with best TT",bestTT)

    πb = copy.deepcopy(π)

    for iteration in range(max_iterations):
        removed_jobs = []
        π_prime = π.copy()
        
        # Remove one job at a time
        range1 = djobs * n/Factories

        #print(int(range1))
        for _ in range(int(range1)):
            random_factory = random.choice(list(π_prime.keys()))
            #print("random Factory", random_factory)
            if len(π_prime[random_factory]) > 0:
                #removed_jobs = π_prime[random_factory].pop(random.randint(0, len(π_prime[random_factory]) - 1))
                removed_jobs.append(π_prime[random_factory].pop(random.randint(0, len(π_prime[random_factory]) - 1)))
        
        #print("removed Jobs", removed_jobs)
        for job in removed_jobs:
            best_factory, best_position, min_tt = None, None, float('inf')
            for factory in range(Factories):
                for position in range(len(π_prime[factory]) + 1):
                    test_schedule = copy.deepcopy(π_prime)
                    test_schedule[factory].insert(position, job)
                    tt = cS.calcTT(d,n,m,p,test_schedule)
                    #print("tt=", tt, "test_shedule=", test_schedule )
                    if tt < min_tt:
                        best_factory, best_position, min_tt = factory, position, tt
            π_prime[best_factory].insert(best_position, job)
            #print("π_prime", π_prime)
        
        # Local search
        bestTTIls2, π_prime = ils.ils(d,n,m,p, π_prime, bestTT)
        ttπ_prime = cS.calcTT(d,n,m,p,π_prime)
        ttπ = cS.calcTT(d,n,m,p,π)
        ttπb = cS.calcTT(d,n,m,p,πb)


        #print("π", π, ttπ)
        #print("π_prime", π_prime, ttπ_prime )
        # Acceptance criteria
        if ttπ_prime < ttπ:
            π = copy.deepcopy(π_prime)
            if ttπ < ttπb:
                πb = copy.deepcopy(π_prime)
        elif random.random() <= math.exp(-(ttπ_prime - ttπ) / T):
            π = copy.deepcopy(π_prime)
        #print("TELIKO P", π)
    ttπb = cS.calcTT(d,n,m,p,πb)       
    #print("pB", πb)     

    return πb, ttπb