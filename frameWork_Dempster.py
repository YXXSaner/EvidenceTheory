#基于通用框架的改进的Dempster方法
#本程序并不完善，过于冗余
#
#如果想增加（减少）数据源的个数，那么需要在 def K(X_set,n)和def m(str_one) 函数下，
#1、增加（减少）空集合，及set_1,set_2,这些是用来做 ∩ 运算
#2、增加（减少）for循环
#3、改变if条件语句


import math
#1、首先说明辩框X
set_List=['A','B','C'];
X_set=set(set_List);#变成集合
empty_set=set();#这是一个空集
#2、列出不同证据源的bpa
# m_1={'A':0.98,'B':0.01,'C':0.01};
# m_2={'A':0,'B':0.01,'C':0.99};
k=0.1;#固定值
#e=0.1,0.01,0.001,0.0001;#变化值
e=0.001
z=1-k-e;#z+e+k=1
m_1={'A':e,'B':k,'C':z};
m_2={'A':z,'B':k,'C':e};
#3、计算K值即冲突质量m(ϕ)
def K(X_set,n):
    sum=0.00;
    set_1=set();
    set_2=set();
    if(n<1):
        #print("只有一个证据,Fail！\n");
        return -1;
    #print("当前有{0}个证据来源\n".format(n));
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
    #print(sum);
    return sum;

#4、计算m_∩(A)
def m(str_one):
    sum=0.00
    set_one=set(str_one);#将字符str_one放在一个集合中
    set_2=set();#为了方便集合运算，创建一个临时的空集合
    for m2 in m_2:
        set_2.add(m2);
        if(set_one.intersection(set_2)==set_one):
            sum+=m_1[str_one]*m_2[m2];
        set_2.clear();
    #dict_one=dict.fromkeys(str_one,sum)
    #return dict_one
    return sum;

#5、计算单个的加权因子w(A,m)，A={H1,H2,H3}
def weight_compute(X_set,n,str_one):
    m_insert=m(str_one);
    m_empty=K(X_set,n);
    if m_empty!=1:
        weights = m_insert / (1 - m_empty);
    else:
        print("Failed:m_empty=1")
        exit(0);
    return weights;
#6、计算出所有的加权因子
#以字典的形式返回
def weight_Frame(X_set):
    n=2;
    dict_result=dict();
    for str_one in X_set:
        values=weight_compute(X_set,n,str_one);
        values=round(values,4)
        dict_result.update(dict.fromkeys(str_one,values));
    return dict_result;
#7、计算出在通用框架下Dempster融合之后的值
def combination_Evidence(X_set,n):
    dict_weight=weight_Frame(X_set);#这是权重
    dict_result=dict();#这是结果
    sum=0.000
    for str_item in X_set:
        m_insert=m(str_item);#M∩(H)
        print(str_item,round(m_insert,4))
        m_empty=K(X_set,n);#M(∅)
        m_weight=weight_compute(X_set,n,str_item);#加权因子
        sum=m_insert+m_weight*m_empty;
        #print("m_insert=",m_insert,"m_weight=",m_weight,"m_empty=",m_empty)
        #print("sum",sum)
        sum=round(sum,4)
        dict_result.update(dict.fromkeys(str_item,sum));
    return dict_result;

if __name__ == '__main__':
    print("**********加权因子***************\n");
    print(weight_Frame(X_set));
    print("\n");
    print("**********融合后的结果***********\n")
    print(combination_Evidence(X_set, 2))
