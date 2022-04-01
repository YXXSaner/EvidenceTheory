#基于加权质量的平均法
#1. 计算BOE之间的距离d(m_i,m_j)
##1.1. 计算m_i∪m_j
##1.2. 利用并集的基数构建向量矩阵 vector_m_i,vector_m_j
##1.3. 构建D=矩阵，大小为|m_i∪m_j|*|m_i∪m_j|
##1.4. 利用公式求d(m_i,m_j)

#2. 利用上面的距离导出BOE之间的相似度Sim(m_i,m_j)

#3.利用相似度Sim(m_i,m_j)构建相似矩阵SMM

#4. 计算各个BOE的支持度 Sup(m_i)

#5. 将支持度Sup(m_i)进行规范化转为权重因子 Crd_i

#6. 计算出加权的平均质量(BPA)

#7. 利用Murphy的方法进行迭代计算
#*********************切割线*****************************#
import pandas as pd
import numpy as np
#数据类型规定#
#1、初始状态的BOE的数据类型为字典dict，例如boe1={"A":0.5,"B":0.2,"C":0.3}
# boe1={"A":0.5,"B":0.2,"C":0.3}
# boe2={"A":0,"B":0.9,"C":0.1}
# boe3={"A":0.55,"B":0.1,"AC":0.35}
# boe4={"A":0.55,"B":0.1,"AC":0.35}
# boe5={"A":0.6,"B":0.1,"AC":0.3}
########准备函数区#################
#抽取字典中的key值，并装进集合中，并且返回集合
def focal_Element(boe):
    key_m=[];
    m_key=boe.keys();
    for item in m_key:
        key_m.append(item)
    keym_set=set(key_m);
    return keym_set;
#*********************切割线*****************************#
#计算任意两个BOE中的并集
def setUnion(boeI,boeJ):
    #提取集合
    setBoe1=focal_Element(boeI);
    setBoe2=focal_Element(boeJ);
    return setBoe1.union(setBoe2);
#构建列向量,生成n*2的矩阵
#第一列：vector(boeI)
#第二列：vector(boeJ)
def columnVector(boeI,boeJ):
    unionSets=setUnion(boeI,boeJ);
    list_name=["key","boeI","boeII"];#这是矩阵的第一行
    list_matrix=[];
    list_matrix.append(list_name);
    for item in unionSets:
        list_value = list();
        list_value.append(item)
        if item in boeI.keys():
            value_I=boeI[item];
        else:
            value_I=0;
        list_value.append(value_I);
        if item in boeJ.keys():
            value_J=boeJ[item];
        else:
            value_J=0;
        list_value.append(value_J);
        list_matrix.append(list_value);#将所有的列表装入
    return np.array(list_matrix);
#返回vector_1-vector_2的结果
def vectorDifference(boeI,boeJ):
    vector_1_2=columnVector(boeI,boeJ);#生成记录两个列向量的矩阵
    #下面进行切片操作
    vector_1=vector_1_2[:,(0,1)];#第一个列向量
    vector_2=vector_1_2[:,(0,2)];#第二个列向量
    line,column=vector_1.shape;
    for i in range(1,line):
        for j in range(1,line):
            if(vector_1[i,0]==vector_2[j,0]):
                vector_1[i,1]=float(vector_1[i,1])-float(vector_2[j,1]);
    vector_1[0,1]="boe"
    return vector_1;
#初始化D==矩阵
def initMatrixD(boeI,boeJ):
    vertorDif=vectorDifference(boeI,boeJ);#两个列向量的插值
    lines,columns=vertorDif.shape;
    set_Key=set();
    #获取m1∪m2的值
    for i in range(1,lines):
        set_Key.add(vertorDif[i,0]);
    line_one=["0"];
    for item in set_Key:
        line_one.append(item);
    listD=[];#首先都装入一个矩阵当中
    listD.append(line_one);
    #开始初始化D=矩阵
    for i in range(1,lines):
        tmp_list=[];#临时列表
        tmp_list.append(line_one[i])
        for j in range(1,lines):
            tmp_list.append(0)
        listD.append(tmp_list)
    dMatrix=np.array(listD);#此时dmatrix是初始的矩阵
    return dMatrix;
#对D=矩阵进行赋值,并返回D=矩阵
def matrixD(boeI,boeJ):
    initMatrix=initMatrixD(boeI,boeJ);#生成一个初始化的矩阵
    #下面生成矩阵中的值。
    lines,columns=initMatrix.shape;
    initMatrix=initMatrix[initMatrix[:,0].argsort()]#对行进行排序
    initMatrix=initMatrix[:,initMatrix[0].argsort()]#在对列进行排序
    if(lines!=columns):
        print("初始化矩阵出现错误");
        return;
    #这是两个临时集合。
    list_m=[]
    for i in range(1,lines):
        str_0=initMatrix[i, 0][:]
        set_column=set(str_0)
        list_t = []
        for j in range(1,lines):
            str_1=initMatrix[0,j][:];
            set_line=set(str_1);
            interChild=len(set_line.intersection(set_column));#交集元素的个数做分子
            unionMother=len(set_line.union(set_column));#并集元素的个数做分母
            sum=interChild/unionMother;
            list_t.append(sum)
            set_line.clear();
        list_m.append(list_t)
        set_column.clear();
    initMatrix=np.array(list_m)
    return initMatrix;
