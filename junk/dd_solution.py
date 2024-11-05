import numpy as np

#=======================================================================================================
#                    ΠΡΟΓΡΑΜΜΑ ΜΕΤΑΠΤΥΧΙΑΚΩΝ ΣΠΟΥΔΩΝ ΠΛΗΡΟΦΟΡΙΚΗΣ ΚΑΙ ΔΙΚΤΥΩΝ
#                                    ΠΑΝΕΠΙΣΤΗΜΙΟ ΙΩΑΝΝΙΝΩΝ
#
#                      Distributed Permutation Flow-Shop Scheduling Problem
#
#********************************************************************************************************
#                                   ΚΙΟΣΣΕΣ ΔΗΜΗΤΡΙΟΣ ΑΜ 163
#********************************************************************************************************
#                                           dd_solution.py
#********************************************************************************************************
#                           Solution based on min duedate time  (TT)
#   1). Παίρνουμε την ακολουθία που υπλογίσαμε με την συνάρτηση nehedd.
#   2). Μοιράζουμε τις εργασίες στα εργοστάσια λαμβάνοντας υπόψη το μικρότερο σφάλμα duedate
#   Παίρνουμε κάθε εργασία με την σειρά της ακολουθίας nehedd και την προσθέτουμε στο κάθε εργοστάσιο.
#   Αν στο εργοστάσιο υπάρχουν ήδη εργασίες υπολογίζουμε τους χρόνους συνυπολογίζοντας τους χρόνους των 
#   προηγούμενων εργασιών. Η εργασία τοοποθετείται στο εργοστάσιο στο οποίο το τελικό duedate error είναι 
#   το μικρότερο.
#========================================================================================================

def dd_solution(duedate, jobs, machines, p, Factories, startSeq):
    
    FactorySeq={}                   #Ακολουθία που προκύπτει για κάθε εργοστάσιο
    FactoryRound={}                 #Χρόνος εκτέλεσης των εργασιών ενός εργοστασίαυ
    FactoryDD={}                    #Κρατάμε δείκτες των duedates 
    FactoryPointer={}               #Δείκτης της τρέχουσας θέσης ενός εργοστασίου. Εξαρτάται από τις εργασίες που τοποθετούντε κάθε φορά σε ένα εργοστάσιο
    FactoryC={}                     #Χρόνοι εκτέλεσης των εργασιών σε ένα εργοστάστιο για μια συγκεκριμένη εργασία

    for j in range(Factories):
        FactoryC[j] = np.zeros((jobs, machines))
        FactorySeq[j] = []
        FactoryDD[j] = [-1] * jobs
        FactoryRound[j] = []

    for idx, j in enumerate(startSeq):
        for f in range(Factories):
            pointer = ((np. count_nonzero(FactoryC[f]))/machines)
            poi = int(pointer)
            roundTime = 0
            for i in range(machines):
                
                if idx == 0: #Εάν εξετάζουμε την πρώτη εργασία της ακολουθίας
                    if i==0: #Εάν βρισκόμαστε στην πρώτη μηχανή
                        FactoryC[f][poi,i] = p[j,i] #Αντιστοιχούμε την αρχική τιμή  
                    else:
                        FactoryC[f][poi,i] = FactoryC[f][poi,i-1] + p[j,i] #Για τις επόμενες μηχανές και την πρώτη εργασία, αθροίζουμε την τρέχουσα τιμή με την προηγούμενη τιμή                     
                else:
                    if i == 0: #Εάν δεν βρισκόμαστε στην πρώτη εργασία της ακολουθίας αλλά στην πρώτη μηχανή
                        FactoryC[f][poi,i] = FactoryC[f][poi-1,i] + p[j,i] # Αθροίζουμε την τρέχουσα τιμή με την προηγούμενη εργασία στην ίδια μηχανή    
                        #print("FACTORY FactoryC[f][poi-1,i]",poi-1,"",i,"->",FactoryC[f][poi-1,i],"+ p[j,i]",j,i,p[j,i])               
                    else:
                        #Αλλιώς επιλέγουμε την μεγαλύτερη τιμή ανάμεσα στην τιμή του χρόνου της εργασίας στην προηγούμενη μηχανή και του χρόνου της προηγούμενης εργασίας στην ίδια μηχανή
                        #και το αθροίζουμε με τον τρέχων χρόνο εργασίας
                        FactoryC[f][poi,i] = max(FactoryC[f][poi,i-1], FactoryC[f][poi-1,i]) + p[j,i]    
                        #print("FACTORY  FactoryC[f][poi-1,i]----> max of",FactoryC[f][poi,i-1]," or",FactoryC[f][poi-1,i],"+",p[j,i] )  
            #print(FactoryC[f]) 
            
            FactoryPointer[f] = poi
            for round in range(poi+1):
                sTime=0
                if FactoryDD[f][round] == -1:
                    #print(FactoryC[f][round, machines-1], duedate[j] )
                    sTime = FactoryC[f][round, machines-1] - duedate[j] 
                else:
                    #print(duedate[FactoryDD[f][round]] )
                    sTime = FactoryC[f][round, machines-1] - duedate[FactoryDD[f][round]]     
                #print("FactoryDD",FactoryDD[f][round])     
                #sTime = FactoryC[f][round, machines-1] - duedate[startSeq[round]] 
                #print(FactoryC[f][round, machines-1], duedate[j], j , startSeq[round], poi, FactoryDD[f][poi])
                #print("sTime=", sTime)
                if sTime > 0:
                    roundTime = roundTime + sTime

            #print("RoundTime =",roundTime)
            FactoryRound[f] = roundTime       
            #print("FactoryC [", f ,"] - [poi]", poi, "i",i, FactoryC[f][poi,i], "j=", j) 
            #print(FactoryRound[f])     
        #print("FactoryRound, pointer", FactoryRound, poi)   
        #print(min(FactoryRound, key=FactoryRound.get))
        
        bestinRound = min(FactoryRound, key=FactoryRound.get)
        #print("best in round =",bestinRound)
        #print("j = ", j, "f=", f, "poi=", poi)
        FactorySeq[bestinRound].append(j)
        FactoryDD[bestinRound][poi] = j
        for fctr in range(Factories):
            
            if fctr != bestinRound:
                for imach in range(machines):
                    FactoryC[fctr][FactoryPointer[fctr], imach] = 0
            #print("Factory = ", fctr)
            #print("job=", j)
            #print(FactoryC[fctr])
        #print("*************************** end of Factories round ******************************")   

    #for fctr in range(Factories):
    #    for ikkk, jkkk in enumerate(FactorySeq[fctr]):
    #        print(ikkk, jkkk)
    #S        print("Job Sequence on Factory: [ ",fctr," ]", FactorySeq[fctr][ikkk], FactoryC[fctr][ikkk][machines-1])
            #print(FactorySeq[fctr])   
            #print(FactoryDD[fctr])
        #print("=================================================================================")
    return FactorySeq, FactoryC