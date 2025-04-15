import algorithms_correct as algos
import math

def distance(x, y):
    sum = 0
    for i in range(len(x)):
        sum += (x[i] - y[i])**2
    return math.sqrt(sum)

# y = ax; x,y - вектора, a - скаляр
def vec_mult_scalar(scalar, vec):
    return [scalar * i for i in vec]

# z = x + y; x,y,z - вектора
def vector_add(veca, vecb):
    return [a + b for a,b in zip(veca,vecb)]

# z = x + ay
def vector_addmult(veca, scalar, vecb):
    return [a + scalar * b for a,b in zip(veca, vecb)]

def scalar_mult(veca: list, vecb: list) -> float:
    return sum([i * j for i, j in zip(veca, vecb)])

def proj(veca, vecb):
    scalar_ab = scalar_mult(veca, vecb)
    scalar_bb = scalar_mult(vecb, vecb)
    proj_factor = scalar_ab / scalar_bb
    return vec_mult_scalar(proj_factor, vecb)

def neg(vec):
    return [-i for i in vec]

def norm(vec: list) -> float:
    return math.sqrt(scalar_mult(vec, vec))

# пересчёт направлений по процедуре Грама-Шмидта
def gram_shmidt(d_old, lambdas):
    dim = len(d_old)
    q = [vec_mult_scalar(lambdas[j], d_old[j]) if lambdas[j] != 0 else d_old[j] for j in range(dim)]
    pattern_vector = [0] * dim
    for vec in q:
        pattern_vector = vector_add(pattern_vector, vec)
    norm_p = norm(pattern_vector)
    new_basis = []
    # Новая первая ось
    new_basis.append(vec_mult_scalar(1/norm_p, pattern_vector))

    # Остальные оси определяются из старого базиса,
    # проецируя их ортогонально к новому первому вектору
    for i in range(1, dim):
        vi = q[i]
        # Проекция на уже сформированные базисные векторы
        for j in range(i):
            prj = proj(vi, new_basis[j])
            vi = vector_add(vi, neg(prj))
        norm_vi = norm(vi)
        if norm_vi < 1e-12:
            # Если вектор вырожден, выбираем произвольное ортогональное направление
            # Например, можно взять i-ый канонический вектор, ортогонализованный относительно
            vi = [0] * dim
            vi[i] = 1.0
            for j in range(i):
                prj = proj(vi, new_basis[j])
                vi = vector_add(vi, neg(prj))
            norm_vi = norm(vi)
        new_basis.append(vec_mult_scalar(1/norm_vi, vi))
    return new_basis


    # Процедура Грамма-Шмидта для построения направлений (только два измерения)
def GramSchmidt(lyamPrev, dj):
    dim = len(dj)
    bj = [[0]*dim for _ in range(dim)]
    aj = [0]*dim
    lyam = list(lyamPrev)

    dj_copy = list(dj)

    for j in range (dim):
        for s in range(dim):
            if lyam[s] == 0:
                aj[j] = dj[j][s]
            else:
                aj[j] = aj[j]+ lyam[j]*dj[j][s]
    sum = [0]*dim
    l_dj = [0]*dim
    l_bj= [0]*dim

    for j in range(dim):
        l_dj[j] = math.sqrt(math.pow(dj[j][0], 2) + math.pow(dj[j][1], 2));
        for s in range(dim):
            sum[j] = sum[j] + (aj[s] * dj[j][s]) * dj[j][s];
    for j in range(dim):
        for s in range(dim):
            if (j == 0):
                bj[j][s] = aj[s]
            else:
                bj[j][s] = aj[s] - (sum[j - 1] + sum[j]);

    for j in range(dim):
        l_bj[j] = math.sqrt(math.pow(bj[j][0], 2) + math.pow(bj[j][1], 2));

    for j in range(dim):
        for s in range(dim):
            dj_copy[j][s] = bj[j][s] / l_bj[j];
            aj[j] = 0;
            bj[j][s] = 0;
    return dj_copy




