#%% Import Python libraries
from collections import namedtuple
from math import acos, asin, cos, sin, atan, sqrt, radians, degrees

#%% Design function to calculate J-well type parameters

Data = namedtuple("Input", "TVD KOP BUR DOR DH")
Output = namedtuple("Output", "R1 R2 Theta TVD_EOB MD_EOB DH_EOB Tan_Len MD_SOD TVD_SOD DH_SOD MD_TOTAL")


def well_S(data: Data, unit="ingles") -> Output:
    # Call input values
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dor= data.DOR
    dh = data.DH
    if unit == "ingles":
        R_1 = 5729.58 / bur
        R_2= 5729.58 / dor
    else:
        R_1 = 1718.87 / bur
        R_2= 1718.87 / dor

    if dh > R_1+R_2:
        fe = dh - (R_1+R_2)
    elif dh < (R_1+R_2):
        fe = R_1 - (dh-R_2)
    eo = tvd - kop
    foe = degrees(atan(fe / eo))
    of = sqrt(fe**2 + eo**2)
    fg=R_1+R_2
    fog=degrees(asin(fg/of))
    theta=fog-foe
    tvd_eob=kop+(abs(R_1*sin(radians(theta))))

    if unit == "ingles":
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30

    dh_eob = R_1 - R_1 * cos(radians(theta))
    bc = sqrt(of**2 - fg**2)
    if unit == "ingles":
        md_sod = kop + (theta / bur) * 100 + bc
    else:
        md_sod = kop + (theta / bur) * 30 + bc
    tvd_sob=tvd_eob + abs(bc*cos(radians(theta)))
    dh_sob=kop+abs(bc*sin(radians(theta)))
    if unit == "ingles":
        md_total= kop + (theta/bur)*100 + bc + (theta/dor) * 100
    else:
        md_total = kop + (theta / bur) * 30 + bc + (theta / dor) * 30

    output_J = Output(
        R1=R_1,
        R2=R_2,
        Theta=theta,
        TVD_EOB=tvd_eob,
        Md_EOB=md_eob,
        Dh_EOB=dh_eob,
        Tan_len=bc,
        MD_SOD= md_sod,
        TVD_SOD= tvd_sob,
        DH_SOD= dh_sob,
        Md_total=md_total,
    )

    names = ["R1", "R2", "Theta", "TVD_EOB", "MD_EOB", "DH_EOB", "Tan_Len", "MD_SOD", "TVD_SOD", "DH_SOD", "MD_TOTAL"]
    for param, value in zip(names, output_J):
        if unit == "ingles":
            if param == "theta":
                print(f"{param} -> {value:.3f} degrees")
            else:
                print(f"{param} -> {value:.3f} ft")

        else:
            if param == "theta":
                print(f"{param} -> {value:.3f} degrees")
            else:
                print(f"{param} -> {value:.3f} m")


#%% data - Example 1
tvd = 12000  # ft
kop = 6084  # ft
bur = 3  # o/100ft
dor= 2 # o/100ft
dh = 3500  # ft

#%% Results - Example 1
well_S(Data(tvd, kop, bur,dor,dh))
