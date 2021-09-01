#!python3
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.animation import FuncAnimation
import os
import io
import serial

 
FFT_MAX_DEFAULT=0.1
Vp_MAX=1.65

STREAM_FILE=("/dev/ttyUSB2","serial")
#STREAM_FILE=("log.bin","file")

header = { "pre": b"*header*", "id": 0, "N": 256, "fs": 10000, "cutFrec":0,"cutFrec2":0,"ruido":0,"M":10,"pos":b"end*" }
fig    = plt.figure ( 1 )
fig.suptitle('Ruido en la red de 220v con CIAA', fontsize=16)

#--------------------------ADC---------------------------------------------------------
adcAxe = fig.add_subplot ( 3,1,1 )
adcLn, = plt.plot        ( [],[],'r-o',linewidth=12, alpha = 0.3 ,label  = "adc")
adcAxe.grid              ( True )
adcAxe.set_ylim          ( -Vp_MAX ,Vp_MAX )


#----------------------ciaaFFT vs fft(adc)----------------------------------------------
fftAxe        = fig.add_subplot ( 3,1,2 )
fftAxe.clear()
fftAxe.set_ylim ( 0,FFT_MAX_DEFAULT)      #np.max(absFft))  ---> 0.03
#cutFrecZoneLn   = fftAxe.fill_between([0,0],100,-100,facecolor = "yellow",alpha = 0.2)
fftAxe.set_title("fft(ciaaFFT) vs fft(adc)",rotation = 0,fontsize = 10,va = "center")
fftLn,     = plt.plot ( [] ,[] ,'r-o' ,linewidth = 10  ,alpha = 0.3 ,label = "abs(FFT(adc))" )
ciaaFftLn, = plt.plot ( [] ,[] ,'b-o' ,linewidth = 3 ,alpha = 0.8 ,label = "ciaaFFT filtered out" )
fftLg      = fftAxe.legend()
#fftAxe.text([],[],"Ampl. ruido="+str(f'{fftAbsMax*1.65:.{4}f}')+"v",fontsize=20)


#----------------------------Valores----------------------------------------------------
valoresRx        = fig.add_subplot ( 3,1,3 )
valoresRx.clear()
valoresRx.set_ylim ( 0,10) 
valoresRx.set_xlim ( 0,10) 
plt.axis('off')
valoresRx.spines['right'].set_visible(False)
valoresRx.spines['top'].set_visible(False)
valoresRx.spines['bottom'].set_visible(False)
valoresRx.spines['left'].set_visible(False)
N_Rx=valoresRx.text(0,8,' ',fontsize=10)
M_Rx=valoresRx.text(0,6,' ',fontsize=10)
fs_Rx=valoresRx.text(0,4,' ',fontsize=10)
cutFrec_Rx=valoresRx.text(0,2,' ',fontsize=10)
cutFrec2_Rx=valoresRx.text(0,0,' ',fontsize=10)
ruido_Rx=valoresRx.text(5,8,' ',fontsize=10)
muestras=valoresRx.text(5,6,' ',fontsize=10)
vp_pos_RX=valoresRx.text(5,4,' ',fontsize=10)
vp_neg_RX=valoresRx.text(5,2,' ',fontsize=10)
mod_FFT_Rx=valoresRx.text(5,0,' ',fontsize=10)

def findHeader(f,h):
    data=bytearray(b'12345678')
    while data!=h["pre"]:
        data+=f.read(1)
        if len(data)>len(h["pre"]):
            del data[0]
    h["id"]      = readInt4File(f,4)
    h["N" ]      = readInt4File(f)
    h["fs"]      = readInt4File(f)
    h["cutFrec"] = readInt4File(f)
    h["cutFrec2"] = readInt4File(f)
    h["ruido"]   = readInt4File(f)
    h["M"]       = readInt4File(f)
    data=bytearray(b'1234')
    while data!=h["pos"]:
        data+=f.read(1)
        if len(data)>len(h["pos"]):
            del data[0]
    print({k:round(v,2) if isinstance(v,float) else v for k,v in h.items()})
    return h["id"],h["N"],h["fs"],h["cutFrec"],h["cutFrec2"],h["ruido"],h["M"]

def readInt4File(f,size=2,sign=False):
    raw=f.read(1)
    while( len(raw) < size):
        raw+=f.read(1)
    return (int.from_bytes(raw,"little",signed=sign))

def flushStream(f,h):
    if(STREAM_FILE[1]=="serial"): #pregunto si estoy usando la bibioteca pyserial o un file
        f.flushInput()
    else:
        f.seek ( 2*(h["N"]+h["M"]-1),io.SEEK_END)

def readSamples(adc,synth,N,trigger=False,th=0):
    state="waitLow" if trigger else "sampling"
    i=0
    for t in range(N):
        sample = (readInt4File(streamFile,sign = True)*1.65)/(2**6*512)
        ciaaFFT = (readInt4File(streamFile,sign = True)*1.65)/(2**1*512)
        state,nextI= {
                "waitLow" : lambda sample,i: ("waitHigh",0) if sample<th else ("waitLow" ,0),
                "waitHigh": lambda sample,i: ("sampling",0) if sample>th else ("waitHigh",0),
                "sampling": lambda sample,i: ("sampling",i+1)
                }[state](sample,i)
        adc[i]=sample
        synth[i]=ciaaFFT
        i=nextI

def update(t):
    global header
    flushStream ( streamFile,header )
    id,N,fs,cutFrec,cutFrec2,ruido,M=findHeader ( streamFile,header )
    nData     = np.arange(0,N+M-1,1) #arranco con numeros enteros para evitar errores de float
    adc       = np.zeros(N+M-1)
    ciaaFFT = np.zeros(N+M-1).astype(complex)
    tData     = nData/fs
    
    # Leo los datos recibidos
    readSamples(adc,ciaaFFT,N+M-1,False,0)

    #===================================#=
    # Gráfico en función de la muestras #=
    adcAxe.set_xlim ( 0    ,(N+M-1) )   #=
    adcLn.set_data  ( nData ,adc  )     #=
    #===================================#=

    #==================================================================================================#=
    #                                  Gráfico del abs(FFT(adc)) y  del la señal filtrada              #=
    # if(fftAbsMax<FFT_MAX_DEFAULT):
    #     fftAbsMax=FFT_MAX_DEFAULT
    # fftAxe.set_ylim ( 0, fftAbsMax)                #Escalo al máximo
    
    #fftAxe.clear()

    fftAxe.grid     ( True   )

    fftAxe.set_xlim ( -fs/2,fs/2-fs/(N+M-1))
    fData=nData*fs/(N+M-1)-fs/2
    # Datos del gáfico
    ciaaFftLn.set_data (fData ,np.fft.fftshift(ciaaFFT))
    fftLn.set_data (fData ,np.abs(np.fft.fftshift(np.fft.fft(adc))/(N+M-1))**2)

    #auto escala el eje y, pero no tan bajo
    fftAxe.set_ylim ( 0,np.clip(np.max(ciaaFFT),0.1,300))
    #fftAxe.set_ylim ( 0,np.max(ciaaFFT))
    #fftAxe.set_ylim ( 0,np.max(np.fft.fft(adc)))

    cutFrecZoneLn = fftAxe.fill_between([-cutFrec,-cutFrec2],300,-300,facecolor="yellow",alpha=0.5)
    cutFrecZoneLn = fftAxe.fill_between([cutFrec2,cutFrec],300,-300,facecolor="yellow",alpha=0.5)
    
    
    
    #==================================================================================================#=
    
    #==================================================================================================#=
    #                     Calculo el fft en la PC con los valores recibidos en adc                     #=
    muestras.set_text("Muestras="+str(id)) 
    N_Rx.set_text("Cant de muestras del adc N="+str(N))
    M_Rx.set_text("Cant de muestras del filtro N="+str(M))
    fs_Rx.set_text("fs="+str(fs)+"Hz")
    cutFrec_Rx.set_text("Frec. de corte superior="+str(cutFrec)+"Hz")
    cutFrec2_Rx.set_text("Frec. de corte inferior="+str(cutFrec2)+"Hz")
    ruido_Rx.set_text("Ruido="+str(ruido))
    vp_pos=0
    vp_neg=0
    for i in range(0,len(adc)):
        if(vp_pos<adc[i]):
            vp_pos=adc[i]
        if(vp_neg>adc[i]):
            vp_neg=adc[i]
    vp_pos_RX.set_text("Vp+="+str(f'{vp_pos:.{4}f}')+"v")   
    vp_neg_RX.set_text("Vp-="+str(f'{vp_neg:.{4}f}')+"v")
    mod_FFT_Rx.set_text("|ciaaFFT|max="+str(f'{np.abs(np.max(ciaaFFT)):.{4}f}'))
    #==================================================================================================#=
  
  
    return adcLn, ciaaFftLn, fftLn, cutFrecZoneLn,muestras,N_Rx,M_Rx,fs_Rx,cutFrec_Rx,cutFrec2_Rx,ruido_Rx,vp_pos_RX,vp_neg_RX,mod_FFT_Rx

#seleccionar si usar la biblioteca pyserial o leer desde un archivo log.bin
if(STREAM_FILE[1]=="serial"):
    streamFile = serial.Serial(port=STREAM_FILE[0],baudrate=460800,timeout=None)
else:
    streamFile=open(STREAM_FILE[0],"rb",0)

ani=FuncAnimation(fig,update,10000,init_func=None,blit=True,interval=100,repeat=True)
plt.get_current_fig_manager().window.showMaximized() #para QT5
plt.show()
streamFile.close()
