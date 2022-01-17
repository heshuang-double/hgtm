import numpy as np
import sympy

m=3
r=0.08

def F0(z,x):
    sum0=0
    a=z*(sympy.exp(-m))
    b=m

    for q in range(sympy.floor(1/r)+1):
        Tqa=0
        for n in range(1,q+1):
            Sqn=0
            for k in range(n+1):
                Sqn=Sqn+((-1)**k)/sympy.factorial(k)/sympy.factorial(n-k)*((n-k)**q)

            Tqa=Tqa+Sqn*(a**n)

        Pq=(sympy.exp(a-z))*Tqa*(b**q)/sympy.factorial(q)
        sum0=sum0+Pq*(x**q)

    return sum0
        

def F1(z,x):
    sum1=0
    a=z*(sympy.exp(-m))
    b=m
    
    for q in range(m,sympy.floor(1/r)+1):
        Tqa=0
        for n in range(1,q-m+1):
            Sqn=0
            for k in range(n+1):
                Sqn=Sqn+((-1)**k)/sympy.factorial(k)/sympy.factorial(n-k)*((n-k)**(q-m))

            Tqa=Tqa+Sqn*(a**n)

        Pq=(sympy.exp(a-z))*Tqa*(b**(q-m))/sympy.factorial(q-m)
        sum1=sum1+Pq*(x**(q-m))

    return sum1


def H1_1(z):
    u=sympy.Symbol('u')
    ans=sympy.nsolve(1-F1(z,1)+F1(z,u)-u, u, 0)
    return ans

def Sv(z):
    return (F0(z,1)-F0(z,(H1_1(z))))


z_list=[]
vul=[]
for z in np.arange(0.1,7.1,0.1):
    z_list.append(z)
    vul.append(Sv(z))


f=open('work\\non-uniform\\Sv_avg100\\ER_vul_theory3.txt','w+')  # 若磁盘中无此文件将自动新建
for i in range(len(z_list)):
    f.write(str(format(z_list[i], '.1f')))
    f.write(' ')
    f.write(str(format(float(vul[i]), '.4f')))
    f.write('\n')
f.close()