#获取两个BOE之间的距离，d(m1,m2)
def getDistance(boeI,boeJ):
    vector_column=vectorDifference(boeI,boeJ);#这是(vector(m1)-vector(m2))的结果，列向量
    x, y = vector_column.shape;
    vector_column=vector_column[1:x,:]#去除第一行
    vector_column=vector_column[vector_column[:,0].argsort()]#按照第0列排序并扩展到其它区域
    x,y=vector_column.shape;
    vector_=vector_column[:,y-1];
    x=vector_.shape[0];
    vector_=vector_.reshape(x,1)
    x,y=vector_.shape;
    list_tmp=[];#将向量中的值的类型改变为float型
    for i in range(0,x):
        sum=float(vector_[i, y - 1])
        list_tmp.append(sum);
    vector_0=np.array(list_tmp).reshape(x,1);#列向量
    vector_T=vector_0.reshape(1,x);#行向量
    #到这里，已经抽取完了两个向量。
    dMatrix=matrixD(boeI,boeJ);#这是D=矩阵,已经按照顺序排好
    result_0=np.dot(vector_T,dMatrix);
    result_1=result_0.dot(vector_0);
    result_finall=(1/2)*result_1[0][0]
    distance=pow(result_finall,1/2);
    return distance;
#获得两个BOE之间的相似度
def getSimilar(boeI,boeJ):
    return 1-getDistance(boeI,boeJ);
#构建相似度矩阵
#*args为可变参数，代表一个元组tuple
def SMM(n,*args):
    SMM_=np.zeros((n,n),dtype=float);#初始化一个矩阵
    for i in range(0,n):
        for j in range(0,n):
            SMM_[i,j]=getSimilar(args[i],args[j]);#赋值，构建SMM矩阵
    return SMM_;
#计算BOE的支持度，并且返回支持率Crdi
#数据类型为字典
def Crdi(n,*args):
    smm=SMM(n,*args);
    if n<1:
        print("Crdi 错误")
        exit(0);
    str_0="m"
    dictSup=dict();#字典，记录支持
    totalSup=0.00
    for i in range(0,n):
        sup= 0.00
        for j in range(0,n):
            if j!=i:
                sup+=smm[i,j]
        str_1 = str_0 + str(i + 1);
        totalSup+=sup;
        if str_1 in dictSup.keys():
            dictSup[str_1]=sup;
        else:
            dictSup[str_1]=sup
    #将SUP转化为支持率Crdi
    for item in dictSup.keys():
        crdi=dictSup[item]/totalSup;
        dictSup[item]=crdi;
    return dictSup
#计算出加权平均质量
def MAE(n,*args):
    dictCrdi=Crdi(n,*args);#这是支持率
    #print(dictCrdi)
    #首先获得并集，装进列表中
    keysList=[];
    for item in args:
        keysList.append(focal_Element(item));
    #求这几个的并集
    keySet=set();
    for item in keysList:
        keySet=keySet.union(item);
    keysList=list(keySet);
    keysList.sort()#排序
    #首先统一元素，不存的值为0
    for item_key in keysList:
        for item_fun in args:
            if item_key not in item_fun.keys():
                item_fun[item_key]=0;
    str_0="m"
    dict_Result = dict();
    for item_key in keysList:
        i = 0;
        values=0.00
        for item_fun in args:
            i = i + 1;
            str_1=str_0+str(i);
            if item_key in item_fun.keys():
                if str_1 in dictCrdi.keys():
                    values+=item_fun[item_key]*dictCrdi[str_1]
        if item_key in dict_Result.keys():
            dict_Result[item_key]=values;
        else:
            dict_Result[item_key] = values;
    #print(dict_Result);
    return dict_Result;
#计算m_empty,直接返回值
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
#计算 m_intersection，返回计算好的。
def computeInter(m_1,m_2):
    F1=focal_Element(m_1);
    F2=focal_Element(m_2);
    thetaSet=F2;
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
    # boe1={"A":0.5,"B":0.2,"C":0.3}
    # boe2={"A":0,"B":0.9,"C":0.1}
    # boe3={"A":0.55,"B":0.1,"AC":0.35}
    # boe4={"A":0.55,"B":0.1,"AC":0.35}
    # boe5={"A":0.6,"B":0.1,"AC":0.3}
    # n=5
    # avgSet=MAE(5,boe1,boe2,boe3,boe4,boe5);
    # weightAvg(5,avgSet);