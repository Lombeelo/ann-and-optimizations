#include <vector>
#include <cmath>
#include <fstream>
#include <format>
#include <string>
#include <array>

using TVector = std::vector<double>;

void add(const TVector& a, const TVector& b, TVector& res)
{
    for (size_t i = 0; i < a.size(); i++)
    {
        res[i] = a[i] + b[i];
    }
}

void mul_scalar(const TVector& a, double b, TVector& res)
{
    for (size_t i = 0; i < a.size(); i++)
    {
        res[i] = a[i] * b;
    }
}

class TDynamicModel
{
public:
    virtual TVector Funcs(float, const TVector&) = 0;
};

class TSpaceCraft : public TDynamicModel
{
public:
    TVector Funcs(float t, const TVector& input)
    {
        double a_mult = -3.98603e14 /
            std::pow(std::sqrt(input[0] * input[0] + input[1] * input[1] + input[2] * input[2]), 3);
        TVector a = { input[0] * a_mult, input[1] * a_mult, input[2] * a_mult };
        return TVector{
            input[3],
            input[4],
            input[5],
            a[0],
            a[1],
            a[2]
        };
    }
};

class TAbstractIntegrator
{
public:
    double t0, h;
    TDynamicModel* RightParts;
    virtual TVector OneStep(int i, const TVector& input) = 0;
};

class TEuler : public TAbstractIntegrator
{
public:
    virtual TVector OneStep(int i, const TVector& input) override
    {
        double ti = t0 + i * h;
        TVector F = RightParts->Funcs(ti, input);
        mul_scalar(F, h, F);
        add(F, input, F);
        return F;
    }
};

class TRungeKutta : public TAbstractIntegrator
{
public:
    virtual TVector OneStep(int i, const TVector& input) override
    {
        double ti = t0 + i * h;
        TVector k1 = RightParts->Funcs(ti, input);
        TVector k2 = k1;
        mul_scalar(k1, h / 2, k2);
        add(k2, input, k2);
        k2 = RightParts->Funcs(ti + h / 2, k2);
        TVector k3 = k2;
        mul_scalar(k2, h / 2, k3);
        add(k3, input, k3);
        k3 = RightParts->Funcs(ti + h / 2, k3);
        TVector k4 = k3;
        mul_scalar(k3, h, k4);
        add(k4, input, k4);
        k4 = RightParts->Funcs(ti + h, k4);

        mul_scalar(k2, 2, k2);
        mul_scalar(k3, 2, k3);
        add(k1, k2, k1);
        add(k1, k3, k1);
        add(k1, k4, k1);
        mul_scalar(k1, h / 6, k1);
        add(k1, input, k1);
        return k1;
    }
};

void calc_csv(const std::string& path, std::array<TAbstractIntegrator*, 2>& integrators, TVector X0, int iterations)
{
    std::ofstream fout(path);
    TVector Xi = X0;
    for (size_t i = 0; i < iterations; i++)
    {
        for (size_t j = 0; j < integrators.size(); j++)
        {
            auto& cur_integr = *integrators[j];
            double ti = cur_integr.t0 + i * cur_integr.h;
            Xi = cur_integr.OneStep(i, Xi);
            if (i % 1000 == 0)
            {
                fout << std::format("{:.3f};{:.3f};{:.3f};{:.3f};", ti, Xi[0], Xi[1], Xi[2]);
            }
        }
        if (i % 1000 == 0)
        {
            fout << "\n";
        }
    }
}


int main(int argc, char* argv[])
{
    TSpaceCraft spaceCraft;
    TVector X0 = { 6878000, 6878000, 6878000, -3000, -100, 3000 };
    TEuler euler;
    TRungeKutta rungie;
    euler.t0 = rungie.t0 = 0;
    euler.RightParts = rungie.RightParts = &spaceCraft;
    euler.h = rungie.h = 0.001;
    std::array<TAbstractIntegrator*, 2> integrators{ &euler, &rungie };
    calc_csv("out_euler.csv", integrators, X0, 7200000);
    return 0;
}