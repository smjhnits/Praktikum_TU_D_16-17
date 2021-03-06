import numpy as np
from scipy.stats import sem
from uncertainties import ufloat
import uncertainties.unumpy as unp
import matplotlib.pyplot as plt
import scipy.constants as sc
from scipy.optimize import curve_fit
#from pint import UnitRegistry
import operator


#u = UnitRegistry()
#Q_ = u.Quantity

Time_ges = 81591 #Bsp lambda_r = Q_(643.2, 'nanometer')
C_Start = 1444133
C_Stop = 4255

print("Gesamter Messzeitraum: ", Time_ges)
print("Gemessene Startimpulse: ", C_Start)
print("Gemessene Stopimpulse: ", C_Stop, '\n')
Time_Search = 10 *10**(-6)

C_Start_r = ufloat(C_Start, np.sqrt(C_Start))

Rate = C_Start_r/Time_ges
N_Search = Time_Search*Rate

W = N_Search * unp.exp(N_Search)
U_Search = W*C_Start/512

print("Rate pro Sekunde: ", Rate)
print("Wahrscheinlichkeit: ", W)
print("Untergrund nach Poisson: ", U_Search, '\n')


#Datenaufnahme etwas umständlich
Counts_M = np.genfromtxt('Messung.txt', unpack=True)
Channels = np.linspace(0, 511, 512)


Messung_Errors = np.sqrt(Counts_M)
Messung = unp.uarray(Counts_M, Messung_Errors)

#Kalibrierung_Errors = np.sqrt(Counts_K)
#Kalibrierung_Werte = np.array([ufloat(n, Kalibrierung_Errors[i]) for i,n in enumerate(Counts_K) ])
#Kalibrierung_y = np.array([Kalibrierung_Werte[i] for i,n in enumerate(Counts_K) if n!= 0])

Counts_K = np.genfromtxt('Kalibrierung.txt', unpack=True)
Kalibrierung_x = np.array([Channels[i] for i,n in enumerate(Counts_K) if n!= 0])
K_x = Kalibrierung_x
Kalibrierung_y = np.array([0.3,1,2,3,4,5,6,7,8,9,10])
Channels_real = np.array([K_x[0],K_x[2],K_x[3],K_x[4],K_x[6],K_x[7],K_x[8],K_x[9],K_x[10],K_x[12],K_x[13]])




Plateau_x = np.array([-24,-22,-20,-18,-16,-14,-12,-10,-8,-6,-4,-2,-1,0,1,2,4,6,8,10,12,14,16,18,20])

P1 = unp.uarray([154,186,186,173], np.sqrt([154,186,186,173]))
P2 = unp.uarray([176,189,164,172], np.sqrt([176,189,164,172]))
P4 = unp.uarray([183,167,178,194], np.sqrt([183,167,178,194]))
P6 = unp.uarray([178,193,165,180], np.sqrt([178,193,165,180]))
P8 = unp.uarray([186,168,147,168], np.sqrt([186,168,147,168]))

M0  = unp.uarray([167,184,180], np.sqrt([167,184,180]))
M1  = unp.uarray([177,189,178], np.sqrt([177,189,178]))
M2  = unp.uarray([169,180,171,171], np.sqrt([169,180,171,171]))
M4  = unp.uarray([177,168,183,158], np.sqrt([177,168,183,158]))
M6  = unp.uarray([167,164,179,153], np.sqrt([167,164,179,153]))
M8  = unp.uarray([176,144,151,135], np.sqrt([176,144,151,135]))
M10 = unp.uarray([123, 134], np.sqrt([123, 134]))

Plateau = unp.uarray([6,2,12,10,37,54,86,unp.nominal_values(M10.mean()),unp.nominal_values(M8.mean()),
unp.nominal_values(M6.mean()),unp.nominal_values(M4.mean()),unp.nominal_values(M2.mean()),
unp.nominal_values(M1.mean()),unp.nominal_values(M0.mean()),unp.nominal_values(P1.mean()),
unp.nominal_values(P2.mean()),unp.nominal_values(P4.mean()),unp.nominal_values(P6.mean()),
unp.nominal_values(P8.mean()),140,120,63,40,0,0] , [np.sqrt(6),np.sqrt(2),
np.sqrt(12),np.sqrt(10),np.sqrt(37),np.sqrt(54),np.sqrt(86),unp.std_devs(M10.mean()),
unp.std_devs(M8.mean()),unp.std_devs(M6.mean()),unp.std_devs(M4.mean()),unp.std_devs(M2.mean()),
unp.std_devs(M1.mean()),unp.std_devs(M0.mean()),unp.std_devs(P1.mean()),unp.std_devs(P2.mean()),
unp.std_devs(P4.mean()),unp.std_devs(P6.mean()),unp.std_devs(P8.mean()),np.sqrt(140),
np.sqrt(120),np.sqrt(63),np.sqrt(40),np.sqrt(0),np.sqrt(0)])

