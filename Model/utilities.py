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

#%%
Data = namedtuple("Input", "TVD KOP BUR DOR DH")
Output = namedtuple("Output", "R1, R2, Theta, TVD_EOB, MD_EOB, DH_EOB, Tan_Len, MD_SOD, TVD_SOD, DH_SOD, MD_TOTAL")


def pozotipoS(data: Data, unit="ingles") -> Output:
    # Call input values
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
    EG = (tvd - kop) - R2
    EO = dh - R1
    GOE = degrees(atan(EG / EO))
    OG = sqrt(EG**2 + EO**2)
    OF = R1 - R2
    GOF = degrees(acos(OF / OG))
    theta = 180 - GOE - GOF
    tvd_eob = kop + abs(R1 * sin(radians(theta)))
    if unit == "ingles":
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30

    dh_eob = R1 - R1 * cos(radians(theta))
    tan_len = sqrt(OG ** 2 - OF ** 2)

    if unit == "ingles":
        md_sod = kop + (theta / bur) * 100 + tan_len
    else:
        md_sod = kop + (theta / bur) * 30 + tan_len
    tvd_sod = tvd_eob + abs(tan_len * cos(radians(theta)))
    dh_sod = dh + abs(tan_len * sin(radians(theta)))
    CGD = 90 - theta
    if unit == "ingles":
        md_total = kop + (theta / bur) * 100 + tan_len + (CGD / dor) * 100
    else:
        md_total = kop + (theta / bur) * 30 + + tan_len + (CGD / dor) * 30
    output_J = Output(
        R1=R1,
        R2=R2,
        Theta=theta,
        TVD_EOB=tvd_eob,
        TVD_SOD=tvd_sod,
        Md_EOB=md_eob,
        Md_SOD=md_sod,
        Dh_EOB=dh_eob,
        DH_SOD=dh_sod,
        Tan_len=tan_len,
        Md_total=md_total)

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