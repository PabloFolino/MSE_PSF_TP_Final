import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sc
import simpleaudio as sa
import os


N=50000             # Cantidad de períodos 
cantidad=2          # Cantidad de veces que se repite la señal
fase    = 0         # Fase de la señal en radianes
amp     = 1.0       # Ampitud de la señal
f       = 50        # Frecencia de la señal
fsec    = 2500      # Frecuencia de batido
amp2    = 0.1
fs      = 44100     # Frecuencia de muestreo en Hz, ver frecuencias soportadas de
                    # la place de sonido


def stop_tx():
        if (sa.PlayObject.is_playing):
            sa.stop_all()


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
    n = np.arange(0, muestras/f, 1/fs)        # Intervalo de tiempo en segundos
    f1=(2**15-1)*amp*np.sin(2*np.pi*f*n+fase)         # Definimos el Vector de Frecuencias
    return f1,n

# Función cuadrada
# Parámetros:
#       fs      --> fecuencia de sampleo
#       f       --> frecuencia de la señal de entrada
#       amp     --> amplitud del señal de 0 a 1.
#       muestras--> cantidad de veces que se repite la señal
# Devuelve:
#       t       --> vector de valores temporales
#       senal   --> vector de valores de la señal  
def cuadrada(fs,f,amp,muestras):
    n = np.arange(0, muestras/f, 1/fs)        # Intervalo de tiempo en segundos
    return (2**15-1)*amp*sc.square(2*np.pi*n*f),n



# Función triangular
# Parámetros:
#       fs      --> fecuencia de sampleo
#       f       --> frecuencia de la señal de entrada
#       amp     --> amplitud del señal de 0 a 1.
#       muestras--> cantidad de veces que se repite la señal
# Devuelve:
#       t       --> vector de valores temporales
#       senal   --> vector de valores de la señal
def triangular(fs,f,amp,muestras):
    n = np.arange(0, muestras/f, 1/fs)        # Intervalo de tiempo en segundos
    return (2**15-1)*sc.sawtooth(2*np.pi*f*n,1),n


def senoidalSuma(fs,f,amp,muestras,fase,B,amp2):
    n = np.arange(0, muestras/f, 1/fs)        # Intervalo de tiempo en segundos
       # Definimos el Vector de Frecuencias
    f1=(2**15-1)*amp*np.sin(2*np.pi*f*n+fase)+(2**15-1)*amp2*np.sin(2*np.pi*B*n)      
    return f1,n

def senoidalB(fs,f,amp,muestras,fase,B):
    n = np.arange(0, muestras/f, 1/fs)        # Intervalo de tiempo en segundos
    f1=(2**15-1)*np.sin(2*np.pi*B/2*n*n)      #sweept
    return f1,n

# Grafica la señal
def graficar(encabezado,funcion,n,xlim):
    global f
    fig = plt.figure(1)
    plt.suptitle(encabezado)
    plt.subplots_adjust(left=0.08, bottom=0.08, right=0.98, top=0.9, wspace=0.4, hspace=0.8)
    
    s1 = fig.add_subplot(1,1,1)
    plt.title("Señal")
    plt.xlabel("Tiempo(s)")
    plt.ylabel("Amplitud")
    plt.xlim(0,xlim)
    s1.grid(True)
    s1.plot(n,funcion*1.65/(2**15-1),'b-')
    plt.show()
    return


def reproducir(note):
    audio = note.astype(np.int16)                   #tranforma la variable note a entero de 16bits y lo guarda en audio
    for i in range(cantidad):
        play_obj = sa.play_buffer(audio, 1, 2, fs)  # sale el audio
       # play_obj.wait_done()                        # espera que termine la linea anterior


def op_senoidal():
    global f,amp,N,fs,fase
    os.system("clear")
    print("==============================")
    print("=======Señal Senoidal=========")
    print("==============================")
    print("La frecuencia de la señal a reproducir es ={}Hz".format(f))
    print("La amplitud de la señal de red \t\tamp={}v-->{}%".format(amp*1.65,amp*100))
    f1,n=senoidal(fs,f,amp,N,fase)
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        encabezado="Senoidal -->"+" f="+str(f)+"Hz"+" T="+str((1/f)*1000)+"mseg"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
        graficar(encabezado,f1,n,2/f)
    consulta=input("Desea reproducir la señal S o N[Enter] :")    
    if consulta=='S' or consulta =='s':
        reproducir(f1)
    return

