import math
import os
import sys

def welcome():

    print(
        '''
\033[94m 
╔═╗┬ ┬┌─┐┌─┐┌┬┐  ╔═╗┌─┐┌┬┐┬┌─┐┬ ┬┬─┐┌─┐
╚═╗├─┤├─┤├┤  │   ╠╣ ├─┤ │ ││ ┬│ │├┬┘├┤ 
╚═╝┴ ┴┴ ┴└   ┴   ╚  ┴ ┴ ┴ ┴└─┘└─┘┴└─└─┘
╔═╗┌┐┌┌─┐┬ ┬ ┬┌─┐┌─┐┬─┐                
╠═╣│││├─┤│ └┬┘┌─┘├┤ ├┬┘                
╩ ╩┘└┘┴ ┴┴─┘┴ └─┘└─┘┴└─  
\033[92m
\nJohn Dennis - 2021 - Auburn University
\nValues from Shigley's \"Mechanical Engineering Design 11th Edition\"
\033[95m              
        '''
    )


def getMatProps(param):

    if param == 1:
        sut_mpa = int(input("Enter the Ultimate Tensile Strength in MPa: "))
        sy_mpa = int(input("Enter the Yield Strength in MPa: "))

        mat_prop = [sut_mpa, sy_mpa]

    elif param == 2:
        sut_kpsi = int(input("Enter the Ultimate Tensile Strength in kPsi: "))
        sy_kpsi = int(input("Enter the Yield Strength in kPsi: "))

        mat_prop = [sut_kpsi, sy_kpsi]

    return mat_prop

def getStressType():

    type = int(input("Is the stress Axial[1], Bending[2], or Torsion[3]?: "))

    return type

def getUnits():

    units = int(input("Are the units in MPa[1] or kPsi[2]?: "))

    return units

def getLoading(param):
    
    if param == 1:
        unit = "MPa"
    elif param == 2:
        unit = "kPsi"
    else:
        unit = ""

    load = float(input("Enter the stress that the part undergoes in {}: ".format(unit)))

    return load

def getSePrime(sut, unit):

    if unit == 1:
        if sut <= 1400:
            return sut * 0.5
        elif sut > 1400:
            return 700
    elif unit == 2:
        if sut <= 200:
            return sut * 0.5
        elif sut > 200:
            return 100

def getSe(se_prime, k_values):

    k_fact = 1
    for i in range(0, len(k_values)):

        k_fact *= k_values[i]

    se = se_prime * k_fact

    return se

def getSurfaceType():

    print("What is the surface type?")
    surf = int(input("Ground[1], Machined or Cold-Drawn[2], Hot Rolled[3], Forged[4]?: "))

    return surf

def getSurfFac(units, surf, sut):

    ka = 1

    if units == 1:
        if surf == 1:
            ka = 1.58 * (sut ** -0.085)
        elif surf == 2:
            ka = 4.51 * (sut ** -0.265)
        elif surf == 3:
            ka = 57.5 * (sut ** -0.718)
        elif surf == 4:
            ka = 272.0 * (sut ** -0.995)
    elif units == 1:
        if surf == 1:
            ka = 1.34 * (sut ** -0.085)
        elif surf == 2:
            ka = 2.70 * (sut ** -0.265)
        elif surf == 3:
            ka = 14.4 * (sut ** -0.718)
        elif surf == 4:
            ka = 39.9 * (sut ** -0.995)

    return ka

def getPartSize(units):

    if units == 1:
        option = "Millimeters"
    elif units == 2:
        option = "Inches"
    else:
        option = "Millimeters"

    diameter = float(input("Enter diameter of part in {}: ".format(option)))

    return diameter

def getSizeFac(units, loading,  size):

    if loading != 1:
        if units == 1:
            if size >= 2.79 and size <= 51:
                return 1.24 * (size ** -0.107)
            elif size > 51 and size < 254:
                return 1.51 * (size ** -0.157)
            else:
                return 1
        elif units == 2:
            if size >= 0.11 and size <= 2:
                return 0.879 * (size ** -0.107)
            elif size > 2 and size <= 10:
                return 0.91 * (size ** -0.157)
            else:
                return 1
        else:
            return 1
    elif loading == 1:
        return 1
    else: 
        return 1