#print("Plateau: ", Plateau, '\n')

# nächste Abschnitt für das Plateau

fit_x = np.linspace(-25,25,1000)#Plateau_x[9],Plateau_x[18],100)

def PlateauFit(x, b):
    return 0*x+b

def Flankenfit(x, A, b):
    return A*x + b

LinksParams, LinksCovariance = curve_fit(Flankenfit, Plateau_x[3:10], unp.nominal_values(Plateau[3:10]))
RechtsParams, RechtsCovariance = curve_fit(Flankenfit, Plateau_x[19:24], unp.nominal_values(Plateau[19:24]))
Links_errors = np.sqrt(np.diag(LinksCovariance))
Rechts_errors = np.sqrt(np.diag(RechtsCovariance))

fitParams, fitCovariance = curve_fit(PlateauFit, Plateau_x[9:19], unp.nominal_values(Plateau[9:19]), sigma = unp.std_devs(Plateau[9:19]), absolute_sigma = True )
Plateau_errors = np.sqrt(np.diag(fitCovariance))
Höhe = ufloat(fitParams[0], Plateau_errors[0])


A_L = ufloat(LinksParams[0], Links_errors[0])
A_R = ufloat(RechtsParams[0], Rechts_errors[0])
B_L = ufloat(LinksParams[1], Links_errors[1])
B_R = ufloat(RechtsParams[1], Rechts_errors[1])

x_L = (Höhe/2-B_L)/A_L
x_R = (Höhe/2-B_R)/A_R

print("zeiten: ", x_L, x_R, '\n')
print("Links: ", Plateau_x[3:10], A_L, B_L, '\n')
print("rechts: ", Plateau_x[19:24], A_R, B_R, '\n')


plt.errorbar(Plateau_x, unp.nominal_values(Plateau), xerr= 0, yerr = unp.std_devs(Plateau), fmt = 'kx', label = r'Messwerte')
plt.plot(fit_x, PlateauFit(fit_x, *fitParams), 'r-', label = r'linearer Fit')
plt.axvline(unp.nominal_values(x_L), color = 'r', linestyle = '--', label = r'$T_{\mathrm{VZ,links}}$')
plt.axvline(unp.nominal_values(x_R), color = 'r', linestyle = '--', label = r'$T_{\mathrm{VZ,rechts}}$')
plt.ylabel(r'N(t)')
plt.xlabel(r'$T_{\mathrm{VZ}}$ in $\mathrm{ns}$')
plt.legend(loc = 'best')
plt.savefig('Plateau.pdf')
#plt.show()

print("Bestimmte Höhe des Plateaus: ", Höhe, '\n')

# Kalibrierung

def Kalibrierung(x, A, B):
    return A*x + B

KParams, KCovariance = curve_fit(Kalibrierung, Channels_real, Kalibrierung_y)
K_errors = np.sqrt(np.diag(KCovariance))
Steigung = ufloat(KParams[0], K_errors[0])
Abschnitt = ufloat(KParams[1], K_errors[1])
print("Abschnitt der Gerade: ", Abschnitt, '\n')
print("Steigung der Gerade: ", Steigung, '\n')

plt.clf()
plt.plot(Channels_real, Kalibrierung_y, 'kx', label = r'Messwerte')
plt.plot(Channels, Kalibrierung(Channels, *KParams), 'r-', label = r'linearer Fit')
plt.ylabel(r'$t$ in $\mathrm{\mu s}$')
plt.xlabel(r'Kanal')
plt.legend(loc = 'best')
#plt.savefig('Kalibrierung.pdf')
#plt.show()


# Auswertung der Zeiten

def Lebensdauer(x, N0, LB, U):
    return N0 * np.exp(-LB*x) + U

Zeiten = Kalibrierung(Channels, *KParams)


Zeiten_neu = np.linspace(0,0,512)
Counts_neu = np.linspace(0,0,512)


Zählstruktur = np.linspace(0,255,256)
Counts_neu_1 = np.array([Counts_M[2*i]+Counts_M[2*i+1] for i,n in enumerate(Zählstruktur)])
Zeiten_neu_1 = np.array([(Zeiten[2*i]+Zeiten[2*i+1])/2 for i,n in enumerate(Zählstruktur)])

