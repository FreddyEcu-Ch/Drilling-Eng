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


#%% Design function to calculate S type well parameters

Data_S = namedtuple("Input", "TVD KOP BUR DOR DH")
Output_S = namedtuple(
    "Output", "R1 R2 Theta TVD_EOB Md_EOB Dh_EOB Tan_len Md_SOD TVD_SOD Dh_SOD Md_total"
)


def well_S(data: Data_S, unit="ingles"):
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
    if dh > (R1 + R2):
        fe = dh - (R1 + R2)
    elif dh < (R1 + R2):
        fe = R1 - (dh - R2)
    eo = tvd - kop
    foe = degrees(atan(fe / eo))
    of = sqrt(fe**2 + eo**2)
    fg = R1 + R2
    fog = degrees(asin(fg / of))
    theta = fog - foe
    tvd_eob = kop + R1 * sin(radians(theta))
    if unit == "ingles":
        md_eob = kop + (theta / bur) * 100
    else:
        md_eob = kop + (theta / bur) * 30
    dh_eob = R1 - abs(R1 * cos(radians(theta)))
    tan_len = sqrt(of**2 - fg**2)
    if unit == "ingles":
        md_sod = kop + (theta / bur) * 100 + tan_len
    else:
        md_sod = kop + (theta / bur) * 30 + tan_len
    tvd_sod = tvd_eob + tan_len * abs(cos(radians(theta)))
    dh_sod = dh_eob + abs(tan_len * sin(radians(theta)))
    if unit == "ingles":
        md_total = kop + (theta / bur) * 100 + tan_len + (theta / dor) * 100
    else:
        md_total = kop + (theta / bur) * 30 + tan_len + (theta / dor) * 30

    output_S = Output_S(
        R1=R1,
        R2=R2,
        Theta=theta,
        TVD_EOB=tvd_eob,
        Md_EOB=md_eob,
        Dh_EOB=dh_eob,
        Tan_len=tan_len,
        Md_SOD=md_sod,
        TVD_SOD=tvd_sod,
        Dh_SOD=dh_sod,
        Md_total=md_total,
    )

    names = [
        "R1",
        "R2",
        "theta",
        "tvd_EOB",
        "Md_EOB",
        "Dh_EOB",
        "Lengh_tan",
        "Md_SOD",
        "tvd_SOD",
        "Dh_SOD",
        "Md_Total",
    ]
    for param, value in zip(names, output_S):
        if unit == "ingles":
            if param == "theta":
                print(f"{param} -> {value} degrees")
            else:
                print(f"{param} -> {value} ft")
        else:
            if param == "theta":
                print(f"{param} -> {value} degrees")
            else:
                print(f"{param} -> {value} m")


#%% Data - Example 2
kop = 6084  # ft
tvd = 12000  # ft
bur = 3  # o/100ft
dor = 2  # o/ft
dh = 3500  # ft

#%% Results - Example 2
well_S(Data_S(tvd, kop, bur, dor, dh))

#%% Taller Angel - Pozo Horizontal
Data = namedtuple("Input","DH KOP TVD BUR1 BUR2")
Output = namedtuple("Output", "R1 R2 Theta TVD_eob1 MD_eob1 DH_eob1 MD_sob2 MD_total")

def well_H(data:Data, unit="ingles") -> Output:
    #Call imput values
    tvd = data.TVD
    dh = data.DH
    kop = data.KOP
    bur1 = data.BUR1
    bur2 = data.BUR2
    if unit == "ingles":
        R1 = 5729.58 / bur1
        R2 = 5729.58 / bur2
    else:
        R1 = 1718.87 / bur1
        R2 = 1718.87 / bur2
    #ángulo máximo
    eg = (tvd - kop) - R2
    eo = dh - R1
    goe = degrees(atan(eg/eo))
    og = sqrt(eg**2 + eo**2)
    of = R1-R2
    gof = degrees(acos(of/og))
    theta = 180 - goe - gof
    TVD_eob1 = kop + (R1 + sin(theta))
    if unit == "ingles":
        MD_eob1 = kop + (theta/bur1)*100
    else:
        MD_eob1 = kop + (theta / bur1) * 30
    DH_eob1 = R1 - (R1 * cos(theta))
    bc = sqrt(og**2 - of**2)
    if unit == "ingles":
        MD_sob2 = kop + (theta/bur1)*100 + bc
    else:
        MD_sob2 = kop + (theta / bur1) * 30 + bc
    if unit == "ingles":
        MD_total = kop + (theta/bur1)*100 + bc + ((90-theta)/bur2)*100
    else:
        MD_total = kop + (theta / bur1) * 30 + bc + ((90 - theta) / bur2) * 30

    output_H = Output(
        R1=R1,
        R2=R2,
        Theta=theta,
        TVD_eob1 = TVD_eob1,
        MD_eob1 = MD_eob1,
        DH_eob1 = DH_eob1,
        MD_sob2 = MD_sob2,
        MD_total = MD_total)

    names = ["R1","R2","theta","TVD_EOB1","MD_EOB1","DH_EOB1","MD_SOB2","MD_TOTAL"]
    for param, value in zip(names,output_H):
        if unit == "ingles":
            if param == "theta":
                print(f'{param} -> {value:.3f} degrees')
            else:
                print(f'{param} -> {value:.3f} ft')
        else:
            if param == "theta":
                print(f'{param} -> {value:.3f} degress')
            else:
                print(f'{param} -> {value:.3f} m')

#%% Data exercise Well Horizontal
dh = 1800 #@135° AZM
kop = 2000 #ft
tvd = 3800 #ft
bur1 = 5.73 #/100 ft
bur2 = 9.55 #/100 ft

#%% Test function
well_H(Data(dh,kop,tvd,bur1,bur2))