def getLoadFac(loading):

    if loading == 1:
        return 1
    elif loading == 2:
        return 2
    elif loading == 3:
        return 0.59
    else:
        return 1

def getTemp():

    corf = int(input("Is Temp in C[1] or F[2]?: "))
    temp = float(input("What is the Temperature?: "))
    if corf == 2:
        return temp
    elif corf == 1:
        return (temp * 9 / 5) + 32
    else:
        return temp

def getTempFac(temp):

    a = 0.975
    b = (0.432 * 10 ** -3 * temp)
    c = (0.115 * 10 ** -5 * temp ** 2)
    d = (0.104 * 10 ** -8 * temp ** 3)
    e = (0.595 * 10 ** -12 * temp ** 4)
    tot = a + b - c + d - e

    return tot

def getRel():

    rel = float(input("Enter the Reliability (%): "))

    return rel

def getRelFac(rel):

    if rel == 50:
        return 1
    elif rel == 90:
        return 0.897
    elif rel == 95:
        return 0.868
    elif rel == 99:
        return 0.814
    elif rel == 99.9:
        return 0.753
    elif rel == 99.99:
        return 0.702
    elif rel == 99.999:
        return 0.659
    elif rel == 99.9999:
        return 0.620
    else:
        return 1

def getNotchGeometry(units):

    if units == 1:
        option = "Millimeters"
    if units == 2:
        option = "Inches"
    else:
        option = "Millimeters"

    small_dia = float(input("Enter value for d in {}: ".format(option)))
    large_dia = float(input("Enter value for D in {}: ".format(option)))
    radius = float(input("Enter the size of radius in {}: ".format(option)))

    ratioD2d = large_dia / small_dia
    ratior2d = radius / small_dia

    return [ratioD2d, ratior2d]

def getNotchType():

    type = int(input("Is notch a U-Notch[1] or a Shoulder Fillet[2]: "))

    return type

def getStressConcFac(D_d, r_d, D, d, r, stressType, notchType):

    range = (D - d) / r

    if notchType == 1:
        if stressType = 1:
            if range >= 0.25 and range <= 2.0:
                c1 = 0.4550 + 3.3540 * math.sqrt(range) - 0.7690 * range
                c2 = 3.1290 - 15.955 * math.sqrt(range) + 7.4040 * range
                c3 = -6.909 + 29.286 * math.sqrt(range) - 16.104 * range
                c4 = 4.3250 - 16.685 * math.sqrt(range) + 9.4690 * range
            elif range >= 2.0 and range <= 50.0:
                c1 =  0.935 + 1.922 * math.sqrt(range) + 0.004 * range
                c2 =  0.537 - 3.708 * math.sqrt(range) + 0.040 * range
                c3 = -2.538 + 3.438 * math.sqrt(range) - 0.012 * range
                c4 =  2.066 - 1.652 * math.sqrt(range) - 0.031 * range
            else:
                return 0
        elif stressType = 2:
            if range >= 0.25 and range <= 2.0:
                c1 = a + b * math.sqrt(range) - c * range
                c2 = a - b * math.sqrt(range) + c * range
                c3 = a + b * math.sqrt(range) - c * range
                c4 = a - b * math.sqrt(range) + c * range
            elif range >= 2.0 and range <= 50.0:
                c1 = a +- b * math.sqrt(range) +- c * range
                c2 = a +- b * math.sqrt(range) +- c * range
                c3 = a +- b * math.sqrt(range) +- c * range
                c4 = a +- b * math.sqrt(range) +- c * range
            else:
                return 0
        else:
            if range >= 0.25 and range <= 2.0:
                c1 = a +- b * math.sqrt(range) +- c * range
                c2 = a +- b * math.sqrt(range) +- c * range
                c3 = a +- b * math.sqrt(range) +- c * range
                c4 = a +- b * math.sqrt(range) +- c * range
            elif range >= 2.0 and range <= 50.0:
                c1 = a +- b * math.sqrt(range) +- c * range
                c2 = a +- b * math.sqrt(range) +- c * range
                c3 = a +- b * math.sqrt(range) +- c * range
                c4 = a +- b * math.sqrt(range) +- c * range
            else:
                return 0
    elif notchType == 2:
        if stressType = 1:
            if range >= 0.25 and range <= 2.0:
                c1 = a +- b * math.sqrt(range) +- c * range
                c2 = a +- b * math.sqrt(range) +- c * range
                c3 = a +- b * math.sqrt(range) +- c * range
                c4 = a +- b * math.sqrt(range) +- c * range
            elif range >= 2.0 and range <= 20.0:
                c1 = a +- b * math.sqrt(range) +- c * range
                c2 = a +- b * math.sqrt(range) +- c * range
                c3 = a +- b * math.sqrt(range) +- c * range
                c4 = a +- b * math.sqrt(range) +- c * range
            else:
                return 0
        elif stressType = 2:
            if range >= 0.25 and range <= 2.0:
                c1 = a +- b * math.sqrt(range) +- c * range
                c2 = a +- b * math.sqrt(range) +- c * range
                c3 = a +- b * math.sqrt(range) +- c * range
                c4 = a +- b * math.sqrt(range) +- c * range
            elif range >= 2.0 and range <= 20.0:
                c1 = a +- b * math.sqrt(range) +- c * range
                c2 = a +- b * math.sqrt(range) +- c * range
                c3 = a +- b * math.sqrt(range) +- c * range
                c4 = a +- b * math.sqrt(range) +- c * range
            else:
                return 0
        else:
            if range >= 0.25 and range <= 4.0:
                c1 = a +- b * math.sqrt(range) +- c * range
                c2 = a +- b * math.sqrt(range) +- c * range
                c3 = a +- b * math.sqrt(range) +- c * range
                c4 = a +- b * math.sqrt(range) +- c * range
            else:
                return 0
            
    else:
        return 0

    

