import algorithms_correct as algos
import math

def distance(x, y):
    sum = 0
    for i in range(len(x)):
        sum += (x[i] - y[i])**2
    return math.sqrt(sum)

def scalar_mult(scalar, vec):
    return list( map(lambda y: y * scalar, vec))

def vector_add(veca, vecb):
    return list( map(lambda a, b: a + b, veca, vecb))

# veca + scalar*vecb
def vector_addmult(veca, scalar, vecb):
    return list( map(lambda a, b: a + scalar*b, veca, vecb))

def rosenbrock(func, dim, epsylon, alpha, beta, delta_starting, a, b):
    #выбрать в качестве d1..dn направления
    d = []
    for i in range(dim):
        di = [0] * dim
        di[i] = 1
        d.append(di)
    
    delta = delta_starting
    x = [0] * dim
    y = x
    y_prev = y
    k = j = 0
    step = "step1"
    while step != "end":
        if step == "step1":
            new_value_try = func(vector_addmult(y, delta[j], d[j]))
            if(new_value_try < func(y)):
                #success
                y = new_value_try
                delta[j] = scalar_mult(alpha, delta[j])
            else:
                #failure
                y = y
                delta[j] = scalar_mult(beta, delta[j])

            if j < dim:
                j = j + 1
                step = "step1"
            else:
                step = "step2"
        elif step == "step2":
            if func(y) < func(y_prev):
                y_prev = y
                step = "step1"
            elif (func(y) < func(x)): # func(y) == func(y_prev)
                step = "step3"
            else: # func(y) == func(x)
                for i in range(dim):
                    if abs(delta[j]) >= epsylon:
                        y_prev = y
                        j = 1
                        step = "step1"
                        break
                    else: # криво, но пофиг    
                        step = "end"
        elif step == "step3":
            if distance(x, y) < epsylon:
               x = y
               step = "end"
            else:
                y_prev = y
                x = y
                

           """
           Шаг 3. Построить новое множество линейно независимых и взаимно
            ортогональных направлений в соответствии с процедурой Грама-Шмидта и
            вернуться к шагу 1.
           """ 

            


