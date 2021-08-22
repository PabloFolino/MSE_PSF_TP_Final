# Autos : Pablo D. Folino
# Ejercitación de señales senoidales, cuadradas y triangulares

from typing import Any
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft.helper import fftshift
import scipy.signal as sc
from scipy.fftpack import fft,fftfreq 
from matplotlib.animation import FuncAnimation
import mpl_interactions.ipyplot as iplt
import simpleaudio as sa
import time
import os

#Valores a probar
cantidad=2      # cantidad de veces a reproducir la señal

N   =  128      # Número de muestras 
#N   =  1024      # Número de muestras
#fs  =  44100     # frecuencia de muestreo en Hz
#fs  =  22050     # frecuencia de muestreo en Hz
fs  =  11025     # frecuencia de muestreo en Hz
ts  =  1/fs
tiempo_tx=30    # tiempo en segundos de transmisón
f   =  50       # frecuencia de la señal principal
amp = 0.8       # ampitud de la señal
fase = 0        # fase de la señal en radianes
fsec =  1500     # frecuencia de la señal segundaria
amp2 = 0.05     # ampitud de la señal


faux=0          # Frecuencia de la 2da señal a transformar

vs_min=0.0
vs_max=0.0
pot_promedio=0.0


# Funciones 

def pote_promedio(faux_fft):
    potprom=0
    for i in range (len(faux_fft)-1):
        potprom+=faux_fft[i]**2
    return potprom

def  maxinos(faux):
    return np.max(faux),np.min(faux)

def reproducir(faux):
    global cantidad
    faux=faux*(2**15-1)
    audio = faux.astype(np.int16)             #tranforma la variable note a entero de 16bits y lo guarda en audio
    for i in range(cantidad):
        play_obj = sa.play_buffer(audio, 1, 2, fs)  # sale el audio
        play_obj.wait_done()                        # espera que termine la linea anterior


def valores():
    global N,fs,fsec,amp2,fase,amp,f,fsec
    os.system("clear")
    print("Los valores actuales son:")
    print("La cantidad de muestras es N={}".format(N))
    print("La frecuencia de la señal es de f={}Hz".format(f)) 
    print("La amplitud de la señal es={}".format(amp))  
    print("La fase de la señal en radianes es={}*Pi radianes".format(fase)) 
    print("La frecuencia de fs={}Hz, y el ts={}seg".format(fs,1/fs)) 
    print("La frecuencia de la señal secundaria es de fsec={}Hz".format(fsec)) 
    print("La amplitud de la señal secundaria es={}".format(amp2))
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        valor=input("Ingrese el número de muestras N =")
        if valor.isdigit():
            N=int(valor)
        valor=input("Ingrese la nueva frecuencia en Hz f =")
        if valor.isdigit():
            f=int(valor)
        valor=input("Ingrese la amplitud de la señal entre 0 a 100% =")
        if valor.isdigit():
            amp=float(valor)/100        
        valor=input("Ingrese la fase en grados( enteros) entre 0 a 360 =")
        if valor.isdigit():
            fase=float(valor)*np.pi/180    
        valor=input("Ingrese la nueva frecuencia en Hz f2 =")
        if valor.isdigit():
            fsec=int(valor)
        valor=input("Ingrese la amplitud de la señal de f2 entre 0 a 100% =")
        if valor.isdigit():
            amp2=float(valor)/100   
        valor=input("Ingrese la frecuencia Hz de sampling fs =")
        if valor.isdigit():
            fs=int(valor)        
            print("El tiempo de sampleo es ts={}".format(1/fs))
        input("Presiona cualquier tecla para continuar")
        os.system("clear")
     

# Se usa para acomodar el orden de las listas que entrega numpy.fft
def rotar(lista):
    for n1 in range(0,int(len(lista)/2)):
        temp=lista[len(lista)-1]
        for n2 in range(len(lista)-1,0,-1):
            lista[n2]=lista[n2-1]
        lista[0]=temp
    return lista

# Transformada Rápida de Fourier
def  tdf(funcion,ts):
    X_fft=fft(funcion)/len(funcion)
    ABS_X_fft=np.abs(X_fft)
    #X_fft=rotar(X_fft)
    F_fft=fftfreq(len(funcion),ts)
    #F_fft=rotar(F_fft)
    return  X_fft,F_fft,ABS_X_fft

