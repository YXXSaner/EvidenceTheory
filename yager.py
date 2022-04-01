#这是孙全论文中提及的Yager的公式
#本程序并不完善，过于冗余
#并且只支持手动修改证据来源，当前支持3个证据源
#如果想增加（减少）数据源的个数，那么需要在 def K(X_set,n)和def m(str_one) 函数下，
#1、增加（减少）空集合，及set_1,set_2,这些是用来做 ∩ 运算
#2、增加（减少）for循环
#3、改变if条件语句



#1、首先说明辩框X
set_List=['A','B','C'];
X_set=set(set_List);
empty_set=set();#这是一个空集

#2、列出不同证据源的bpa

# m_1={'A':0.98,'B':0.01,'C':0.01};
# m_2={'A':0,'B':0.01,'C':0.99};
m_1={'A':0.98,'B':0.01,'C':0.01};
m_2={'A':0,'B':0.01,'C':0.99};
m_3={'A':0.9,'B':0,'C':0.1}
#3、计算K值
def K(X_set,n):
    sum=0.00;
    set_1=set();
    set_2 = set();
    set_3=set();
    if(n<1):
        print("只有一个证据,Fail！\n");
        return -1;
    print("当前有{0}个证据来源\n".format(n));
    for m1 in X_set:
        set_1.add(m1);
        for m2 in X_set:
            set_2.add(m2)
            for m3 in X_set:
                set_3.add(m3)
                if(set_1.intersection(set_2).intersection(set_3)==set()):
                    sum+=m_1[m1]*m_2[m2]*m_3[m3];
                set_3.clear()
            set_2.clear()
        set_1.clear();
    return sum;

#4、计算A≠{},X时的 m(A)
def m(str_one):
    sum = 0.000
    set_one = set(str_one);  # 将字符str_one放在一个集合中
    set_2 = set();  # 为了方便集合运算，创建一个临时的空集合
    set_3 = set();
    for m2 in m_2:
        set_2.add(m2);
        for m3 in m_3:
              set_3.add(m3)
              if (set_one.intersection(set_2).intersection(set_3) == set_one):
                  sum += m_1[str_one] * m_2[m2];
              set_3.clear();
        set_2.clear();
    dict_one = dict.fromkeys(str_one, sum)
    return dict_one
#5、计算 A=X时，m(X)
def X(k):
    return k+0;

if __name__ == '__main__':
    k=K(X_set,2);
    dict_end=dict();
    for set_m in X_set:
        keys,values=m(set_m).popitem()
        values=round(values,4)
        dict_end.update(dict.fromkeys(keys,values))
    print("*******k完成*************\n");
    print("k = ",k);
    print("*********m(A)完成*********\n")
    key="X";
    value=round(X(k),4);
    dict_end.update(dict.fromkeys(key,value))
    print("*********全部完成******\n")
    print(dict_end)