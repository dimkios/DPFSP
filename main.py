import loadfile as lf

import nehedd as nh
import ect_solution as ect
import time

#ΕΠΙΛΟΓΗ DATASET


#ΦΟΡΤΩΣΗ DATASET
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Large/Ta012_6.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_1.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/test.txt')

startSeq = {}
print(n)
print(F)

print("============ dataset loaded ===============")
for j in range(n):
    print("job=[",j,"]",  end="", flush=True)
    for i in range(m):
        print("machine=[", i,"] -> ", p[j,i], "-", end="", flush=True)
    print("duedate = ",j, d[j], "", end="", flush=True) 
    print() 
print("============================================")   

startSeq = nh.nehedd(d,n,m,p,F) 
print(startSeq)

ectSequence, ectC = ect.ect_solution(d,n,m,p,F,startSeq)
dueDateFaultSum = 0
dueDateFault = 0


for fctr in range(F):
        print("Job Sequence on Factory: [ ",fctr," ]", ectSequence[fctr]) #, ectC[ectSequence[fctr][-1], -1])
        for idx, seq in enumerate(ectSequence[fctr]):
             dueDateFault = 0
             dueDateFault = ectC[fctr][idx, m-1] - d[seq]
             if dueDateFault > 0:
                  dueDateFaultSum += dueDateFault
             print(seq, ectSequence[fctr][idx], ectC[fctr][idx, m-1], dueDateFault )

print("TOTAL TT = ", dueDateFaultSum)
 #return C[job_sequence[-1], -1]

#nh.nehedd(d,n,m,p,F)
#ΕΠΙΛΟΓΗ ΑΛΓΟΡΙΘΜΟΥ

#ΕΞΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ


