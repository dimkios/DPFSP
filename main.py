import loadfile as lf

import nehedd as nh
import ect_solution as ect
import time

#ΕΠΙΛΟΓΗ DATASET


#ΦΟΡΤΩΣΗ DATASET
n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Large/Ta012_6.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_2_4_2_1.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/I_4_8_3_2.txt')
#n,m,F,p,d = lf.read_dpfsp_dataset('./dataSet/Small/test.txt')
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
#print(d)



ect.ect_solution(d,n,m,p,F)
#nh.nehedd(d,n,m,p,F)
#ΕΠΙΛΟΓΗ ΑΛΓΟΡΙΘΜΟΥ

#ΕΞΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ


