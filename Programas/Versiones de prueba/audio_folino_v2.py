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
import serial


#Valores a probar
cantidad=2      # cantidad de veces a reproducir la señal

N   =  128      # Número de muestras de la señal
M   =  129      # Número de muestras del kernel(filtro)
                # Para la CIAA N+M-1 debe dar 2**n
                # Ej: N+M-1=256

#N   =  1024    # Número de muestras
fs  =  44100   # frecuencia de muestreo en Hz
#fs  =  22050   # frecuencia de muestreo en Hz
#fs  =  11025    # frecuencia de muestreo en Hz
ts  =  1/fs
tiempo_tx=30    # tiempo en segundos de transmisón
f   =  50       # frecuencia de la señal principal
amp = 1.0       # ampitud de la señal
fase = 0        # fase de la señal en radianes
fsec =  1500    # frecuencia de la señal segundaria
amp2 = 0.05     # ampitud de la señal


faux=0          # Frecuencia de la 2da señal a transformar

vs_min=0.0
vs_max=0.0
pot_promedio=0.0

delta=300       # frecuencia en Hz para eliminar los 50Hz
                # refuerza el filtro

# Reservo espacio en los vectores
xData=np.zeros(N+M-1)
XData=np.zeros(N+M-1)
HData=np.zeros(N+M-1)
yData=np.zeros(N+M-1)
YData=np.zeros(N+M-1)


STREAM_FILE=("/dev/ttyUSB1","serial")

# Funciones 

def cerrar_puerto():
    
    try:
        streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
        print("\t Se cerró el puerto.")
        streamFile.close()
    except:
        print("\t El puerto estaba cerrado.")
    
    input("Presiona cualquier tecla para continuar")
    os.system("clear")


def pote_promedio(faux_fft):
    potprom=0
    for i in range (len(faux_fft)-1):
        potprom+=faux_fft[i]**2
    return potprom

def  maxinos(faux):
    return np.max(faux),np.min(faux)

def stop_tx():
        if (sa.PlayObject.is_playing):
            sa.stop_all()

def reproducir(faux):
    global cantidad
    faux=faux*(2**15-1)
    stop_tx()
    audio = faux.astype(np.int16)             #tranforma la variable note a entero de 16bits y lo guarda en audio
    for i in range(cantidad):
        play_obj = sa.play_buffer(audio, 1, 2, fs)  # sale el audio
        play_obj.wait_done()                        # espera que termine la linea anterior



def valores():
    global N,fs,fsec,amp2,fase,amp,f,fsec
    os.system("clear")
    print("Los valores actuales son:")
    print("\tLa cantidad de muestras  \tN={}".format(N))
    print("\tLa frecuencia de \t\tfs={}Hz, \ty el ts={}seg".format(fs,1/fs)) 
    print("\tLa frecuencia principal \tf={}Hz".format(f)) 
    print("\tLa amplitud \t\t\tamp={}%".format(amp*100))  
    print("\tLa fase \t\t\tfase={}*Pi radianes".format(fase)) 
    print("\tLa frecuencia del ruido \tfsec={}Hz".format(fsec)) 
    print("\tLa amplitud del ruido es \tamp2={}%".format(amp2*100))
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        valor=input("\tIngrese el número de muestras \t\t\tN =")
        if valor.isdigit():
            N=int(valor)
        valor=input("\tIngrese la frecuencia Hz de sampling \t\tfs=")
        if valor.isdigit():
            fs=int(valor)        
            print("\tEl tiempo de sampleo es \tts={}".format(1/fs))
        valor=input("\tIngrese la frecuencia principal en Hz \t\tf =")
        if valor.isdigit():
            f=int(valor)
        valor=input("\tIngrese la amplitud de la señal entre 0 a 100% \tamp=")
        if valor.isdigit():
            amp=float(valor)/100        
        valor=input("\tIngrese la fase en grados(enteros 0º-360ª) \tfase =")
        if valor.isdigit():
            fase=float(valor)*np.pi/180    
        valor=input("\tIngrese la frecuencia del ruido en Hz \t\tfsec =")
        if valor.isdigit():
            fsec=int(valor)
        valor=input("\tIngrese la amplitud del ruido entre 0 a 100% \tamp2=")
        if valor.isdigit():
            amp2=float(valor)/100   
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
    global amp,vs_max,vs_min,pot_promedio,X_fft_max,X_fft_min,fs
    global xData,XData,HData,yData,YData,fData,circularHData, circularYData,circularXData,circularyData,tData
    global yDataAux

    fig = plt.figure(1)
    plt.suptitle(encabezado)
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.98, top=0.9, wspace=0.4, hspace=0.8)
    plt.rcParams["figure.figsize"] = (17, 4)
    
    s1 = fig.add_subplot(6,2,1)
    s1.clear()
    #plt.title("Señal")
    plt.xlabel("Tiempo(s)")
    plt.ylabel("Amplitud")
    s1.grid(True)
    plt.xlim(0,2/f)
    #uno,=s1.plot(n,funcion,'ro')
    dos,=s1.plot(n,funcion,'b--')
    #plt.legend([uno,dos],["puntos","Señal de entrada"])
    plt.legend([dos],["Señal de entrada"])

    s2 = fig.add_subplot(6,2,2)
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
    plt.text(0,7,"Frec. red="+str(f)+"Hz",fontsize=10)
    #plt.text(5,7,"Amplitud="+str(amp*1.65)+"v",fontsize=10)
    plt.text(5,7,"Ampl. red="+str(f'{amp*1.65:.{4}f}')+"v",fontsize=10)
    plt.text(0,5,"Frec. ruido="+str(fsec)+"Hz",fontsize=10)
    #plt.text(5,5,"Amplitud2="+str(amp2*1.65)+"v",fontsize=10)
    plt.text(5,5,"Ampl. ruido="+str(f'{amp2*1.65:.{4}f}')+"v",fontsize=10)
    #plt.text(0,3,"V Max="+str(vs_max)+"v",fontsize=10)
    plt.text(0,3,"V Max(red+ruido)="+str(f'{vs_max:.{4}f}')+"v",fontsize=10)
    #plt.text(5,3,"V Min="+str(vs_min)+"v",fontsize=10)
    plt.text(5,3,"V Min(red+ruido)="+str(f'{vs_min:.{4}f}')+"v",fontsize=10)
    #plt.text(0,1,"|X_fft_max|="+str(X_fft_max)+"w",fontsize=10)
    plt.text(0,1,"|X[n] máxima| red="+str(f'{X_fft_max:.{4}f}')+"w",fontsize=10)
    #plt.text(5,1,"X_ffft_min="+str(X_fft_min)+"v",fontsize=10)
    #plt.text(0,-1,"Pot prom="+str(pot_promedio)+"w",fontsize=10) 
    plt.text(0,-1,"Pot prom (red+ruido)="+str(f'{pot_promedio:.{4}f}')+"w",fontsize=10)

    s3 = fig.add_subplot(6,2,3)
    s3.clear()
    #plt.title("Transformada usando el módulo scipy")
    plt.text(0.8,0.8,'Transformada usando el', ha='center', va='center', transform=s3.transAxes)
    plt.text(0.8,0.6,'módulo scipy', ha='center', va='center', transform=s3.transAxes)
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("| Amplitud FFT | ")
    s3.grid(True)
    plt.xlim(-fsec-50,fsec+50)
    s3.plot(F_fft,np.abs(X_fft),"g")

    s4 = fig.add_subplot(6,2,4)
    s4.clear()
    plt.text(0.8,0.8,'Transformada usando el', ha='center', va='center', transform=s4.transAxes)
    plt.text(0.8,0.6,'módulo scipy', ha='center', va='center', transform=s4.transAxes)
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Real-Imag. de FFT")
    s4.grid(True)
    plt.xlim(-fsec-50,fsec+50)
    #plt.xlim(-fs/2,fs/2-fs/N)
    s4.plot(F_fft,np.real(X_fft),"b-")
    s4.plot(F_fft,np.imag(X_fft),"r-")

    #============= XData*HData ===================================

    s5 = fig.add_subplot(6,2,5)
    s5.clear()
    #plt.title("|H|")
    plt.text(0.8,0.8,'Filtro usando', ha='center', va='center', transform=s5.transAxes)
    plt.text(0.8,0.6,'pyFDA(PC)', ha='center', va='center', transform=s5.transAxes)
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("|H|")
    s5.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    #plt.xlim(-fs/2,fs/2-fs/N)
    s5.plot(fData,np.abs(circularHData),"b-")

    s6 = fig.add_subplot(6,2,6)
    s6.clear()
    #plt.title("|H|")
    plt.text(0.8,0.8,'Señal + ruido', ha='center', va='center', transform=s6.transAxes)
    plt.text(0.8,0.6,'(PC)', ha='center', va='center', transform=s6.transAxes)
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("|X[n]|")
    s6.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    #plt.xlim(-fs/2,fs/2-fs/N)
    s6.plot(fData,np.abs(circularXData),"b-")

    s7 = fig.add_subplot(6,2,7)
    s7.clear()
    #plt.title("|H|")
    plt.text(0.8,0.8,'(Señal+ruido) filtradas', ha='center', va='center', transform=s7.transAxes)
    plt.text(0.8,0.6,'(PC)', ha='center', va='center', transform=s7.transAxes)
    plt.xlabel("Frecuencia (Hz)")
    plt.ylabel("Y[n]=|X[n]*H[n]|")
    s7.grid(True)
    plt.xlim(-fs/2,fs/2-fs/N)
    #plt.xlim(-fs/2,fs/2-fs/N)
    s7.plot(fData,np.abs(circularYData),"b-") 
    #s7.plot(fData,np.abs(yDataAux),"ro")

    s8 = fig.add_subplot(6,2,8)
    s8.clear()
    #plt.title("|H|")
    plt.text(0.8,0.8,'Ruido con la ifft', ha='center', va='center', transform=s8.transAxes)
    plt.text(0.8,0.6,'(PC)', ha='center', va='center', transform=s8.transAxes)
    plt.xlabel("Tiempo(s)")
    plt.ylabel("y[n]")
    s8.grid(True)
    plt.xlim(0,N/fs)
    s8.plot(tData,circularyData,"b-") 
 
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
    global f,amp,vs_max,vs_min,pot_promedio,X_fft_max,X_fft_min,amp2
    global xData,XData,HData,yData,YData,fData,circularHData,circularYData,circularXData,circularyData,tData
    global yDataAux

    # Definimos una onda  
    f1,n=senoidal(fs,f,amp,N,fase)        

    # Calculo la transformada discreta de Fourier
    X_fft,F_fft,ABS_X_fft=tdf(f1,1/fs)              # Transformada Discreta de Fourier-->usando scipy
    
    # Obtengo el máximo y mínimo de f1 en el dominio del tiempo
    vs_max,vs_min=maxinos(f1)

    # Obtengo el máximo y minimo de f1 en el dominio del tiempo
    X_fft_max,X_fft_min=maxinos(ABS_X_fft)

    # Obtengo la Potencia promedio en el dominio de la frecuencia
    pot_promedio=pote_promedio(ABS_X_fft)

    #============= XData*HData ===================================
    # xData --> vector con valores reales de la señal en el tiempo
    # XData --> vector valores complejos de la señal en frecuencia
    # HData --> vector valores complejos del filtro en frecuencia
    #
    # Se hace YData=XData*HData, y luego la antitranformada
    # para obtener yData
    #
    # Todos los vectores deben tener N+M-1
    #==============================================================



    nData= np.arange(0,N+M-1,1)
    tData=nData/fs
    xData=1.65*amp*np.sin(2*np.pi*f*tData+fase)         # Definimos el Vector de Frecuencias
    fData=nData*(fs/(N+M-1))-fs/2

    firData,=np.load("./Filtro_PSF/N_129_200Hz_5KHz_B_5/BinaryNumpyArray_ba.npy").astype(float)
    firExtendedData=np.concatenate((firData,np.zeros(N-1)))

    XData = np.fft.fft(xData)
    circularXData=np.fft.fftshift(XData)
    HData=np.fft.fft(firExtendedData)
    circularHData=np.fft.fftshift(HData)
    YData=XData*HData
    circularYData=np.fft.fftshift(YData)
    yData=np.real(np.fft.fft(YData))/len(YData)
    #circularyData=np.fft.ifftshift(yData)
    circularyData=(yData)

    #==============================================================

    # Se grafica para probar las señales
    encabezado="Señal de red"
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        graficar(encabezado,f1,n,X_fft,F_fft)
    consulta=input("Desea transmitir la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        reproducir(f1)

    

def fft_senoidal2():
    global f,fsec,amp,amp2,N,fs,fase,vs_max,vs_min,pot_promedio,X_fft_max,X_fft_min
    global xData,XData,HData,yData,YData,fData,circularHData,circularYData,circularXData,circularyData,tData
    global yDataAux

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

 #============= XData*HData ===================================
    # xData --> vector con valores reales de la señal en el tiempo
    # XData --> vector valores complejos de la señal en frecuencia
    # HData --> vector valores complejos del filtro en frecuencia
    #
    # Se hace YData=XData*HData, y luego la antitranformada
    # para obtener yData
    #
    # Todos los vectores deben tener N+M-1
    #==============================================================


    nData= np.arange(0,N+M-1,1)
    tData=nData/fs
    xData=1.65*amp*np.sin(2*np.pi*f*tData+fase)+ 1.65*amp2*np.sin(2*np.pi*fsec*tData)        # Definimos el Vector de Frecuencias
    fData=nData*(fs/(N+M-1))-fs/2

    firData,=np.load("./Filtro_PSF/N_129_200Hz_5KHz_B_5/BinaryNumpyArray_ba.npy").astype(float)
    firExtendedData=np.concatenate((firData,np.zeros(N-1)))

    XData = np.fft.fft(xData)
    circularXData=np.fft.fftshift(XData)
    HData=np.fft.fft(firExtendedData)
    circularHData=np.fft.fftshift(HData)
    YData=XData*HData
    circularYData=np.fft.fftshift(YData)
    yData=np.real(np.fft.fft(YData))/len(YData)
    circularyData=(yData)
  

    #==============================================================
    # Se grafica para probar las señales
    encabezado="Señales de red +ruido"
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        graficar(encabezado,f1,n,X_fft,F_fft)
    consulta=input("Desea transmitir la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        reproducir(f1)


#================================================================
# Inicio del programa principal
#================================================================
menu="""
Programas de la transformada Discreta de Fourier
elija una opción:

[1] Transformada de una señal senoidal (fs,f,amp,muestras,fase)
[2] Transformada de una señal senoidal (fs,f,amp,f2,amp2,muestras,fase)

[3] Para la Tx
[4] Cerrar el Puerto /dev/ttyUSB1
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
        stop_tx()
    elif opcion== '4':
        cerrar_puerto()
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