#1、先写出结果的形式
x_result={"A":0,"A|B":0,"B":0,"Ω":0,"empty":0}
#2、输入平均值，为了节省时间，就直接给出average
#average={"A":0.58,"A|B":0,"B":0.4,"Ω":0.02,"empty":0}

#3 抽取每一个证据源中的焦元，返回一个集合
def focal_Element(m_dict):
    key_m=[];
    m_key=m_dict.keys();
    for item in m_key:
        key_m.append(item)
    keym_set=set(key_m);
    return keym_set;
#4、计算m_empty,直接返回值
def computeEmpty(m_1,m_2):
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
#5、计算 m_intersection，返回计算好的。
def computeInter(m_1,m_2):
    F1=focal_Element(m_1);
    F2=focal_Element(m_2);
    #thetaSet=F2;
    thetaSet=focal_Element({"A": 0, "AB": 0, "C": 0, "BC":0,"B":0})
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
        if item0 in inter:
            inter[item0]=sum;
        else:
            inter[item0] = sum;
        #inter.update(dict.fromkeys(item0,sum));
        strSet.clear();
    return inter;
# n:迭代次数
# avgSet:初始的average
def weightAvg(n,avgSet):
    for i in range(1,n):
        if(i==1):
            diedai=computeInter(avgSet,avgSet);#返回没有归一化的交集
            k=computeEmpty(avgSet,avgSet);#冲突质量
            k=1/(1-k);#归一化处理
            for item in diedai.keys():
                if item in diedai:
                    value_=round(diedai[item]*k,4);
                    diedai[item]=value_;
            diedai_0 = diedai;
            print("第 {0} 次迭代结果：{1}".format(i,diedai));
        else:
            diedai_1=computeInter(diedai_0,avgSet);
            k=computeEmpty(diedai_0,avgSet);
            k=1/(1-k);#归一化处理
            for item in diedai_1:
                if item in diedai_1:
                    value_=round(diedai_1[item]*k,4);
                    diedai_1[item]=value_;
            #diedai_0.clear();
            print("第 {0} 次迭代结果：{1}".format(i, diedai_1));
            diedai_0=diedai_1;
            #diedai_1.clear();
if __name__ == '__main__':
    n=2;
    #average_ = {"A": 0.58, "A|B": 0, "B": 0.4, "Ω": 0.02, "empty": 0}
    # average_ = {"A": 0.7, "A|B": 0, "B": 0.25, "Ω": 0.05, "empty": 0}
    average_ = {"A": 0.25, "AB": 0.25, "C": 0.25, "BC":0.25,"B":0}
    weightAvg(n,average_);
