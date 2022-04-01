#D-S证据融合

#本程序并不完善，过于冗余
#并且只支持手动修改证据来源，当前支持3个证据源
#如果想增加（减少）数据源的个数，那么需要在 def K(X_set,n)和def m(str_one) 函数下，
#1、增加（减少）空集合，及set_1,set_2,这些是用来做 ∩ 运算
#2、增加（减少）for循环
#3、改变if条件语句


import math
#1、首先说明辩框X
set_List=['A','B','C'];
X_set=set(set_List);
empty_set=set();#这是一个空集

#2、列出不同证据源的bpa

# m_1={'A':0.98,'B':0.01,'C':0.01};
# m_2={'A':0,'B':0.01,'C':0.99};
m_1={"A":0.4,"B":0.3,"C":0.2,"AB":0.1}
m_2={"A":0.4,"B":0.3,"C":0.2,"AB":0.1}
#3、计算K值,即计算冲突质量
def K(X_set,n):
    sum=0.00;
    set_1=set();
    set_2=set();
    if(n<1):
        print("只有一个证据,Fail！\n");
        return -1;
    print("当前有{0}个证据来源\n".format(n));
    for m1 in X_set:
        set_1.add(m1);
        for m2 in X_set:
            set_2.add(m2);
            #print(type(set_2),set_2)
            if(set_1.intersection(set_2)==set()):
                #此时相交集合为空集合
                sum+=m_1[m1]*m_2[m2];
            set_2.clear()
        set_1.clear();
    print(sum);
    return sum;

#4、计算m(Ai)
def m(k,str_one):
    i=1
    K_=1/(1-k);#归一化因子系数
    sum=0.000
    set_one=set(str_one);#将字符str_one放在一个集合中
    set_2=set();#为了方便集合运算，创建一个临时的空集合
    for m2 in m_2:
        set_2.add(m2);
        if(set_one.intersection(set_2)==set_one):
            # print(str_one,m2,i)
            sum+=m_1[str_one]*m_2[m2];
            # print(m_1[str_one],"*",m_2[m2],"=",sum)
            i+=1
        set_2.clear();
    #计算出某一个m(i),然后将其存储在字典当中
    # dict_one=dict.fromkeys(str_one,sum)
    # print("k=",k)
    # print("1/1-k = ",K_)
    # print("m(A)=",sum*K_)
    # print("sum=",sum)
    # return dict_one;
    dict_one=dict.fromkeys(str_one,sum*K_)
    # print(type(dict_one))
    # print(dict_one)
    return dict_one

if __name__ == '__main__':
    k=K(X_set,2);
    dict_end=dict();
    for set_m in X_set:
        keys,values=m(k,set_m).popitem()
        values=round(values,4)
        dict_end.update(dict.fromkeys(keys,values))
    print(dict_end)
