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
#                                           calcShedule.py
#       Συναρτήσεις για τον υπολογισμό του makeSpan και του χρόνου καθυστέρησης μιας ακολουθίας
#********************************************************************************************************


# Συνάρτηση που υπολογίζει για μια συγκεκριμένη ακολουθία τους χρόνους εκτέλεσης μιας εργασίας σύμφωνα πάντα με τον 1ο αλγόριθμο του NEH
def schedule(n_jobs, n_machines, p, solution):
    C = np.zeros((n_jobs, n_machines)) #Δημιουργεί έναν πίνακα με μέγεθος n_jobs x n_machines και τον γεμίζει με μηδενικά
    for idx, j in enumerate(solution): #Για κάθε θέση της ακολουθίας (όπου idx->η θέση του πίνακα ακολουθίας και όπου j->η τιμή της θέσης)
        for i in range(n_machines):
            if idx == 0: #Εάν εξετάζουμε την πρώτη εργασία της ακολουθίας
                if i==0: #Εάν βρισκόμαστε στην πρώτη μηχανή
                    C[j,i] = p[j,i] #Αντιστοιχούμε την αρχική τιμή  
                    #print("j=",j, "i=", i)
                else:
                    C[j,i] = C[j,i-1] + p[j,i] #Για τις επόμενες μηχανές και την πρώτη εργασία, αθροίζουμε την τρέχουσα τιμή με την προηγούμενη τιμή  
                    #print("j=",j, "i=", i)                   
            else:
                if i == 0: #Εάν δεν βρισκόμαστε στην πρώτη εργασία της ακολουθίας αλλά στην πρώτη μηχανή
                    C[j,i] = C[solution[idx-1],i] + p[j,i] # Αθροίζουμε την τρέχουσα τιμή με την προηγούμενη εργασία στην ίδια μηχανή 
                    #print("j=",j, "i=", i)                   
                else:
                    #Αλλιώς επιλέγουμε την μεγαλύτερη τιμή ανάμεσα στην τιμή του χρόνου της εργασίας στην προηγούμενη μηχανή και του χρόνου της προηγούμενης εργασίας στην ίδια μηχανή
                    #και το αθροίζουμε με τον τρέχων χρόνο εργασίας
                    C[j,i] = max(C[j,i-1], C[solution[idx-1],i]) + p[j,i] 
                    #print("j=",j, "i=", i)                        
    #print(C)                
    return C

# Χρόνος ολοκλήρωσης μιας συγκεκριμένης ακολουθίας
def makespan(job_sequence, C): # Με τους παρακάτω τελεστές παίρνουμε την τελευταία τιμή του πίνακα με τους χρόνους που αντιστοιχεί στον τελικό χρόνο εκτέλεσης
    return C[job_sequence[-1], -1]

def calcTT(d,n,m,p,startSeq):

    f = 0    
    f=len(startSeq)

    
    sumTT = 0
    for fn in range(f):
        FactoryC = schedule(n, m, p, startSeq[fn])
        #print("FACTORY : [", fn ,"] -> ",startSeq[fn])
        inTT = 0
        for idJob, job in enumerate(startSeq[fn]):
            inTT = FactoryC[startSeq[fn][idJob],-1] -  d[job]
            if(inTT > 0):
                sumTT = sumTT + inTT
        sumTT - sumTT + sumTT
    #print("SUMTT :", sumTT)
    return sumTT


def calcTToneFact(d,n,m,p,workSeq):
    sumTT = 0
    FactoryC = schedule(n, m, p, workSeq)
    #print("FACTORY : [", fn ,"] -> ",startSeq[fn])
    inTT = 0
    for idJob, job in enumerate(workSeq):
        inTT = FactoryC[workSeq[idJob],-1] -  d[job]
        if(inTT > 0):
            sumTT = sumTT + inTT
        sumTT - sumTT + sumTT
    #print("SUMTT :", sumTT)
    return sumTT