for i,n in enumerate(Counts_neu_1):
    if n == 0:
        print("Index von 0:", i)

Counts_r = np.array([n for n in Counts_M])
Zeiten_r = np.array([n for n in Zeiten])

#print(Counts_M)

Counts_M[0] = 1
Counts_M[1] = 1
Counts_M[2] = 1

for i,n in enumerate(Counts_M):
    #print("Schlaufe", i, Counts_M[i-1:i+2])
    k = i
    #print(i)
    if Counts_M[i]!=0:
        Counts_neu[i] = Counts_M[i]
        Zeiten_neu[i] = Zeiten[i]
        #print(i,n,"--------------")
    elif Counts_M[i]==0:
        if Counts_M[i-1]!=0 and Counts_M[i+1]!=0:
            #print(i,0)
            Zeiten_neu[i-1] = (Zeiten[i]+Zeiten[i-1])/2
            Counts_neu[i] = Counts_M[i+1]
            Zeiten_neu[i] = Zeiten[i+1]
            #print("nächster", Counts_M[k+1])
            while k < 510:
                Counts_M[k] = Counts_M[k+1]
                Zeiten[k] = Zeiten[k+1]
                k=k+1
            #print(Counts_M[i:i+10])
        elif Counts_M[i-1]!=0 and Counts_M[i+1]==0 and Counts_M[i+2]!=0:
            #print(i, 00)
            Zeiten_neu[i-1] = (Zeiten[i]+Zeiten[i-1])/2
            Counts_neu[i] = Counts_M[i+2]
            Zeiten_neu[i] = (Zeiten[i+1]+Zeiten[i+2])/2
            while k <= 509:
                Counts_M[k] = Counts_M[k+2]
                Zeiten[k] = Zeiten[k+2]
                k=k+1
        elif Counts_M[i-1]==0:
            #print(i, i-1, i+1, "Abbruch")
            break
        else:
            #print(i,Counts_M[i-3:i+2], "Abbruch")
            break

for i,n in enumerate(Counts_neu):
    if n == 0:
        print("Fehler", i)
        break
#print(Counts_neu[0:378])

Counts_M = Counts_r
Zeiten = Zeiten_r

Counts_neu[0] = 0
Counts_neu[1] = 0
Counts_neu[2] = 0


#Counts_fusch = np.array([n for n in Counts_neu if n != 0]) # mach aus Counts_M Counts_neu
#Zeiten_fusch = np.array([Zeiten_neu[i] for i,n in enumerate(Counts_neu) if n != 0]) # mach aus Counts_M Counts_neu und Zeiten
#Errors_fusch = np.sqrt(Counts_fusch)

Counts_fusch = Counts_neu_1[1:184]
Zeiten_fusch = Zeiten_neu_1[1:184]
Errors_fusch = np.sqrt(Counts_fusch)

LD_Params, LD_Covariance = curve_fit(Lebensdauer, Zeiten_fusch, Counts_fusch,  sigma = Errors_fusch, absolute_sigma = True)
LD_Errors = np.sqrt(np.diag(LD_Covariance))

N0 = ufloat(LD_Params[0], LD_Errors[0])
LB = ufloat(LD_Params[1], LD_Errors[1])
LD = 1 /LB
U_fit = ufloat(LD_Params[2], LD_Errors[2])

print("Wert für N0: ", N0)
print("Zerfallskonstante: ", LB)
print("Lebensdauer: ", LD)
print("Untergrund durch Fit: ", U_fit, '\n')

Zeiten_x = np.linspace(-2, 12, 1000)

plt.clf()
plt.errorbar(Zeiten_fusch, Counts_fusch, xerr = 0, yerr = Errors_fusch, fmt = 'kx', label = r'Messwerte')
plt.plot(Zeiten_x, Lebensdauer(Zeiten_x, *LD_Params), 'r-', label = r'Exponentieller Fit')
plt.xlim(-0.5,11.5)
#plt.ylim(-2, 65)
plt.axvline(0, color = 'b', linestyle = '-', label = r'$t=0$')
plt.ylabel(r'N(t)')
plt.yscale('log')
plt.xlabel(r'$t$ in $\mathrm{ns}$')
plt.legend(loc = 'best')
plt.savefig('Spektrum_klein_log.pdf')
plt.show()

print("Verhältnisse Untergrund:", U_Search/U_fit)

LD_Lit = 2.20

print("Verhältniss Lebensdaier:", LD/LD_Lit)
