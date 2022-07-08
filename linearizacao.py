import numpy as np

n_dados = int(input("número de dados coletados: "))
rep = int(input("digite quantas vezes foram feitas as medições para calcular o erro: "))
erro_instrumental = float(input("digite o erro instrumental: "))

y_raw = [(lambda x: [float(input(f"\ny{x+1}.{i+1}: ")) if i == 0 else float(input(f"y{x+1}.{i+1}: ")) for i in range(rep)])(i) for i in range(n_dados)]

y = [(lambda x,y: [round(np.mean(x),5), round(np.sqrt(((np.std(x,ddof=1))/np.sqrt(len(x)))**2+y**2),5)])(y_raw[i],erro_instrumental) for i in range(len(y_raw))]

x = [float(input(f"\nx{i+1}: ")) if i == 0 else float(input(f"x{i+1}: ")) for i in range(n_dados)]

# v = [round(x[i]/y[i][0],5) for i in range(len(y))]
# errov = [np.mean(v), (np.std(v,ddof=1))/np.sqrt(len(v))]

# print(f"v = {v} \nerrov = {errov[0]} +/- {errov[1]}")

lny = [round((np.log(i[0])),5) for i in y]
erroy = [round((i[1]/i[0]),5) for i in y]
lnx = [round(np.log(i),5) for i in x]

# lnv = [round(np.log(i),5) for i in v]
print('-----------------------------------------------------------------')

for i in y: print(f'y{y.index(i)+1}: {i[0]} +/- {i[1]}')

print(f'\nlny: {lny} \nerro de y: {erroy} \nlnx: {lnx}\n')

def somatorio(v, a=1, b=1, c=1, d=lnx, wi = erroy):
    n = len(lny); soma = 0
    for i in range(n):
        if v == 1:
            soma += (1/wi[i]**2)
        elif v == 2:
            soma += a[i]*(1/wi[i]**2)
        elif v == 3:
            soma += a[i]*b[i]*(1/wi[i]**2)
        elif v == 4:
            soma += a[i]*b[i]*c[i]*(1/wi[i]**2)
        elif v == 5:
            soma += (d[i]**2)*(1/wi[i]**2)
    return soma

soma1 = (somatorio(1)) #so com o wi
soma2 = (somatorio(3, lnx, lny)) #wi, xi e yi
soma3 = (somatorio(2, lny)) #so com o lny
soma4 = (somatorio(2, lnx)) #so com o lnx
soma5 = (somatorio(5)) # wi e lnx^2

delta = (soma1*soma5 - (soma4**2))

a = ((soma1*soma2) - (soma3*soma4))/delta

b = ((soma3*soma5) - (soma2*soma4))/delta

erroa = (soma1/delta)**0.5

errob = (soma5/delta)**0.5

for i in range(len(erroy)): print(f'w{i+1} = {round((1/erroy[i]**2),5)}')

print(f'\nsoma1 = {round(soma1, 5)}\nsoma2 = {round(soma2, 5)}\nsoma3 = {round(soma3, 5)}\nsoma4 = {round(soma4, 5)}\nsoma5 = {round(soma5, 5)}\ndelta = {round(delta, 5)}\n\na = {round(a, 5)} +/- {round(erroa, 5)}\nb = {round(b, 5)} +/- {round(errob, 5)}\n')

print("Esses valores consideram o eixo y como sendo o eixo que possui erros estatisticos e/ou experimentais. O eixo x não possui erros. Para calcular os erros no eixo x, basta fazer a inversa da função obtida na linearização, ou seja, y = (1/a)x - b/a")