#基于pignistic transform证据冲突的度量标准
#作者的度量指标为cf(m(empty),difBetP)
##其中m(empty)就是Dempster规则中1/(1-k)中的k
##difBetP是两个不同的BBA之间的赌博信度的差值
import numpy as np;
import pandas as pd;
#辩框
# theta=set(["A","B","C","D","E"]);
#BBA的格式如下
# bba1={"A":0.2,"B":0.2,"C":0.6}
# bba2={"A":0.2,"B":0.2,"C":0.6}

#抽取字典中的key值，并装进集合中，并且返回集合
def focal_Element(boe):
    key_m=[];
    m_key=boe.keys();
    for item in m_key:
        key_m.append(item)
    keym_set=set(key_m);
    return keym_set;
#进行pignistic变换
#BBA——>BetP
##输入参数：辩框，BBA
##返回一个字典类型的BetP
def transform(bba):
    bba_set=focal_Element(bba);#抽取字典中的key值
    if "empty" in bba.keys():
        m_empty=bba["empty"];
    else:
        m_empty=0
    BetP=dict();#字典类型
    item_A=set();
    item_B=set();
    for variable in bba_set:
        sum=0.00
        item_A.update(variable);
        for B in bba_set:
            item_B.update(B);
            A_insert_B=item_A.intersection(item_B);#A与B的交集
            size_insert=len(A_insert_B);
            size_B=len(B);#|B|
            mass_B = bba[B];#B的质量
            sum+=(size_insert/size_B)*(mass_B/(1-m_empty));#求BetP(A)
            item_B.clear();  # 这样是为了使，集合中只包含一个变量
        # 记录一组BBA中的BetP
        if variable in BetP.keys():
            BetP[variable] = sum;
        else:
            BetP[variable] = sum;
        item_A.clear();
    return BetP;
##获得最大的difBetP
def difBetP(bba1,bba2):
    #首先我们假设bba1，bba2已经统一化处理了,这是正确的
    #这里我发现了自己之前的错误，虽然BBA中有些元素质量为0
    #但是其BetP并不为0。
    for item in bba1:
        if item not in bba2.keys():
            bba2[item] = 0;
    for item in bba2:
        if item not in bba1.keys():
            bba1[item]=0;
    setbba1=focal_Element(bba1);
    setbba2=focal_Element(bba2);
    #进行bba的pignistic 转换
    betP1=transform(bba1);#betP
    betP2=transform(bba2);#betP
    #定义一个存放差值的工具
    difbetp=dict();
    for item_1 in setbba1:
        for item_2 in setbba2:
            if item_1==item_2:
                value=abs(betP1[item_1]-betP2[item_2]);
                if item_1 in difbetp.keys():
                    difbetp[item_1]=value;
                else:
                    difbetp[item_1] = value;
    maxdifBetP=max(difbetp.values());#只要找到其中的最大值即可
    maxdifBetP=round(maxdifBetP,4);#保留4位数
    return maxdifBetP;
