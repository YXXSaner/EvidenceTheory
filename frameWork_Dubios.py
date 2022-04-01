#这是在通用框架下的Dubios&Prade规则
#这个新的规则之前没有写过原版的，就直接写改进的吧
#这个程序主要分为：m*、m_intersection、m_empty

#1、确定辩框
theta=['A','B','C'];
theta_set=set(theta);

#2、确定证据源
k=0.1;#固定值
e=0.1;#变化值
z=1-k-e;#因变量
m_1={'A':e,'B':k,'C':z};
m_2={'A':z,'B':k,'C':e};

#2.1 抽取每一个证据源中的焦元，返回一个集合
def focal_Element(m_dict):
    key_m=[];
    m_key=m_dict.keys();
    for item in m_key:
        key_m.append(item)
    keym_set=set(key_m);
    return keym_set;

#3、计算m_empty
def computeEmpty(m_1,m_2,n):
    F1=focal_Element(m_1);
    F2=focal_Element(m_2);
    # 构造空集合
    theta_set1 = set();
    theta_set2 = set();
    empty = set();
    m_empty = 0.00
    for item1 in F1:
        theta_set1.update(item1);
        for item2 in F2:
            theta_set2.update(item2);
            if (theta_set1.intersection(theta_set2) == empty):
                m_empty += m_1[item1] * m_2[item2];
            theta_set2.clear();
        theta_set1.clear();
    return m_empty;

#4、计算m*
def computLocal(m_1,m_2,n,thetaSet):
    F1=focal_Element(m_1);
    F2=focal_Element(m_2);
    #空集合
    f1_set=set();
    f2_set=set();
    empty=set();
    m_local=dict();
    for item1 in F1:
        f1_set.update(item1);
        for item2 in F2:
            f2_set.update(item2);
            if (f1_set.intersection(f2_set) == empty):
                if(f1_set.union(f2_set).intersection(thetaSet)!=empty):
                    sum = m_1[item1] * m_2[item2];
                    str_=item1+"∪"+item2;
                    str_copy=item2+"∪"+item1;
                    #sum = round(sum, 4);
                    if str_copy not in m_local.keys():
                        if str_ in m_local.keys():
                            m_local[str_] = sum;
                        else:
                            m_local[str_]=sum;
                    else:
                        m_local[str_copy]=m_local[str_copy]+sum;
            f2_set.clear();
        f1_set.clear();
    return m_local;

#5、计算 m_intersection
def computeInter(m_1,m_2,thetaSet):
    F1=focal_Element(m_1);
    F2=focal_Element(m_2);
    #空集合
    f1_set=set();
    f2_set=set();
    strSet=set();

    inter=dict();
    for item0 in thetaSet:
        strSet.update(item0);
        sum=0.00
        for item1 in F1:
            f1_set.update(item1);
            for item2 in F2:
                f2_set.update(item2);
                if(f1_set.intersection(f2_set)==strSet):
                    sum+=m_1[item1]*m_2[item2];
                f2_set.clear();
            f1_set.clear();
        inter.update(dict.fromkeys(item0,sum));
        strSet.clear();
    return inter;
#6、计算融合
def combinationEvidence(m_1,m_2,n,thetaSet):
    m_insert=computeInter(m_1,m_2,thetaSet);#字典类型
    m_empty=computeEmpty(m_1,m_2,n);#float类型
    m_local=computLocal(m_1,m_2,n,thetaSet);#字典类型
    #计算出各个w值
    print("***************加权因子********************");
    for item1 in m_local.keys():
        if item1 in m_local:
            m_local[item1]=round(m_local[item1]*m_empty,4);
    print(m_local);
    print();
    print("**************融合后的MASS*****************");
    #m_combination=dict();
    for item0 in thetaSet:
        if item0 in m_insert:
            m_intersection=m_insert[item0];
        else:
            m_intersection=0;
        if item0 in m_local:
            m_c=m_local[item0];
        else:
            m_c=0
        print(item0,round(m_intersection+m_c,4));
    print()
    print("***************intersection*****************");
    print(m_insert);
    return 0;
if __name__ == '__main__':
    print("e = ",e)
    combinationEvidence(m_1,m_2,2,theta_set);