def op_ruido():
    global fsec,amp2,N,fs
    os.system("clear")
    print("==============================")
    print("=======Señal Senoidal=========")
    print("==============================")
    print("La frecuencia de la señal a reproducir es ={}Hz".format(fsec))
    print("La amplitud de la señal de red \t\tamp2={}v-->{}%".format(amp2*1.65,amp2*100))
    f1,n=senoidal(fs,fsec,amp2,N,0)
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        encabezado="Senoidal -->"+" f="+str(fsec)+"Hz"+" T="+str((1/fsec)*1000)+"mseg"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
        graficar(encabezado,f1,n,2/fsec)
    consulta=input("Desea reproducir la señal S o N[Enter] :")    
    if consulta=='S' or consulta =='s':
        reproducir(f1)
    return

def op_cuadrada():
    global f
    os.system("clear")
    print("==============================")
    print("=======Señal Cuadrada=========")
    print("==============================") 
    print("La frecuencia de la señal a reproducir es ={}Hz".format(f))
    print("La amplitud de la señal de red \t\tamp={}v-->{}%".format(amp*1.65,amp*100)) 
    f1,n=cuadrada(fs,f,amp,N)
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        encabezado="Cuadrada -->"+" f="+str(f)+"Hz"+" T="+str((1/f)*1000)+"mseg"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
        graficar(encabezado,f1,n,2/f)
    consulta=input("Desea reproducir la señal S o N[Enter] :")    
    if consulta=='S' or consulta =='s':
        reproducir(f1)
    return

def op_triangular():
    global f
    os.system("clear")
    print("==============================")
    print("======Señal Triangular========")
    print("==============================") 
    print("La frecuencia de la señal a reproducir es ={}Hz".format(f))
    print("La amplitud de la señal de red \t\tamp={}v-->{}%".format(amp*1.65,amp*100)) 
    f1,n=triangular(fs,f,amp,N)
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        encabezado="Triangular -->"+" f="+str(f)+"Hz"+" T="+str((1/f)*1000)+"mseg"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
        graficar(encabezado,f1,n,2/f)
    consulta=input("Desea reproducir la señal S o N[Enter] :")    
    if consulta=='S' or consulta =='s':
        reproducir(f1)
    return

def op_senoidalB():
    global B
    os.system("clear")
    print("==============================")
    print("=Señal Barrido de Senoidales==")
    print("==============================") 
    print("La frecuencia de la señal a reproducir es ={}Hz".format(f))
    print("La amplitud de la señal de red \t\tamp={}v-->{}%".format(amp*1.65,amp*100)) 
    f1,n=senoidalB(fs,f,amp,N,fase,B)
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        encabezado="Barrido de 2 senoidales-->"+" f="+str(f)+"Hz"+" T="+str((1/f)*1000)+"mseg"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
        graficar(encabezado,f1,n,200/f)
    consulta=input("Desea reproducir la señal S o N[Enter] :")    
    if consulta=='S' or consulta =='s':
        reproducir(f1)
    return


