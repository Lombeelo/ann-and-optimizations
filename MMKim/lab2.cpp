#include <vector>
#include <cmath>
#include <fstream>
#include <format>
#include <string>
#include <numbers>

const double mu = 3.98603e14;

const char* tbl_header = "время;координата x;координата y;координата z;"
"скорость x;скорость y;скорость z;"
"фокальный параметр;эксцентриситет;наклонение;долгота восходящего узла; аргумент широты перигея;"
"время прохождения перигея;аргумент широты;истинная аномалия;большая полуось;период обращения;"
"среднее движение; средняя аномалия; радиус-вектор точки"
"\n";

const char* tbl_header_short = "t;x;y;z;vx;vy;vz;p;e;i;Omega;omega;tau;u;nu;a;T;n;M;r;\n";

struct kepler_parameters
{
    double focal_param; // p
    double eccentricity; // e
    double inclination; // i
    double orbital_node; // \Omega
    double periapsis_arg; // \omega
    double periapsis_time; // \tau
    double mean_lat_arg; // u
    double true_anomaly; // \nu
    double semi_major_ax; // a
    double rot_period; // T
    double average_motion; // n
    double avg_anomaly; // M
    double rad_vec_point; // r
};

struct kinematic_parameters
{
    double x, y, z;
    double vx, vy, vz;
};


// u, \Omega, i, \nu, e, p, (r)
kinematic_parameters from_kepler(const kepler_parameters& k)
{
    kinematic_parameters p;
    const double cosu = std::cos(k.mean_lat_arg);
    const double sinu = std::sin(k.mean_lat_arg);
    const double cosOmega = std::cos(k.orbital_node);
    const double sinOmega = std::cos(k.orbital_node);
    const double cosi = std::cos(k.inclination);
    const double sini = std::sin(k.inclination);
    const double sinnu = std::sin(k.true_anomaly);
    const double cosnu = std::cos(k.true_anomaly);

    const double r = k.focal_param / (1 + k.eccentricity * cosnu);
    p.x = r * (cosu * cosOmega - sinu * sinOmega * cosi);
    p.y = r * (cosu * sinOmega - sinu * cosOmega * cosi);
    p.z = r * sinu * sini;
    const double vr = std::sqrt(mu / k.focal_param) * k.eccentricity * sinnu / r;
    const double vn = std::sqrt(mu / k.focal_param) * (1 + k.eccentricity * cosnu);
    p.vx = p.x * vr + vn * (-sinu * cosOmega - cosu * sinOmega * cosi);
    p.vy = p.y * vr + vn * (-sinu * sinOmega + cosu * cosOmega * cosi);
    p.vz = p.z * vr + vn * cosu * sini;
    return p;
}

kepler_parameters to_kepler(const kinematic_parameters& k, const double t)
{
    kepler_parameters out;
    out.rad_vec_point = std::sqrt(k.x * k.x + k.y * k.y + k.z * k.z);
    const double V = std::sqrt(k.vx * k.vx + k.vy * k.vy + k.vz * k.vz);
    const double cx = k.y * k.vz - k.z * k.vy;
    const double cy = k.z * k.vx - k.x * k.vz;
    const double cz = k.x * k.vy - k.y * k.vx;
    const double nu0 = -mu / out.rad_vec_point;
    const double fx = nu0 * k.x + cz * k.vy - cy * k.vz;
    const double fy = nu0 * k.y + cx * k.vz - cz * k.vx;
    const double fz = nu0 * k.z + cy * k.vx - cx * k.vy;

    out.inclination = std::atan2(std::sqrt(cx * cx + cy * cy), cz);
    out.orbital_node = std::atan2(cx, -cy);
    out.focal_param = (cx * cx + cy * cy + cz * cz) / mu;
    out.eccentricity = std::sqrt(fx * fx + fy * fy + fz * fz) / mu;
    out.semi_major_ax = out.focal_param / (1 - out.eccentricity * out.eccentricity);
    const double cosi = std::cos(out.inclination);
    const double cosOmega = std::cos(out.orbital_node);
    const double sinOmega = std::sin(out.orbital_node);

    const double Sw = std::abs(cosi) <= 0e-31 ? fz : (fy * cosOmega - fx * sinOmega) / cosi;
    const double Cw = fx * cosOmega + fy * sinOmega;
    const double Su = std::abs(cosi) <= 0e-31 ? k.vx : (k.y * cosOmega - k.x * sinOmega) / cosi;
    const double Cu = k.x * cosOmega + k.y * sinOmega;
    out.periapsis_arg = std::atan2(Sw, Cw);
    out.mean_lat_arg = std::atan2(Su, Cu);
    out.true_anomaly = out.periapsis_arg - out.mean_lat_arg;
    out.average_motion = std::pow(std::sqrt(2 * mu / out.rad_vec_point - V * V), 3) / mu;
    out.avg_anomaly =
        out.true_anomaly - 2 * out.eccentricity * std::sin(out.true_anomaly)
        + (std::pow(0.75 * out.eccentricity, 2) + 0.125 * std::pow(out.eccentricity, 4) * std::sin(2 * out.true_anomaly))
        - std::pow(out.eccentricity, 3) / 3 * std::sin(3 * out.true_anomaly)
        + 5 / 32 * std::pow(out.eccentricity, 4) * std::sin(4 * out.true_anomaly);

    out.periapsis_time = t - out.avg_anomaly / out.average_motion;
    out.rot_period = 2 * std::numbers::pi / out.average_motion;
    return out;
}


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
        double a_mult = -mu /
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

void calc_csv(const std::string& path, TAbstractIntegrator& integrator, TVector X0, int iterations)
{
    std::ofstream fout(path);
    fout << tbl_header;
    TVector Xi = X0;
    for (size_t i = 0; i < iterations; i++)
    {
        double ti = integrator.t0 + i * integrator.h;
        Xi = integrator.OneStep(i, Xi);
        if (i % 1000 == 0)
        {
            kepler_parameters p = to_kepler(
                kinematic_parameters{ Xi[0],Xi[1],Xi[2],Xi[3],Xi[4],Xi[5] }, ti);
            fout << std::format("{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f};{:.3f}\n",
                ti, Xi[0] / 1000, Xi[1], Xi[2], Xi[3], Xi[4], Xi[5],
                p.focal_param,
                p.eccentricity,
                p.inclination,
                p.orbital_node,
                p.periapsis_arg,
                p.periapsis_time,
                p.mean_lat_arg,
                p.true_anomaly,
                p.semi_major_ax,
                p.rot_period,
                p.average_motion,
                p.avg_anomaly,
                p.rad_vec_point);
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
    calc_csv("out_rungie.csv", rungie, X0, 7200000);
    return 0;
}