def graficar(encabezado,funcion,n,X_fft,F_fft):
    global amp,vs_max,vs_min,pot_promedio,X_fft_max,X_fft_min

    fig = plt.figure(1)
    plt.suptitle(encabezado)
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.98, top=0.9, wspace=0.4, hspace=0.8)
    plt.rcParams["figure.figsize"] = (17, 4)
    
    s1 = fig.add_subplot(2,2,1)
    s1.clear()
    plt.title("Señal")
    plt.xlabel("Tiempo(s)")
    plt.ylabel("Amplitud")
    s1.grid(True)
    plt.xlim(0,2/f)
    uno,=s1.plot(n,funcion,'ro')
    dos,=s1.plot(n,funcion,'b--')
    plt.legend([uno,dos],["puntos","continuas"])

    s2 = fig.add_subplot(2,2,2)
    s2.clear()
    plt.title("Valores")
    plt.xlim(0,10)
    plt.ylim(0,10)
    plt.axis('off')
    s2.spines['right'].set_visible(False)
    s2.spines['top'].set_visible(False)
    s2.spines['bottom'].set_visible(False)
    s2.spines['left'].set_visible(False)
    plt.text(0,9,"Muestras="+str(N),fontsize=10)
    plt.text(5,9,"FrecSampl.="+str(fs)+"Hz",fontsize=10)
    plt.text(0,7,"Frecuencia="+str(f)+"Hz",fontsize=10)
    plt.text(5,7,"Amplitud="+str(amp*1.65)+"v",fontsize=10)
    plt.text(0,5,"Frecuencia2="+str(fsec)+"Hz",fontsize=10)
    plt.text(5,5,"Amplitud2="+str(amp2*1.65)+"v",fontsize=10)
    plt.text(0,3,"V Max="+str(vs_max)+"v",fontsize=10)
    plt.text(5,3,"V Min="+str(vs_min)+"v",fontsize=10)  
    plt.text(0,1,"|X_fft_max|="+str(X_fft_max)+"w",fontsize=10)
    #plt.text(5,1,"X_ffft_min="+str(X_fft_min)+"v",fontsize=10)
    plt.text(0,-1,"Pot prom="+str(pot_promedio)+"w",fontsize=10)


    s5 = fig.add_subplot(2,2,3)
    s5.clear()
    plt.title("Transformada usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("| Amplitud FFT | ")
    s5.grid(True)
    plt.xlim(-fsec-50,fsec+50)
    s5.plot(F_fft,np.abs(X_fft),"g")

    s6 = fig.add_subplot(2,2,4)
    s6.clear()
    plt.title("Transformada usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Real-Imag. de FFT")
    s6.grid(True)
    plt.xlim(-fsec-50,fsec+50)
    #plt.xlim(-fs/2,fs/2-fs/N)
    s6.plot(F_fft,np.real(X_fft),"b-")
    s6.plot(F_fft,np.imag(X_fft),"r-")

 
    plt.get_current_fig_manager().window.showMaximized() #para QT5
    #plt.show()
    plt.ion()
    return

# Función senoidal
# Parámetros:
#       fs      --> fecuencia de sampleo
#       f       --> frecuencia de la señal de entrada
#       amp     --> amplitud del señal de 0 a 1.
#       muestras--> cantidad de veces que se repite la señal
#       fase    --> fase de la señal en radianes
# Devuelve:
#       f1      --> vector de señal de la señal 
#       n       --> vector de tienpos de sampling 
def senoidal(fs,f,amp,muestras,fase):
    n = np.arange(0, tiempo_tx, 1/fs)            # Intervalo de tiempo en segundos
    f1=1.65*amp*np.sin(2*np.pi*f*n+fase)         # Definimos el Vector de Frecuencias
    return f1,n


def fft_senoidal():
    global f,amp,vs_max,vs_min,pot_promedio,X_fft_max,X_fft_min

    # Definimos una onda  
    f1,n=senoidal(fs,f,amp,N,fase)        

    # Calculo la transformada discreta de Fourier
    X_fft,F_fft,ABS_X_fft=tdf(f1,1/fs)              # Transformada Discreta de Fourier-->usando scipy
    
    # Obtengo el màximo y mìnimo de f1 en el dominio del tiempo
    vs_max,vs_min=maxinos(f1)

    # Obtengo el máximo y minimo de f1 en el dominio del tiempo
    X_fft_max,X_fft_min=maxinos(ABS_X_fft)

    # Obtengo la Potencia promedio en el dominio de la frecuencia
    pot_promedio=pote_promedio(ABS_X_fft)

    # Se grafica para probar las señales
    encabezado="Senoidal"
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        graficar(encabezado,f1,n,X_fft,F_fft)
    consulta=input("Desea transmitir la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        reproducir(f1)

    

def fft_senoidal2():
    global f,fsec,amp,amp2,N,fs,fase,vs_max,vs_min,pot_promedio,X_fft_max,X_fft_min

    # Definimos una onda  
    f1,n=senoidal(fs,f,amp,N,fase)
    f2,n=senoidal(fs,fsec,amp2,N,0) 
    f1=f1+f2            

    # Calculo la transformada discreta de Fourier
    X_fft,F_fft,ABS_X_fft=tdf(f1,1/fs)              # Transformada Discreta de Fourier-->usando scipy
    
    # Obtengo el màximo y mìnimo de f1 en el dominio del tiempo
    vs_max,vs_min=maxinos(f1)

    # Obtengo el máximo y minimo de f1 en el dominio del tiempo
    X_fft_max,X_fft_min=maxinos(ABS_X_fft)

    # Obtengo la Potencia promedio en el dominio de la frecuencia
    pot_promedio=pote_promedio(ABS_X_fft)


    # Se grafica para probar las señales
    encabezado="2 señales senoidales"
    graficar(encabezado,f1,n,X_fft,F_fft)


#================================================================
# Inicio del programa principal
#================================================================
menu="""
Programas de la transformada Discreta de Fourier
elija una opción:

[1] Transformada de una señal senoidal (fs,f,amp,muestras,fase)
[2] Transformada de una señal senoidal (fs,f,amp,f2,amp2,muestras,fase)

[5] Valores default:
                 N=8, fase=0, fs=8Hz
                 f1=1Hz amp=1.0 --> 1,65v f2=10Hz amp2=0.5
[6] Valores default:
                 N=128, fase=0, fs=44100Hz
                 f1=50Hz amp=0.8 f2=560Hz amp2=0.05
[7] Valores 
                 N=128, fase=0, fs=100Hz
                 f1=50Hz amp=0.8 f2=560Hz amp2=0.05
[8] Seteo de frecuencia de la señal de entrada, número de muestras, frecuencia 
de sampling
[9] Salir
"""

while(True):

    # Limpio las listas en donde se guarda la Fransformada de Fourier

    os.system("clear")
    print(menu)

    opcion=input("Elija una opción: ")

    if opcion== '1':
        fft_senoidal()
    elif opcion== '2':
        fft_senoidal2()
    elif opcion== '3':
        pass
    elif opcion== '4':
        pass
    elif opcion== '5':
        N   =  8            # Número de muestras 
        fs  =  8            # frecuencia de muestreo en Hz
        ts  =  1/fs
        f   =  1            # frecuencia de la señal a realizar la transformada
        amp = 1.0           # ampitud de la señal
        fase = 0            # fase de la señal en radianes
        fsec   =  10        # frecuencia de la señal a realizar la transformada
        amp2 = 0.5          # ampitud de la señal
    elif opcion== '6':
        N   =  128          # Número de muestras 
        fs  =  44100        # frecuencia de muestreo en Hz
        ts  =  1/fs
        f   =  50           # frecuencia de la señal a realizar la transformada
        amp = 0.8           # ampitud de la señal
        fase = 0            # fase de la señal en radianes
        fsec   =  560         # frecuencia de la señal a realizar la transformada
        amp2 = 0.05         # ampitud de la señal

    elif opcion== '7':
        N   =  128          # Número de muestras 
        fs  =  100          # frecuencia de muestreo en Hz
        ts  =  1/fs
        f   =  50           # frecuencia de la señal a realizar la transformada
        amp = 0.8           # ampitud de la señal
        fase = 0            # fase de la señal en radianes
        fsec   =  560         # frecuencia de la señal a realizar la transformada
        amp2 = 0.05         # ampitud de la señal
    elif opcion== '8':
        valores()
    elif opcion== '9':
        os.system("clear")
        print("Gracias por usar el programa !!!")
        exit (0)
    else:
        print("No selecionó una opción válida\n\r")