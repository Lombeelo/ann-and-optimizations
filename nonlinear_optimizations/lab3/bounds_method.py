import algorithm_multidimensional as mulalg
import matplotlib.pyplot as plt
import numpy as np

def bounds_method(f, g, alpha, x_0, mu, epsylon, beta):
    log = []
    k = 1
    x_i = x_0

    while True:
        x_i = list(mulalg.cyclic_coordinate_descend_nolog(lambda x: f(x) + mu * alpha(g(x)), 0.01, x_i,  [-10,10]))
        log.append(dict(k=k, mu=mu, xknext=x_i, fxk=f(x_i), alphax=alpha(g(x_i)), omega=f(x_i) + mu * alpha(g(x_i)), mualpha=mu * alpha(g(x_i))))
        if mu * alpha(g(x_i)) < epsylon:
            return log
        mu = mu * beta
        k = k + 1

#test
if __name__ == "__main__":
    f = lambda x: (x[0]-1)**2 + (x[1]+5)**2
    g = lambda x: (x[0]**2-x[1])
    alpha = lambda gx: max(gx, 0)
    x_1 = [1,-5]
    mu = 100
    epsylon = 0.1
    beta = 2
    log = bounds_method(f, g, alpha, x_1, mu, epsylon, beta)
    for entry in log:
        print(entry)
