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


    pi = copy.deepcopy(startSeqls)
    bestTT = cS.calcTT(d,n,m,p,pi)
    #print("NEHedd = ", pi, "with best TT", bestTT)
    
    bestTT, pi = rsls.rsls(d,n,m,p,pi, bestTT)
    bestTT = cS.calcTT(d,n,m,p,pi)
    #print("After Local Search",pi, "with best TT",bestTT)

    pib = copy.deepcopy(pi)

    for iteration in range(max_iterations):
        removed_jobs = []
        pi_prime = pi.copy()
        print("iteration:", iteration)
        # Remove one job at a time
        range1 = djobs * n/Factories

        #print(int(range1))
        for _ in range(int(range1)):
            random_factory = random.choice(list(pi_prime.keys()))
            #print("random Factory", random_factory)
            if len(pi_prime[random_factory]) > 0:
                #removed_jobs = pi_prime[random_factory].pop(random.randint(0, len(pi_prime[random_factory]) - 1))
                removed_jobs.append(pi_prime[random_factory].pop(random.randint(0, len(pi_prime[random_factory]) - 1)))
        
        #print("removed Jobs", removed_jobs)
        for job in removed_jobs:
            best_factory, best_position, min_tt = None, None, float('inf')
            for factory in range(Factories):
                for position in range(len(pi_prime[factory]) + 1):
                    test_schedule = copy.deepcopy(pi_prime)
                    test_schedule[factory].insert(position, job)
                    tt = cS.calcTT(d,n,m,p,test_schedule)
                    #print("tt=", tt, "test_shedule=", test_schedule )
                    if tt < min_tt:
                        best_factory, best_position, min_tt = factory, position, tt
            pi_prime[best_factory].insert(best_position, job)
            #print("pi_prime", pi_prime)
        
        # Local search
        bestTTIls2, pi_prime = ils.ils(d,n,m,p, pi_prime, bestTT)
        ttpi_prime = cS.calcTT(d,n,m,p,pi_prime)
        ttpi = cS.calcTT(d,n,m,p,pi)
        ttpib = cS.calcTT(d,n,m,p,pib)


        #print("pi", pi, ttpi)
        #print("pi_prime", pi_prime, ttpi_prime )
        # Acceptance criteria
        if ttpi_prime < ttpi:
            pi = copy.deepcopy(pi_prime)
            if ttpi < ttpib:
                pib = copy.deepcopy(pi_prime)
        elif random.random() <= math.exp(-(ttpi_prime - ttpi) / T):
            pi = copy.deepcopy(pi_prime)
        #print("TELIKO P", pi)
    ttpib = cS.calcTT(d,n,m,p,pib)       
    #print("pB", pib, ttpib )     

    return pib, ttpib