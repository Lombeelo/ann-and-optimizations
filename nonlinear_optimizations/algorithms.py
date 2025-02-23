
max_steps = 100

def dichotomy_solver(a, b, epsylon, l, func):
    solver_result = { 
        "solution_log": [],
        "a_end": 0,
        "b_end": 0
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
                middle = (a + b )/2
                lam = middle - epsylon
                mu = middle + epsylon
                current_step = "step2"
        elif current_step == "step2":
            print("test2")
            f_lam = func(lam)
            f_mu = func(mu)
   
            solver_result["solution_log"].append(
                dict(k = k, a = a, b = b, lam = lam, mu = mu, f_lam = f_lam, f_lam_calculated = True,
                      f_mu = f_mu, f_mu_calculated = True))

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
                print("step11")
                current_step = "step1"
    solver_result["a_end"] = a
    solver_result["b_end"] = b
    return solver_result


def golden_ratio_solver(a, b, epsylon, l, func):
    solver_result = { 
        "solution_log": [],
        "a_end": 0,
        "b_end": 0
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
                      f_mu = f_mu, f_mu_calculated = mu_calc))
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
                dict(k = k, a = a, b = b, lam = lam, mu = mu,
                      f_lam = f_lam, f_lam_calculated = lam_calc,
                      f_mu = f_mu, f_mu_calculated = mu_calc))
            
            current_step = "step1"

    solver_result["a_end"] = a
    solver_result["b_end"] = b
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
        "b_end": 0
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
                f_mu = f_mu, f_mu_calculated = mu_calc))

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
                dict(k = k, a = a, b = b, lam = lam, mu = mu,
                        f_lam = f_lam, f_lam_calculated = lam_calc,
                        f_mu = f_mu, f_mu_calculated = mu_calc))
            
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
                dict(k = k, a = a, b = b, lam = lam, mu = mu,
                        f_lam = f_lam, f_lam_calculated = lam_calc,
                        f_mu = f_mu, f_mu_calculated = mu_calc))
            current_step = "end"
    
    solver_result["a_end"] = a
    solver_result["b_end"] = b
    return solver_result


solvers = [dichotomy_solver, golden_ratio_solver, fibonacchi_solver]
for solver in solvers:
    solution = solver(-3, 5, 0.09, 0.2, lambda x: x*x - 2*x)
    for step in solution["solution_log"]:
        print(step)
        