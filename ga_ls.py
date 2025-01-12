import calcShedule as cS
import utils
import rsls
import rsls_II as rs2
import ls_insertion_job as ls_ij
import ls_move_job as ls_mv
import ls_exchange_job as ls_xc
import nehedd_new as neh

import copy
import random as rand
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
    
    #GA PARAMETERS
    population_Size = 50
    generation = 0
    generations = 50
    bestTTGARet = float("inf")
    bestSolution = {}
    child1 = {}
    child2 = {}
    R1 = {}
    R2 = {}
    L1 = {}
    L2 = {}
   

    #Create Population *****************************************
    population = create_population(population_Size, Factories, n)
    population_tt = {}
    for pop in range(len(population)):                                      #Calculate TT of each pop
        tt = cS.calcTT(d,n,m,p,population[pop])
        population_tt[pop] = tt      
        #print("population: [", pop, "]", population[pop], "---", tt)
    population[19] = workingSeq_GA

    runTimerGALS = n*m*0.25

    startTimerGALS = time.time()
    timerGALS = 0
    i=0
    #for generation in range(generations):
    while timerGALS < runTimerGALS:
        i = i+1     
        generation = generation+1
        #print("GENERATION: ", generation)
        sorted_data = sorted(population_tt.items(), key=lambda item: item[1])   #Sort Population (Best to Worst)
        #print("Sorted Data Before LS", sorted_data)
        #*************************************************************
        

        #Take the first Individual (BEST) and do local Search*********
        #print("BEST INDIVIDUAL")
        first_key, first_value = sorted_data[0]
        #print("sorted_data", first_key, first_value )
        #print(population[first_key])
        #print("IN LOCALSEARCH BEST")
        workingSeq_GA = copy.deepcopy(population[first_key])
        workingSeq_GARet, bestTTGARet = localSearch(d,n,m,p,Factories, workingSeq_GA)
        population[first_key] = copy.deepcopy(workingSeq_GARet)
        #print("OUT LOCALSEARCH BEST")
        #**************************************************************

        #Take random Individual and do local Search********************
        #print("RANDOM INDIVIDUAL")
        selectPop = rand.randint(1, population_Size-1)
        #print(selectPop)
        #print("IN LOCALSEARCH INDIVIDUAL")
        workingSeq_GA = copy.deepcopy(population[selectPop])
        workingSeq_GAInv, bestTTGAInv = localSearch(d,n,m,p,Factories, workingSeq_GA)
        population[selectPop] = copy.deepcopy(workingSeq_GAInv)
        #print("Individual:", population[selectPop], bestTTGAInv)
        #print("OUT LOCALSEARCH Individual")
        #**************************************************************




        #Sort population after Local Search ***************************
        for pop in range(len(population)):                             
            tt = cS.calcTT(d,n,m,p,population[pop])
            population_tt[pop] = tt      
            #print("population: [", pop, "]", population[pop], "---", tt)
        sorted_data = sorted(population_tt.items(), key=lambda item: item[1]) 
        #print("Sorted Data After LS", sorted_data)
        #**************************************************************


    #Crossover ****************************************************
        
        # Select Parent 1 the best Individual    
        first_key, first_value = sorted_data[0]
        #print("sorted_data", first_key, first_value )
        parent1 = copy.deepcopy(population[first_key])

        # Select Parent 2 random Individual
        selectPop = rand.randint(1, population_Size-1)
        #print(selectPop)
        parent2 = copy.deepcopy(population[selectPop])

        #print()
        #print("PARENT 1 =", len(parent1), parent1,  "PARENT 2 =", len(parent2), parent2)

        #print("crossover START")
        if len(parent1) == len(parent2):
            for facts in range(len(parent1)):
                #if len(parent1[facts]) >= 3:
                    #print(parent1[facts])
                cutPosition = int(len(parent1[facts])/2)
                    #print ("cutPoint",cutPosition)
                R1[facts] = parent1[facts][:cutPosition]
                L1[facts] = parent1[facts][cutPosition:]
                    #print(parent2[facts])
                cutPosition = int(len(parent2[facts])/2)
                    #print ("cutPoint",cutPosition)
                R2[facts] = parent2[facts][:cutPosition]
                L2[facts] = parent2[facts][cutPosition:]
            #print("R1", R1) 
            child1 = R1
            #print("L1", L1) 
            #print("R2", R2) 
            child2 = R2        
            #print("L2", L2)             


        if len(L1) > 0:
            for ins in range(len(L1)):
                for insItem in range(len(L1[ins])):
                    check1 = {}
                    fullCheck = {}
                    #print("item", L1[ins][insItem])
                    bestTTfact = float("inf")
                    for fact in range(len(child1)):
                        jobstoCH = len(child1[fact])
                    
                        for g in range(0, jobstoCH+1):
                            check1 = copy.deepcopy(child1)
                            tmp_seqlsGA = utils.insertion(child1[fact], g, L1[ins][insItem])
                            check1[fact] = copy.deepcopy(tmp_seqlsGA)
                            #print(check1[fact], tmp_seqlsGA)
                            timiTTfact = cS.calcTT(d,n,m,p,check1)
                            #print(check1, timiTTfact)
                            if(timiTTfact<bestTTfact):
                                bestTTfact = timiTTfact
                                fullCheck = copy.deepcopy(check1)
                                #print("FULLOLLL",fullCheck)
                    child1 = copy.deepcopy(fullCheck)  
                population[-1] = child1      
                    #print()
                    #print("child1", cS.calcTT(d,n,m,p,child1))
                    #child1[fact] = bestSequence
            #print("child1:",child1)


        if len(L2) > 0:
            for ins in range(len(L2)):
                for insItem in range(len(L2[ins])):
                    check1 = {}
                    fullCheck = {}
                    #print("item", L2[ins][insItem])
                    bestTTfact = float("inf")
                    for fact in range(len(child2)):
                        jobstoCH = len(child2[fact])
                    
                        for g in range(0, jobstoCH+1):
                            check2 = copy.deepcopy(child2)
                            tmp_seqlsGA = utils.insertion(child2[fact], g, L2[ins][insItem])
                            check2[fact] = copy.deepcopy(tmp_seqlsGA)
                            #print(check1[fact], tmp_seqlsGA)
                            timiTTfact = cS.calcTT(d,n,m,p,check2)
                            #print(check2, timiTTfact)
                            if(timiTTfact<bestTTfact):
                                bestTTfact = timiTTfact
                                fullCheck = copy.deepcopy(check2)
                                #print("FULLOLLL",fullCheck)
                    child2 = copy.deepcopy(fullCheck)  
                population[-2] = child2   
            #print("child2:",child2)
        #print("crossover END")
                    #print()
                    #print("child2", cS.calcTT(d,n,m,p,child2))
                    #child1[fact] = bestSequence

        #print("child1", cS.calcTT(d,n,m,p,child1))    
        #print("child2", cS.calcTT(d,n,m,p,child1))    

        endTimerGALS = time.time()
        timerGALS = endTimerGALS - startTimerGALS 
    
    # Return the best Solution
    first_key, first_value = sorted_data[0]    
    workingSeq_GARet = copy.deepcopy(population[first_key])
    bestTTGARet = cS.calcTT(d,n,m,p, workingSeq_GARet)

    print("GALS :", generation, "timer:", timerGALS)

    return workingSeq_GARet, bestTTGARet

