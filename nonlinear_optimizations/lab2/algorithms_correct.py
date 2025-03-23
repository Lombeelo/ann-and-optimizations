max_steps = 100

# Данная версия отличается тем, что написана по современным лекалам
def dichotomy_correct_solver(a, b, epsylon, l, func):
    solver_result = { 
        "solution_log": [],
        "a_end": 0,
        "b_end": 0,
        "calc_counter": 0
        }
    k = 1
    middle = 0
    lam = 0
    mu = 0
    f_lam = 0
    f_mu = 0

    while b-a >= l:
        middle = (a+b) / 2
        lam = middle - epsylon
        mu = middle + epsylon
        f_lam = func(lam)  
        f_mu = func(mu)
        solver_result["solution_log"].append(
                dict(k = k, a = a, b = b, lam = lam, mu = mu, f_lam = f_lam, f_lam_calculated = True,
                      f_mu = f_mu, f_mu_calculated = True, epsylon = epsylon))
        solver_result["calc_counter"] += 2
        if f_lam < f_mu:
            a = a
            b = mu
        else:
            a = lam
            b = b
        k = k+1  #мб надо обновлять значение раньше?
        if k > max_steps: 
            break
    
    solver_result["a_end"] = a
    solver_result["b_end"] = b
    return solver_result


def golden_ratio_correct_solver(a, b, epsylon, l, func):
    solver_result = { 
        "solution_log": [],
        "a_end": 0,
        "b_end": 0,
        "calc_counter": 0
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
                dict(k = k, a = a, b = b, lam = lam, mu = mu,
                      f_lam = f_lam, f_lam_calculated = lam_calc,
                      f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))
    solver_result["calc_counter"] += mu_calc + lam_calc
    
    while (b-a) >= l:
        if f_lam > f_mu:
            a = lam
            b = b
            lam = mu
            f_lam = f_mu
            mu = a + phi*(b - a)
            f_mu = func(mu)
            mu_calc = True
            lam_calc = False
        else:
            a = a
            b = mu
            mu = lam
            f_mu = f_lam
            lam = a + phi_inv*(b - a)
            f_lam = func(lam)
            mu_calc = False
            lam_calc = True  
        
        k = k+1
        if k > max_steps:
            break

        solver_result["solution_log"].append(
            dict(k = k, a = a, b = b, lam = lam, mu = mu,
                    f_lam = f_lam, f_lam_calculated = lam_calc,
                    f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))
        solver_result["calc_counter"] += mu_calc + lam_calc

    return solver_result



def fibonacchi_correct_solver(a, b, epsylon, l, func):
    fib_max = (b - a)/l
    F = [1,1]
    while F[len(F)-1] < fib_max:
        F.append(F[len(F)-1] + F[len(F)-2])
    n = len(F) - 1
    solver_result = { 
        "solution_log": [],
        "a_end": 0,
        "b_end": 0,
        "calc_counter": 0
        }
    k = 1
    lam = a + F[n-k-1]/F[n-k+1]*(b - a)
    mu = a + F[n-k]/F[n-k+1]*(b - a)
    f_lam = func(lam)
    f_mu = func(mu)

    mu_calc = True
    lam_calc = True

    solver_result["solution_log"].append(
        dict(k = k, a = a, b = b, lam = lam, mu = mu,
                f_lam = f_lam, f_lam_calculated = lam_calc,
                f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))
    solver_result["calc_counter"] += mu_calc + lam_calc
    
    while True:
        if f_lam > f_mu:
            a = lam
            b = b
            lam = mu
            f_lam = f_mu
            mu = a + F[n-k]/F[n-k+1]*(b - a)
            if (k == n-2):
                break
            else:
                f_mu = func(mu)
                mu_calc = True
                lam_calc = False
        else:
            a = a
            b = mu
            mu = lam
            f_mu = f_lam
            lam = a + F[n-k-1]/F[n-k+1]*(b - a)
            if (k == n-2):
                break 
            else:
                f_lam = func(lam)
                mu_calc = False
                lam_calc = True  
        
        k = k+1
        if k > max_steps:
            solver_result["a_end"] = a
            solver_result["b_end"] = b
            return solver_result

        solver_result["solution_log"].append(
            dict(k = k, a = a, b = b, lam = lam, mu = mu,
                    f_lam = f_lam, f_lam_calculated = lam_calc,
                    f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))
        solver_result["calc_counter"] += mu_calc + lam_calc
    
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
        dict(k = k, a = a, b = b, lam = lam, mu = mu,
                f_lam = f_lam, f_lam_calculated = lam_calc,
                f_mu = f_mu, f_mu_calculated = mu_calc, epsylon = epsylon))
    solver_result["calc_counter"] += mu_calc + lam_calc
    
    solver_result["a_end"] = a
    solver_result["b_end"] = b
    return solver_result
