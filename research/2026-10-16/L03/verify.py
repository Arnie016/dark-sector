"""L-03: deterministic lens-core null verification, all profiles SIMULATED.
No telescope data, dark matter particle model, or physical lens likelihood.
"""
import json
import math
G = 6.67430e-11
C = 299792458.0
M_SUN = 1.98847e30
PC = 3.0856775814913673e16
MAS_PER_RAD = 180 * 3600 * 1000 / math.pi
M0, R0 = 3e5, 10.0

def enclosed(r, kind):
    assert r > 0
    if kind == "point":
        return M0
    if kind == "disk":
        return M0 * min((r/R0)**2, 1.0)
    raise ValueError(kind)

def bend_mas(r, kind):
    return 4 * G * M_SUN * enclosed(r, kind) / (C*C*r*PC) * MAS_PER_RAD

def distance_da_mpc(z=0.881, n=2000):
    assert n%2 == 0
    h = z/n
    acc = 0.
    for i in range(n+1):
        x = i*h
        f = 1/math.sqrt(0.315*(1+x)**3+0.685)
        acc += (1 if i in (0,n) else 4 if i%2 else 2)*f
    return ((C/1000)/67.4)*(acc*h/3)/(1+z)

points = {str(r): {"point_mas":bend_mas(r,"point"),"disk_mas":bend_mas(r,"disk")} for r in (3.,10.,30.)}
checks = {
    "same_enclosed_mass_at_R0": enclosed(R0,"point") == enclosed(R0,"disk"),
    "exact_outside_null": all(bend_mas(r,"point")==bend_mas(r,"disk") for r in (10.,10.1,15.,20.,30.,40.,100.)),
    "inside_mass_fraction": abs(points["3.0"]["disk_mas"]/points["3.0"]["point_mas"] - 0.09)<1e-14,
    "internal_difference": abs(points["3.0"]["point_mas"]-points["3.0"]["disk_mas"])>3.,
    "outside_inverse_R": abs(points["10.0"]["point_mas"]/points["30.0"]["point_mas"]-3.)<1e-12,
    "reference_angle": 1.<points["10.0"]["point_mas"]<1.4,
    "distance_stability": abs(distance_da_mpc(n=2000)-distance_da_mpc(n=1000))<1e-6,
}
assert all(checks.values()), checks
print(json.dumps({"claim":"L-03","kind":"SIMULATED analytic profiles, not measured data","mass_inside_10pc_Msun":M0,"radius_pc":R0,"angles":points,"checks":checks,"checks_passed":len(checks),"seed":None,"angular_R0_mas":R0/(distance_da_mpc()*1e6)*MAS_PER_RAD},indent=2))
