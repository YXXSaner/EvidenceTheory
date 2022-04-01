sum=0
for i in range(0,3):
    for j in range(0,3):
        if(i==0 and j==0):
            continue;
        if(i+j<=2):
           sum=sum+1
           print("第 ",sum,"种操作","      ","(",i,",",j,")");