def getNotchSens(units, load_type, sut):

    if units == 1:
        option = "Millimeters"
        sut = 0.145038 * sut
    elif units == 2:
        option = "Inches"
    else:
        option = "Millimeters"

    r = float(input("Enter the radius of notch in {}: ".format(option)))

    if load_type == 1 or load_type == 2:

        a = 0.246 - (3.08 * (10**-3) * sut) + (1.51 * (10 ** -5) * (sut**2)) - (2.67 * (10 ** -8) * (sut**3))

        q = 1 / (1+ (a / math.sqrt(r)))

        kt = float(input("Enter Kt value: "))

        return 1 + (q * (kt - 1))

    elif load_type == 3:

        a = 0.190 - (2.51 * (10**-3) * sut) + (1.35 * (10 ** -5) * (sut**2)) - (2.67 * (10 ** -8) * (sut**3))

        qs = 1 / (1+ (a / math.sqrt(r)))

        kts = float(input("Enter Kts value: "))

        return 1 + (qs * (kts - 1))

    else:
        return 1


def getF(units, sut, sprime):

    if units == 1:
        sig_pri_f = sut + 345
    elif units == 2:
        sig_pri_f = sut + 50
    else:
        sig_pri_f = sut + 345

    b = (-math.log10(sig_pri_f / sprime) ) / (math.log10(2 * 10 ** 6))

    f = (sig_pri_f / sut) * ( 2000 ** b)

    return f

def getA(f, sut, se):

    return ((f * sut) ** 2) / se

def getB(f, sut, se):

    return (-1/3) * (math.log10(f * sut / se))

def getServiceLife(sigma, a, b):

    return (sigma / a) ** (1 / b)

def main():
    
    welcome()

    units = getUnits()
    type = getStressType()
    if units > 0:
        props = getMatProps(units)
        sut = props[0]
        sy = props[1]
        loading = getLoading(units)
        surf = getSurfaceType()
        size  = getPartSize(units)
        temp = getTemp()
        rel = getRel()

    se_prime = getSePrime(sut, units)
    surf_fac = getSurfFac(units, surf, sut)
    size_fac = getSizeFac(units, type, size)
    load_fac = getLoadFac(type)
    temp_fac = getTempFac(temp)
    rel_fac = getRelFac(rel)

    k = [surf_fac, size_fac, load_fac, temp_fac, rel_fac]

    se = getSe(se_prime, k)
    notch = getNotchSens(units, type, sut)

    sigma_max = notch * loading

    f = getF(units, sut, se_prime)
    
    a = getA(f, sut, se)
    
    b = getB(f, sut, se)
    service_life = math.floor(getServiceLife(sigma_max, a, b))

    print("Service life is {} cycles!".format(service_life))

if __name__ == "__main__":
    main()