# func - функция, которая минимизируется float func(x[dim])
# x_starting - начальная точка оптимизации list[dim]
# epsylon - критерий остановки float
# alpha - коэффициент растяжения float
# beta - коэффициент сжатия float
# delta_starting - начальные значения длин шагов list[dim]
def rosenbrock_discrete(func,
                        x_starting: list,
                        epsylon: float,
                        alpha: float,
                        beta: float,
                        delta_starting: list) -> list:
    calculation_log = []
    # размерность функции (размер массива аргументов)
    dim = len(x_starting)

    # Не смог понять алгоритм пересчёта направлений...
    # так что тактично спиздил :)
    # А он только на 2-мерные функции расчитан
    #if dim != 2: raise NotImplementedError()

    # массив направлений шага
    d = []
    for i in range(dim):
        di = [0] * dim
        di[i] = 1
        d.append(di)

    # берём начальные приближения
    delta = list(delta_starting)
    # начальная точка равна 0
    x = list(x_starting)
    # промежуточная точка внутри итерации
    y = list(x)
    # предыдущая точки среди промежуточных
    y_prev = list(y)
    k = j = 0
    step = "step1"
    while step != "end":
        if step == "step1":
            new_value_arg = vector_addmult(y, delta[j], d[j])
            new_value_try = func(new_value_arg)
            if(new_value_try < func(y)):
                calculation_log.append(dict(
                    k=k, xk=list(x), fxk=func(x),
                    j=j, yj=list(y), fyj=func(y),
                    deltaj=delta[j], dj=list(d[j]),
                    yj_next=list(new_value_arg),
                    fyj_next=new_value_try,
                    success = True))
                #success
                y = list(new_value_arg)
                delta[j] *= alpha
            else:
                calculation_log.append(dict(
                    k=k, xk=list(x), fxk=func(x),
                    j=j, yj=list(y), fyj=func(y),
                    deltaj=delta[j], dj=list(d[j]),
                    yj_next=list(new_value_arg),
                    fyj_next=new_value_try,
                    success = False))
                #failure
                y = list(y)
                delta[j] *= beta

            if j < dim-1:
                j = j + 1
                step = "step1"
            else:
                step = "step2"
        elif step == "step2":
            if func(y) < func(y_prev):
                y_prev = list(y)
                j = 0
                step = "step1"
            elif (func(y) < func(x)): # func(y) == func(y_prev)
                step = "step3"
            else: # func(y) == func(x)
                for i in range(dim):
                    if abs(delta[j]) >= epsylon:
                        y_prev = list(y)
                        j = 0
                        step = "step1"
                        break
                    else: # криво, но пофиг
                        step = "end"
        elif step == "step3":
            if distance(x, y) < epsylon:
               x = list(y)
               step = "end"
               continue

            overall_step = vector_add(y, neg(x))
            lambdas = []
            for j in range(dim):
                projection = proj(overall_step, d[j])
                scalar_prod = scalar_mult(overall_step, d[j])
                lambdas.append(math.copysign(norm(projection), scalar_prod))

            d = gram_shmidt(d, lambdas)
            y_prev = list(y)
            x = list(y)
            delta = list(delta_starting)
            k = k + 1
            j = 0
            step = "step1"
    return calculation_log


def cyclic_coordinate_descend_nolog(f, epsylon, x_1, lam_range):
    y_i = list(x_1)
    x_i = list(x_1)
    dim = len(x_1)
    # массив направлений шага
    d = []
    for i in range(dim):
        di = [0] * dim
        di[i] = 1
        d.append(di)
    k = 1
    while True:
        for j in range(dim):
            optimized_f = lambda lam: f(vector_addmult(y_i, lam, d[j]))
            solution = algos.golden_ratio_correct_solver(lam_range[0], lam_range[1], 0, epsylon, optimized_f)["solution_log"][-1]
            lam_opt = (solution["a"] + solution["b"])/2
            y_i = vector_addmult(y_i, lam_opt, d[j])

        if distance(x_i, y_i) < epsylon:
            return y_i
        else:
            x_i = list(y_i)
        k += 1


#test
if __name__ == "__main__":
    log = rosenbrock_discrete(
        lambda x: x[0]**4 + 2*x[0]**3+(x[1]-4)**2+2*x[2]**2+8*x[2],
        [1, 0, 1], 0.1, 2, -0.5, [0.1, 0.1, 0.1])
    for entry in log:
        print(entry)
