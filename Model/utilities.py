#%% Import Python libraries
from collections import namedtuple
from math import acos, asin, cos, sin, atan, sqrt, radians, degrees

#%% Design function to calculate J-well type parameters

Data = namedtuple("Input", "TVD KOP BUR DH")
Output = namedtuple("Output", "R Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_total")


def well_J(data: Data, unit="ingles") -> Output:
    # Call input values
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dh = data.DH
    if unit == "ingles":
        R = 5729.58 / bur
    else:
        R = 1718.87 / bur
    if dh > R:
        dc = dh - R
    elif dh < R:
        dc = R - dh
    do = tvd - kop
    doc = degrees(atan(dc / do))
    oc = sqrt(dc**2 + do**2)
    boc = degrees(acos(R / oc))
    if R < dh:
        bod = boc - doc
    elif R > dh:
        bod = boc + doc
    theta = 90 - bod
    tvd_eob = kop + abs(R * sin(radians(theta)))
    if unit == "ingles":
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R - R * cos(radians(theta))
    tan_len = sqrt(oc**2 - R**2)
    if unit == "ingles":
        md_total = kop + (theta / bur) * 100 + tan_len
    else:
        md_total = kop + (theta / bur) * 30 + tan_len

    output_J = Output(
        R=R,
        Theta=theta,
        TVD_EOB=tvd_eob,
        Md_EOB=md_eob,
        Dh_EOB=dh_eob,
        Tan_len=tan_len,
        Md_total=md_total,
    )

    names = ["R", "theta", "tvd_EOB", "MD_EOB", "DH_EOB", "Length_tan", "MD_Total"]
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
tvd = 8000  # ft
kop = 500  # ft
bur = 2  # o/100ft
dh = 970.8  # ft

#%% Results - Example 1
well_J(Data(tvd, kop, bur, dh))


#%% Well S - Angel Boza
Data = namedtuple("Input", "TVD KOP BUR DOR DH")
Output = namedtuple("Output", "R1 R2 Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_SOD Tvd_SOD Dh_SOD Md_total")

def well_S(data:Data, unit='ingles') -> Output:
    #Call imput values
    tvd = data.TVD
    kop = data.KOP
    bur = data.BUR
    dor = data.DOR
    dh = data.DH
    if unit == "ingles":
        R1 = 5729.58 / bur
        R2 = 5729.58 / dor
    else:
        R1 = 1718.87 / bur
        R2 = 1718.87 / dor
    if dh > (R1+R2):
        Fe = dh - (R1+R2)
    elif dh < (R1+R2):
        Fe = R1 - (dh - R2)
    eo = tvd - kop
    foe = degrees(atan(Fe/eo))
    of = sqrt(Fe**2 + eo**2)
    fg = R1+R2
    fog = degrees(asin(fg/of))
    theta = fog - foe
    tvd_eob = kop + (R1 * sin(theta))
    if unit=="ingles":
        md_eob = kop + (theta/bur)*100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R1 - (R1 * cos(theta))
    bc = sqrt(of**2 - fg**2)
    if unit == "ingles":
        md_sob = kop + (theta/bur)*100 + bc
    else:
        md_sob = kop + (theta / bur) * 30 + bc
    tvd_sob = tvd_eob + (bc * cos(theta))
    dh_sob = dh_eob + (bc * sin(theta))
    if unit == "ingles":
        md_total = kop + (theta/bur)*100 + bc + (theta/dor)*100
    else:
        md_total = kop + (theta / bur) * 30 + bc + (theta / dor) * 30

    output_S = Output(
        R1=R1,
        R2=R2,
        Theta=theta,
        TVD_EOB=tvd_eob,
        Md_EOB=md_eob,
        Dh_EOB=dh_eob,
        Tan_len=bc,
        Md_SOD=md_sob,
        Tvd_SOD=tvd_sob,
        Dh_SOD=dh_sob,
        Md_total=md_total)

    names = ["R1", "R2", "theta", "tvd_EOB", "MD_EOB", "DH_EOB", "Length_tan", "Md_SOD", "Tvd_SOD", "Dh_SOD", "MD_Total"]
    for param, value in zip(names, output_S):
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

#%% Data Exercise Well S
dh = 3500
kop = 6084
tvd = 12000
bur = 3
dor = 2


#%% Test function
well_S(Data(tvd, kop, bur, dor, dh))