#######################################################################################################################################################    



def create_population(pop_size, num_factories, num_jobs):
    return [create_random_individual(num_factories, num_jobs) for _ in range(pop_size)]


def create_random_individual(num_factories, num_jobs):
    jobs = list(range(num_jobs))  # Jobs ξεκινούν από το 0
    random.shuffle(jobs)

    factories = {i: [] for i in range(num_factories)}
    for i, job in enumerate(jobs):
        factory_key = i % num_factories
        factories[factory_key].append(job)

    return factories


def localSearch(d,n,m,p,Factories, workingSeq_GA):
    
    bestSequenseLS = copy.deepcopy(workingSeq_GA)
    ttBestLS = cS.calcTT(d,n,m,p,workingSeq_GA)

       
    calcTimer = 0
    start_time_ls = time.time()  
    #for rounds in range(100):
    #while runTimer > calcTimer:
        #print("LS TIME:", time_ls)        
    flag = True
    for factory in range(Factories):
        #print()
        #print("factory->", factory, "round", rounds, "SEQUENCE",workingSeq_GA)
        workingSeq_GA = ls_ij.insertion_Job_OneFact(d,n,m,p,workingSeq_GA,factory)
    count = 0
    while flag:
        count = count+1
        workingSeq_GA_check = copy.deepcopy(workingSeq_GA)
        bestW, workingSeq_GA = ls_mv.ls_move_job(d,n,m,p,Factories,workingSeq_GA)
        bestW, workingSeq_GA = ls_xc.ls_exchange_job(d,n,m,p,Factories,workingSeq_GA)
        ttMid = cS.calcTT(d,n,m,p,workingSeq_GA)
        #print("sequense Middle", workingSeq_GA, ttMid)
        for factory in range(Factories):
            if (workingSeq_GA_check[factory] == workingSeq_GA[factory]) or count > 20:
                #print ("same")
                flag = False
            else:
                workingSeq_GA = ls_ij.insertion_Job_OneFact(d,n,m,p,workingSeq_GA,factory)
                #print ("not same")
    
    bestTTGA = cS.calcTT(d,n,m,p,workingSeq_GA)
    #print("sequense After", workingSeq_GA, bestTTGA)
    if(bestTTGA < ttBestLS):
        bestSolution = copy.deepcopy(workingSeq_GA) 
        workingSeq_GARet = copy.deepcopy(workingSeq_GA) 
        ttBestOveraAll = bestTTGA
        bestTTGARet = bestTTGA
        bestSequenseOverAll = copy.deepcopy(workingSeq_GA)
        ttBestOveraAll = cS.calcTT(d,n,m,p,workingSeq_GA)
        
        #print("***")
        #print("FIND NEW BEST OVER ALL:",bestSequenseOverAll, "--", ttBestOveraAll)
    else:
        bestSolution = copy.deepcopy(bestSequenseLS) 
        bestTTGARet = ttBestLS
    end_Time_ls = time.time() 
    calcTimer = end_Time_ls - start_time_ls
    return bestSolution, bestTTGARet

































    # parent1 = workingSeq_GA


    # jobs = list(range(1, n + 1))
    # random.shuffle(jobs)
    # # Κατανομή εργασιών σε εργοστάσια
    # split_points = sorted(random.sample(range(1, n), Factories - 1))
    # parent2 = [jobs[i:j] for i, j in zip([0] + split_points, split_points + [len(jobs)])]


#****************************************************************************************************

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

   