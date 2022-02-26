import numpy as np
import sympy

m=3
r=0.08
maxuse_k=sympy.floor(1/(r*(m-1)))+1


def G0(z,x):
    sum0=0
    for i in range(maxuse_k):
        sum0=sum0+(sympy.exp(-z))*(z**i)/(sympy.factorial(i))*(x**i)
    return sum0


def G1(z,x):
    sum1=0
    for i in range(1, maxuse_k):
        sum1=sum1+i*((sympy.exp(-z))*(z**i)/(sympy.factorial(i)))*(x**(i-1))
    return sum1/z


def H1_1(z):
    u=sympy.Symbol('u')
    ans=sympy.nsolve(1-G1(z,1)+G1(z,u**(m-1))-u, u, 0)
    return ans


def Sv(z):
    return (G0(z,1)-G0(z,(H1_1(z))**(m-1)))

z_list=[]
vul=[]
for z in np.arange(0.1,10.1,0.1):
    z_list.append(z)
    vul.append(Sv(z))


f=open('work\\uniform\\poisson\\Sv_avg100\\ER_vul_theory3.txt','w+')  # 若磁盘中无此文件将自动新建
for i in range(len(z_list)):
    f.write(str(format(z_list[i], '.1f')))
    f.write(' ')
    f.write(str(format(float(vul[i]), '.4f')))
    f.write('\n')
f.close()
