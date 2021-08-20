# Autos : Pablo D. Folino
# Ejercitación de señales senoidales, cuadradas y triangulares

from typing import Any
import numpy as np
import matplotlib.pyplot as plt
from numpy.fft.helper import fftshift
import scipy.signal as sc
from scipy.fftpack import fft,fftfreq 
from matplotlib.animation import FuncAnimation
import simpleaudio as sa
import time
import os

#Valores a probar
cantidad=5      # cantidad de veces a reproducir la señal

N   =  128      # Número de muestras 
#N   =  1024      # Número de muestras
#fs  =  44100     # frecuencia de muestreo en Hz
#fs  =  22050     # frecuencia de muestreo en Hz
fs  =  11025     # frecuencia de muestreo en Hz
ts  =  1/fs
tiempo_tx=10    # tiempo en segundos de transmisón
f   =  500      # frecuencia de la señal principal
amp = 0.8       # ampitud de la señal
fase = 0        # fase de la señal en radianes
fsec =  1500     # frecuencia de la señal segundaria
amp2 = 0.05     # ampitud de la señal


faux=0          # Frecuencia de la 2da señal a transformar


# Funciones 

def reproducir(faux):
    global cantidad
    audio = faux.astype(np.int16)             #tranforma la variable note a entero de 16bits y lo guarda en audio
    for i in range(cantidad):
        play_obj = sa.play_buffer(audio, 1, 2, fs)  # sale el audio
        play_obj.wait_done()                        # espera que termine la linea anterior


def valores():
    global N,fs,fsec,amp2,fase,amp
    os.system("clear")
    print("Los valores actuales son:")
    print("La cantidad de muestras es N={}".format(N))
    print("La amplitud de la señal es={}".format(amp))  
    print("La fase de la señal en radianes es={}*Pi radianes".format(fase)) 
    print("La frecuencia de fs={}Hz, y el ts={}seg".format(fs,1/fs)) 
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        valor=input("Ingrese el número de muestras N =")
        if valor.isdigit():
            N=int(valor)
        valor=input("Ingrese la amplitud de la señal entre 0 a 100% =")
        if valor.isdigit():
            amp=float(valor)/100        
        valor=input("Ingrese la fase en grados( enteros) entre 0 a 360 =")
        if valor.isdigit():
            fase=float(valor)*np.pi/180      
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
def  tdf(funcion,N,ts):
    X_fft=fft(funcion)
    #X_fft=rotar(X_fft)
    F_fft=fftfreq(len(funcion),ts)
    #F_fft=rotar(F_fft)
    return  X_fft,F_fft

def graficar(encabezado,funcion,n,X_fft,F_fft):
    fig = plt.figure(1)
    plt.suptitle(encabezado)
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.98, top=0.9, wspace=0.4, hspace=0.8)
    
    s1 = fig.add_subplot(4,1,1)
    plt.title("Señal")
    plt.xlabel("Tiempo(s)")
    plt.ylabel("Amplitud")
    s1.grid(True)
    s1.plot(n,funcion,'ro')
    s1.plot(n,funcion,'b-')
    
    s5 = fig.add_subplot(4,1,2)
    plt.title("Transformada usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("| Amplitud FFT | ")
    s5.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    s5.plot(F_fft,np.abs(X_fft),"g")

    s6 = fig.add_subplot(4,1,3)
    plt.title("Transformada usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Real-Imag. de FFT")
    s6.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    s6.plot(F_fft,np.real(X_fft),"b-")
    s6.plot(F_fft,np.imag(X_fft),"r-")

    s7 = fig.add_subplot(4,1,4)
    plt.title("Angulo usando el módulo scipy")
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Angulos")
    plt.ylim(-185,185)
    s7.grid(True)
    s7.plot(F_fft,np.angle(X_fft)*180/np.pi,'bo-')
    
    plt.get_current_fig_manager().window.showMaximized() #para QT5
    plt.show()

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
    n = np.arange(0, muestras*tiempo_tx, 1/fs)                # Intervalo de tiempo en segundos
    f1=(2**15-1)*amp*np.sin(2*np.pi*f*n+fase)         # Definimos el Vector de Frecuencias
    return f1,n


def fft_senoidal():
    global f,amp
    print("La frecuencia de la señal es de f={}Hz".format(f)) 
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        f=int(input("Ingrese la nueva frecuencia en Hz = "))
    # Definimos una onda  
    f1,n=senoidal(fs,f,amp,N,fase)             
    # Calculo la transformada discreta de Fourier
    X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
    # Se grafica para probar las señales
    encabezado="Senoidal -->"+" frecuencia="+str(f)+"Hz"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
    encabezado+=" Amplitud="+str(amp)+"v"
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        graficar(encabezado,f1,n,X_fft,F_fft)
    consulta=input("Desea transmitir la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        reproducir(f1)

    

def fft_senoidal2():
    global f,fsec,amp,amp2,N,fs,fase,faux

    # Definimos una onda  
    f1,n=senoidal(fs,f,amp,N,fase)
    f2,n=senoidal(fs,fsec,amp2,N,0) 
    f1=f1+f2            
    # Calculo la transformada discreta de Fourier
    X_fft,F_fft=tdf(f1,N,1/fs)              # Transformada Discreta de Fourier-->usando scipy
    # Se grafica para probar las señales
    encabezado="2 señales senoidales-->"+"   f1="+str(f)+"Hz"+"    Amp="+str(amp)+"Hz"+"   N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
    encabezado+="   f2="+str(fsec)+"Hz"+"    Amp="+str(amp2)+"Hz"
    graficar(encabezado,f1,n,X_fft,F_fft)


#================================================================
# Inicio del programa principal
#================================================================
menu="""
Programas de la transformada Discreta de Fourier
elija una opción:

[1] Transformada de una señal senoidal (fs,f,amp,muestras,fase)
[2] Transformada de una señal senoidal (fs,f,amp,f2,amp2,muestras,fase)

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
        pass
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