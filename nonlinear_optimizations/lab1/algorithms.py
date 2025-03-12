
max_steps = 100

def calc_counter(solver_result):
    counter = 0
    for step in solver_result["solution_log"]:
        if step["f_lam_calculated"] == True:
            counter += 1
        if step["f_mu_calculated"] == True:
            counter += 1
    return counter



def dichotomy_solver(a, b, epsylon, l, func):  #a,b - границы интервала, epylon - шаг от центра, l - минимальный интервал, func - функция
    
    solver_result = { 
        "solution_log": [],
        "a_end": 0,
        "b_end": 0,
        "f_a_end": 0,
        "f_b_end": 0,
        "f_calculated_counter": 0
        }
    k = 1
    middle = 0
    lam = 0
    mu = 0
    f_lam = 0
    f_mu = 0
    current_step = "step1"
    while current_step != "end":
        if current_step == "step1":
            print("test1")
            if (b - a) < l:
                print("end")
                current_step = "end"
            else:
                middle = (a + b)/2
                lam = middle - epsylon
                mu = middle + epsylon
                current_step = "step2"
        elif current_step == "step2":
            print("test2")
            f_lam = func(lam)  
            f_mu = func(mu)
   
            solver_result["solution_log"].append(
                dict(solver_type = "Дихотомический поиск", k = k, a = a, b = b, lam = lam, mu = mu, f_lam = f_lam, f_lam_calculated = True,
                      f_mu = f_mu, f_mu_calculated = True, epsylon = epsylon))

            if f_lam < f_mu:
                a = a
                b = mu
            else:
                a = lam
                b = b
            k = k+1  
            if k > max_steps: 
                print("end1")
                current_step = "end"
            else:
                print(f'step{k}') #было step11
                current_step = "step1"

    solver_result["a_end"] = a
    solver_result["b_end"] = b
    solver_result["f_opt"] = func((solver_result["a_end"]+solver_result["b_end"])/2)
    solver_result["f_calculated_counter"] = calc_counter(solver_result)

    return solver_result


def golden_ratio_solver(a, b, epsylon, l, func):
    solver_result = { 
        "solution_log": [],
        "a_end": 0,
        "b_end": 0,
        "f_a_end": 0,
        "f_b_end": 0,
        "f_calculated_counter": 0
        }
    k = 1
    lam = 0
    mu = 0
    f_lam = 0
    f_mu = 0
    phi = .6180339887498948482
    phi_inv = 1 - phi

    lam = a + phi_inv*(b - a)
    mu = a + phi*(b - a)
    f_lam = func(lam)
    f_mu = func(mu)

    mu_calc = True
    lam_calc = True

    solver_result["solution_log"].append(
                dict(solver_type = "Золотое сечение", k = k, a = a, b = b, lam = lam, mu = mu,
                      f_lam = f_lam, f_lam_calculated = lam_calc,
                      f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))
    current_step = "step1"
    while current_step != "end":
        if current_step == "step1":
            if (b - a) < l:
                current_step = "end"
            else:
                if f_lam > f_mu:
                    current_step = "step2"
                else:
                    current_step = "step3"
        elif current_step == "step2":
            a = lam
            b = b
            lam = mu
            f_lam = f_mu
            mu = a + phi*(b - a)
            f_mu = func(mu)
            mu_calc = True
            lam_calc = False
            current_step = "step4"
        elif current_step == "step3":
            a = a
            b = mu
            mu = lam
            f_mu = f_lam
            lam = a + phi_inv*(b - a)
            f_lam = func(lam)
            mu_calc = False
            lam_calc = True  
            current_step = "step4"
        elif current_step == "step4":
            k = k+1
            if k > max_steps:
                current_step = "end"

            solver_result["solution_log"].append(
                dict(solver_type = "Золотое сечение", k = k, a = a, b = b, lam = lam, mu = mu,
                      f_lam = f_lam, f_lam_calculated = lam_calc,
                      f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))
            
            current_step = "step1"

    solver_result["a_end"] = a
    solver_result["b_end"] = b
    solver_result["f_opt"] = func((solver_result["a_end"]+solver_result["b_end"])/2)
    solver_result["f_calculated_counter"] = calc_counter(solver_result)


    return solver_result


def fibonacchi_solver(a, b, epsylon, l, func):
    fib_max = (b - a)/l
    F = [1,1]
    while F[len(F)-1] < fib_max:
        F.append(F[len(F)-1] + F[len(F)-2])
    n = len(F) - 1
    solver_result = { 
        "solution_log": [],
        "a_end": 0,
        "b_end": 0,
        "f_a_end": 0,
        "f_b_end": 0,
        "f_calculated_counter": 0
        }
    k = 1
    lam = a + F[n-k-1]/F[n-k+1]*(b - a)
    mu = a + F[n-k]/F[n-k+1]*(b - a)
    f_lam = func(lam)
    f_mu = func(mu)

    mu_calc = True
    lam_calc = True

    solver_result["solution_log"].append(
        dict(solver_type = "Метод Фибоначчи", k = k, a = a, b = b, lam = lam, mu = mu,
                f_lam = f_lam, f_lam_calculated = lam_calc,
                f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))

    current_step = "step1"
    while current_step != "end":
        if current_step == "step1":
            if f_lam > f_mu:
                current_step = "step2"
            else:
                current_step = "step3"
        elif current_step == "step2":
            a = lam
            b = b
            lam = mu
            f_lam = f_mu
            mu = a + F[n-k]/F[n-k+1]*(b - a)
            if (k == n-2):
                current_step = "step5"    
            else:
                f_mu = func(mu)
                mu_calc = True
                lam_calc = False
                current_step = "step4"
        elif current_step == "step3":
            a = a
            b = mu
            mu = lam
            f_mu = f_lam
            lam = a + F[n-k-1]/F[n-k+1]*(b - a)
            if (k == n-2):
                current_step = "step5"    
            else:
                f_lam = func(lam)
                mu_calc = False
                lam_calc = True  
                current_step = "step4"

        elif current_step == "step4":
            k = k+1
            if k > max_steps:
                current_step = "end"

            solver_result["solution_log"].append(
                dict(solver_type = "Метод Фибоначчи", k = k, a = a, b = b, lam = lam, mu = mu,
                        f_lam = f_lam, f_lam_calculated = lam_calc,
                        f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))
            
            current_step = "step1"

        elif current_step == "step5":
            lam = lam
            mu = lam + epsylon

            f_lam = func(lam)        
            f_mu = func(mu)
            mu_calc = True
            lam_calc = True
            if f_lam > f_mu:
                a = a
                b = mu
            else:
                a = lam
                b = b
            k = k+1
            solver_result["solution_log"].append(
                dict(solver_type = "Метод Фибоначчи", k = k, a = a, b = b, lam = lam, mu = mu,
                        f_lam = f_lam, f_lam_calculated = lam_calc,
                        f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))
            current_step = "end"
    
    solver_result["a_end"] = a
    solver_result["b_end"] = b
    solver_result["f_opt"] = func((solver_result["a_end"]+solver_result["b_end"])/2)
    solver_result["f_calculated_counter"] = calc_counter(solver_result)


    return solver_result