def op_senoidalSuma():
    global f
    os.system("clear")
    print("==============================")
    print("===Señal Suma de Senoidales===")
    print("==============================")   
    print("La frecuencia de la señal a reproducir es ={}Hz".format(f))
    print("La amplitud de la señal es={}".format(amp))  
    f1,n=senoidalSuma(fs,f,amp,N,fase,fsec,amp2)
    consulta=input("Desea graficar la señal S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        encabezado="Suma de 2 senoidales -->"+" f="+str(f)+"Hz"+" T="+str((1/f)*1000)+"mseg"+"  N="+str(N)+"  fs="+str(fs)+"Hz"+"  fase="+str(fase*180/np.pi)+"º"
        graficar(encabezado,f1,n,2/f)
    consulta=input("Desea reproducir la señal S o N[Enter] :")    
    if consulta=='S' or consulta =='s':
        reproducir(f1)
    return

def valores():
    global N,fs,amp,fase,cantidad,fsec,f,amp2
    os.system("clear")
    print("Los valores actuales son:")
    print("----------------------------------------------------------------------") 
    print("La frecuencia de sampling \t\tfs={}Hz --> \tts={:.4f}mseg".format(fs,1/fs*1000)) 
    print("La cantidad de períodos es \t\tN={}".format(N))
    print("La cantidad de veces a repetir es\tN1={}".format(cantidad))
    print("----------------------------------------------------------------------")  
    print("La frecuencia de red \t\t\tfred={} Hz".format(f))
    print("La amplitud de la señal de red \t\tamp={}v-->{}%".format(amp*1.65,amp*100))
    print("La fase de la señal es\t\t\tfase={}*Pi radianes".format(fase))
    print("----------------------------------------------------------------------") 
    print("La frecuencia de ruido es \t\tfr={}Hz".format(fsec))
    print("La amplitud de la señal de ruido \tamp2={}v-->{}%".format(amp2*1.65,amp2*100))
    print("----------------------------------------------------------------------") 
    consulta=input("Desea cambiar los valores S o N[Enter] :")
    if consulta=='S' or consulta =='s':
        valor=input("Ingrese la frecuencia Hz de sampling \t\t\tfs=")
        if valor.isdigit():
            fs=int(valor)
            print("\t\tEl tiempo de sampleo es ts={:.4f}mseg".format(1/fs*1000))
        valor=input("Ingrese la cantidad de períodos a visualzar \t\tN=")
        if valor.isdigit():
            N=int(valor)
        valor=input("Ingrese la cantidad de veces que desea repetir la señal visualizada =")
        if valor.isdigit():
            cantidad=int(valor) 
        valor=input("Ingrese la frecuencia de red en Hz de la señal \t\tfred=")
        if valor.isdigit():
            f=int(valor)
        valor=input("Ingrese la amplitud de la señal de red(0-100)% \t\tamp=")
        if valor.isdigit():
            if(int (valor)>100):
                valor=100
            amp=float(valor)/100  
        valor=input("Ingrese la fase en grados(enteros) entre 0 a 360 \tfase=")
        if valor.isdigit():
            fase=float(valor)*np.pi/180      
        valor=input("Ingrese la frecuencia de ruido en Hz de  \t\tfr=")
        if valor.isdigit():
            fsec=int(valor)
        valor=input("Ingrese la amplitud de la señal de ruido(0-100)%\tamp2=")
        if valor.isdigit():
            if(int (valor)>100):
                valor=100
            amp2=float(valor)/100
        input("Presiona cualquier tecla para continuar")
        os.system("clear")
     

#================================================================
# Inicio del programa principal
#================================================================
menu="""
Programas de la transformada Discreta de Fourier
elija una opción:

[1] Señal de red senoidal 
[2] Señal de ruido senoidal
[3] Señal de red cuadrada 
[4] Señal de red triangular 
[5] Suma de frecuencias senoidales (red+ruido)amp*fred+amp2*fr
[6] Barrido de frecuencias senoidales de fred a fr

[7] Termina Tx de sonido
[8] Seteo de frecuencia de la señal de entrada, número de muestras, 
    frecuencia de sampling.
[9] Salir
"""

while(True):
    os.system("clear")
    print(menu)

    opcion=input("Elija una opción: ")

    if opcion== '1':
        op_senoidal()
    elif opcion== '2':
        op_ruido()
    elif opcion== '3':
        op_cuadrada()   
    elif opcion== '4':
        op_triangular()
    elif opcion== '5':
        op_senoidalSuma()
    elif opcion== '6':
        op_senoidalB()
    elif opcion== '7':
        stop_tx()
    elif opcion== '8':
        valores()
    elif opcion== '9':
        os.system("clear")
        print("Gracias por usar el programa !!!")
        exit (0)
    else:
        print("No selecionó una opción válida\n\r")