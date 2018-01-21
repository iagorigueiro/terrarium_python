#!/usr/bin/python3
# -*- coding: utf-8 -*-
import Adafruit_DHT #importaciones
import RPi.GPIO as GPIO
import time
import os
import glob
from datetime import datetime
#import commands


"""CONFIGURACION CALENDARIO"""

#enero,febrero,marzo
meses_invierno=[1,2,3];dias_invierno=[[20,12],[21,12],[22,12],[23,12],[24,12],[25,12],[26,12],[27,12],[28,12],[29,12],[30,12],[31,12]]
temp_invierno_dia_sala=25;
temp_invierno_noche_sala=22;temp_invierno_dia_calor=30;
temp_invierno_noche_calor=24.5
humedad_invierno_dia=90
humedad_invierno_noche=85
luz_invierno=[10,11,12,13,14,15,16,17,18,19]#TENER EN CUENTA HORA MARZO
#julio,agosto,septiembre
meses_verano=[7,8,9];temp_verano_dia_sala=28;
temp_verano_noche_sala=25;temp_verano_dia_calor=31;
temp_verano_noche_calor=26;luz_verano=[9,10,11,12,13,14,15,16,17,18,19,20];
dias_verano=[[21,6],[22,6],[23,6],[24,6],[25,6],[26,6],[27,6],[28,6],[29,6],[30,6]]
#abril
abril=4;luz_abril=[10,11,12,13,14,15,16,17,18,19]#de 9:30 a 20:30
temp_abril_dia_calor=30.5
temp_abril_noche_calor=25
temp_abril_dia_sala=26
temp_abril_noche_sala=23
#mayo
mayo=5;luz_mayo=[9,10,11,12,13,14,15,16,17,18,19]# hasta las 20:30
temp_mayo_dia_calor=30.5
temp_mayo_noche_calor=25.5
temp_mayo_dia_sala=27
temp_mayo_noche_sala=24
#junio
junio=6;luz_junio=luz_verano
#octubre
octubre=10;luz_octubre=[9,10,11,12,13,14,15,16,17,18,19]#hasta las 20:30
temp_octubre_dia_calor=30.5
temp_octubre_noche_calor=25.5
temp_octubre_dia_sala=27
temp_octubre_noche_sala=24
humedad_octubre_dia=75
humedad_octubre_noche=70
#noviembre
noviembre=11;luz_noviembre=[10,11,12,13,14,15,16,17,18,19]#de 9:30 a 20:30
temp_noviembre_dia_calor=30.5
temp_noviembre_noche_calor=25
temp_noviembre_dia_sala=26
temp_noviembre_noche_sala=23
humedad_noviembre_dia=80
humedad_noviembre_noche=75
#diciembre
diciembre=12;luz_diciembre=luz_invierno;


"""CONFIGURACION SENSORES"""
sensor = Adafruit_DHT.DHT22#configuraciones primarias
pin_higrometro = 17
pin_rele_1= 21
pin_rele_2= 20
pin_rele_3= 16
pin_rele_4= 12
i=0
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_rele_1,GPIO.OUT)
GPIO.output(pin_rele_1,GPIO.HIGH)#el rele en principio no esta como se enchufa
GPIO.setup(pin_rele_2,GPIO.OUT)
GPIO.output(pin_rele_2,GPIO.HIGH)
GPIO.setup(pin_rele_3,GPIO.OUT)
GPIO.output(pin_rele_3,GPIO.HIGH)
GPIO.setup(pin_rele_4,GPIO.OUT)
GPIO.output(pin_rele_4,GPIO.HIGH)
GPIO.setwarnings(False)
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

"""FUNCIONES DE LOS SENSORES Y LEDS"""
def higrometro():#devuelve la temperatura y la humedad del higrometro
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_higrometro)
    if humidity is not None and temperature is not None:
        return temperature, humidity
    else:
        return None,None
        	
def read_temp_raw(): #prepara el archivo de la sonda
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
	
def read_temp(): #devuelve la temperatura de la sonda
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c
    
def imprimir_valores(mes,tempR1,humR1,tempR2,tempD1,humD1,tempD2):
    
#imprimir_valores('octubre',temperaturah,humedadh,temperatura_sonda,temp_octubre_dia_calor,humedad_octubre_dia,temp_octubre_dia_sala)
    print('                                                                %s'%(mes))
    print('Dia y hora:                                 '+str(ahora.day) +' del '+str(ahora.month)+'       '+str(ahora.hour)+':'+str(ahora.minute)+'.'+str(ahora.second))
    
    if tempR1==None:
        print('Problema con el punto de calor :(')
        print('Temperatura de la sala=                     {0:0.2f}*C          {1:0.2f}*C'.format(tempR2,tempD2))
    
    else:
        print('Temperatura del punto de calor=             {0:0.2f}*C         {1:0.2f}*C'.format(tempR1,tempD1))
        print('Humedad del terrario=                       {0:0.2f}%          {1:0.2f}%'.format(humR1,humD1))
        print('Temperatura de la sala=                     {0:0.2f}*C         {1:0.2f}*C'.format(tempR2,tempD2))
        print
        print
        print
    
    

def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("C\n",""))
def getCPUuse():
    return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
)))
def getRAMinfo():
    p = os.popen('free')
    i = 0
    while 1:
        i = i + 1
        line = p.readline()
        if i==2:
            return(line.split()[1:4])
 

    
"""COMIENZA EL PROGRAMA"""
while True:
    ahora= datetime.now()
    dia=ahora.day
    mes=ahora.month
    hora=ahora.hour
    minuto=ahora.minute
    temperaturah,humedadh=higrometro()
    temperatura_sonda=float(read_temp())
    RAM_stats = getRAMinfo()
    RAM_total = round(int(RAM_stats[0]) / 1000,1)
    RAM_used = round(int(RAM_stats[1]) / 1000,1)
    CPU_temp = getCPUtemperature()
    CPU_usage = getCPUuse()
    


    if [dia,mes] in dias_invierno or mes in meses_invierno:
        if hora in luz_invierno:
            
            imprimir_valores('INVIERNO',temperaturah,humedadh,temperatura_sonda,temp_invierno_dia_calor,humedad_invierno_dia,temp_invierno_dia_sala)
            if None in higrometro():#imprimimos datos higrometro
                temperaturah=temp_invierno_dia_calor
                humedadh=humedad_invierno_dia
#bloque reles
            if temperaturah<temp_invierno_dia_calor: #usamos temperatura higrometro
                GPIO.output(pin_rele_1,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_1,GPIO.HIGH)
                
            if humedadh<humedad_invierno_dia:
                GPIO.output(pin_rele_3,GPIO.LOW)
            else:
                GPIO.output(pin_rele_3,GPIO.HIGH)
	#USAMOS VENTILADOR SIEMPRE GPIO.LOW

            GPIO.output(pin_rele_2,GPIO.LOW)
            """if temperatura_sonda<temp_invierno_dia_sala: #usamos temperatura sonda
                GPIO.output(pin_rele_2,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_2,GPIO.HIGH)"""
            #luz
            GPIO.output(pin_rele_4,GPIO.LOW)
            
            
       
        else:#invierno noche!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          
            imprimir_valores('INVIERNO',temperaturah,humedadh,temperatura_sonda,temp_invierno_noche_calor,humedad_invierno_noche,temp_invierno_noche_sala)
            if None in higrometro():#imprimimos datos higrometro
                temperaturah=temp_invierno_noche_calor
                humedadh=humedad_invierno_noche
#bloque reles
            if temperaturah<temp_invierno_noche_calor: #usamos temperatura higrometro
                GPIO.output(pin_rele_1,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_1,GPIO.HIGH)
                
            if humedadh<humedad_invierno_noche:
                GPIO.output(pin_rele_3,GPIO.LOW)
            else:
                GPIO.output(pin_rele_3,GPIO.HIGH)
	#USAMOS VENTILADOR SIEMPRE GPIO.LOW

            GPIO.output(pin_rele_2,GPIO.LOW)
            """if temperatura_sonda<temp_invierno_noche_sala: #usamos temperatura sonda
                GPIO.output(pin_rele_2,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_2,GPIO.HIGH)"""
            #luz
            GPIO.output(pin_rele_4,GPIO.HIGH)
                
            
    elif mes==4:
        if dia<21:
            #temperaturas variando cada dia
            temp_abril_dia_sala=temp_invierno_dia_sala + dia*0.025
            temp_abril_noche_sala=temp_invierno_noche_sala + dia*0.025
            temp_abril_dia_calor=temp_invierno_dia_calor + dia*0.05
            temp_abril_noche_calor=temp_invierno_noche_calor + dia*0.05
            
            if (hora in luz_abril) or (hora==9 and minuto>=30) or (hora==20 and minuto<=30):
           
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_abril_dia_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_abril_dia_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.LOW)
       
            else:#invierno noche
          
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_abril_noche_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_abril_noche_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
                GPIO.output(pin_rele_4,GPIO.HIGH)#luz
                
        else:#abril resto de dias
            
            if hora in luz_abril:
                
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_abril_dia_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_abril_dia_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.LOW)

       
            else:#invierno noche
          
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_abril_noche_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_abril_noche_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
                GPIO.output(pin_rele_4,GPIO.HIGH)#luz
                
    elif mes==5:#mayo
        if dia<21:
            #temperaturas variando cada dia
            temp_mayo_dia_sala=temp_abril_dia_sala + dia*0.025
            temp_mayo_noche_sala=temp_abril_noche_sala + dia*0.025
            temp_mayo_dia_calor=temp_abril_dia_calor
            temp_mayo_noche_calor=temp_abril_noche_calor + dia*0.05
            
            if (hora in luz_mayo) or (hora==20 and minuto<=30):
           
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_mayo_dia_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_mayo_dia_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.LOW)

       
            else:#invierno noche
          
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_mayo_noche_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_mayo_noche_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
                    
                GPIO.output(pin_rele_4,GPIO.HIGH)#luz
                
        else:#abril resto de dias
            
            if hora in luz_mayo:
                
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_mayo_dia_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_mayo_dia_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.LOW)

       
            else:#invierno noche
          
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_mayo_noche_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_mayo_noche_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
                GPIO.output(pin_rele_4,GPIO.HIGH)#luz
                
#HASTA AQUI

    elif mes==6 and [dia,mes] not in dias_verano:#junio
        if dia<21:
            #temperaturas variando cada dia
            temp_junio_dia_sala=temp_mayo_dia_sala + dia*0.025
            temp_junio_noche_sala=temp_mayo_noche_sala + dia*0.025
            temp_junio_dia_calor=temp_mayo_dia_calor + dia*0.05
            temp_junio_noche_calor=temp_mayo_noche_calor + dia*0.05
            
            if (hora in luz_junio):
           
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_junio_dia_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_junio_dia_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.LOW)
                
            else:#junio noche
          
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_junio_noche_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_junio_noche_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
                    
                GPIO.output(pin_rele_4,GPIO.HIGH)#luz
                

    elif [dia,mes] in dias_verano or mes in meses_verano:
        if hora in luz_verano:
           
            if None in higrometro():#imprimimos datos higrometro
                print('Problema con el punto de calor :(')
            else:
                print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
            if temperaturah<temp_verano_dia_calor: #usamos temperatura higrometro
                GPIO.output(pin_rele_1,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
            print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
            if temperatura_sonda<temp_verano_dia_sala: #usamos temperatura sonda
                GPIO.output(pin_rele_2,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
            GPIO.output(pin_rele_4,GPIO.LOW)

        else:#invierno noche
          
            if None in higrometro():#imprimimos datos higrometro
                print('Problema con el punto de calor :(')
            else:
                print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
            if temperaturah<temp_verano_noche_calor: #usamos temperatura higrometro
                GPIO.output(pin_rele_1,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
            print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
            if temperatura_sonda<temp_verano_noche_sala: #usamos temperatura sonda
                GPIO.output(pin_rele_2,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_2,GPIO.HIGH)
            GPIO.output(pin_rele_4,GPIO.HIGH)#luz

      
    elif mes==10:#octubre
        if dia<21:
            #temperaturas variando cada dia
            temp_octubre_dia_sala=temp_verano_dia_sala - dia*0.025
            temp_octubre_noche_sala=temp_verano_noche_sala - dia*0.025
            temp_octubre_dia_calor=temp_verano_dia_calor - dia*0.05
            temp_octubre_noche_calor=temp_verano_noche_calor - dia*0.05
            
            if (hora in luz_octubre) or (hora==20 and minuto<=30):
           
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_octubre_dia_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)
                

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_octubre_dia_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.LOW)

       
            else:#octubre noche
          
                if None in higrometro():#imprimimos datos higrometro
                    print('Problema con el punto de calor :(')
                else:
                    print('Temp={0:0.2f}*C  Humidity={1:0.2f}%'.format(temperaturah,humedadh))
	
                if temperaturah<temp_octubre_noche_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)

			
	#imprimimos temperatura sonda	
	
                print('Temp={0:0.2f}*C'.format(temperatura_sonda))
	
                if temperatura_sonda<temp_octubre_noche_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
                    
                GPIO.output(pin_rele_4,GPIO.HIGH)#luz
                
        else:#octubre resto de dias
           
            if hora in luz_octubre or (hora==20 and minuto<=30):
                
                imprimir_valores('OCTUBRE',temperaturah,humedadh,temperatura_sonda,temp_octubre_dia_calor,humedad_octubre_dia,temp_octubre_dia_sala)
                
                if None in higrometro():#imprimimos datos higrometro
                    temperaturah=temp_octubre_dia_calor
                    humedadh=humedad_octubre_dia
#bloque reles                    
                if temperaturah<temp_octubre_dia_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)
                    
                if humedadh<humedad_octubre_dia:#humedad
                    GPIO.output(pin_rele_3,GPIO.LOW)
                
                else:
                    GPIO.output(pin_rele_3,GPIO.HIGH)
	
                if temperatura_sonda<temp_octubre_dia_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.LOW)
#/bloque reles 

       
            else:#octubre noche
                
                imprimir_valores('OCTUBRE',temperaturah,humedadh,temperatura_sonda,temp_octubre_noche_calor,humedad_octubre_noche,temp_octubre_noche_sala)
          
                if None in higrometro():#imprimimos datos higrometro
                    temperaturah=temp_octubre_noche_calor
                    humedadh=humedad_octubre_noche

#bloque reles 
                if temperaturah<temp_octubre_noche_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)
                    
                if humedadh<humedad_octubre_noche:
                    GPIO.output(pin_rele_3,GPIO.LOW)
                else:
                    GPIO.output(pin_rele_3,GPIO.HIGH)
                
                if temperatura_sonda<temp_octubre_noche_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.HIGH)
                
#/bloque reles 

    elif mes==11:#noviembre
        if dia<21:
            #temperaturas variando cada dia
            temp_noviembre_dia_sala=temp_octubre_dia_sala - dia*0.025
            temp_noviembre_noche_sala=temp_octubre_noche_sala - dia*0.025
            temp_noviembre_dia_calor=temp_octubre_dia_calor
            temp_noviembre_noche_calor=temp_octubre_noche_calor - dia*0.05
            humedad_noviembre_dia=humedad_octubre_dia + dia*0.25
            humedad_noviembre_noche=humedad_octubre_noche + dia*0.25
            
            if (hora in luz_noviembre) or (hora==20 and minuto<=30) or (hora==9 and minuto>=30):
           
                imprimir_valores('noviembre',temperaturah,humedadh,temperatura_sonda,temp_noviembre_dia_calor,humedad_noviembre_dia,temp_noviembre_dia_sala)
                if None in higrometro():#imprimimos datos higrometro
                    temperaturah=temp_noviembre_dia_calor
                    humedadh=humedad_noviembre_dia
#bloque reles
                if temperaturah<temp_noviembre_dia_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)
                
                if humedadh<humedad_noviembre_dia:
                    GPIO.output(pin_rele_3,GPIO.LOW)
                else:
                    GPIO.output(pin_rele_3,GPIO.HIGH)
	
                if temperatura_sonda<temp_noviembre_dia_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.LOW)
#/bloque reles
       
            else:#noviembre noche
          
                imprimir_valores('noviembre',temperaturah,humedadh,temperatura_sonda,temp_noviembre_noche_calor,humedad_noviembre_noche,temp_noviembre_noche_sala)
                if None in higrometro():#imprimimos datos higrometro
                    temperaturah=temp_noviembre_dia_calor
                    humedadh=humedad_noviembre_dia
                    
#bloque reles         
                if temperaturah<temp_noviembre_noche_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)
                    
                if humedadh<humedad_noviembre_noche:
                    GPIO.output(pin_rele_3,GPIO.LOW)
                else:
                    GPIO.output(pin_rele_3,GPIO.HIGH)

                if temperatura_sonda<temp_noviembre_noche_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
                    
                GPIO.output(pin_rele_4,GPIO.HIGH)#luz
#/bloque reles
                
        else:#noviembre resto de dias

            if hora in luz_noviembre or (hora==20 and minuto<=30) or (hora==9 and minuto>=30):
                
                imprimir_valores('NOVIEMBRE',temperaturah,humedadh,temperatura_sonda,temp_noviembre_dia_calor,humedad_noviembre_dia,temp_noviembre_dia_sala)
                
                if None in higrometro():#imprimimos datos higrometro
                    temperaturah=temp_noviembre_dia_calor
                    humedadh=humedad_noviembre_dia
#bloque reles                    
                if temperaturah<temp_noviembre_dia_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)
                    
                if humedadh<humedad_noviembre_dia:#humedad
                    GPIO.output(pin_rele_3,GPIO.LOW)
                
                else:
                    GPIO.output(pin_rele_3,GPIO.HIGH)
	
                if temperatura_sonda<temp_noviembre_dia_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.LOW)
#/bloque reles 

       
            else:#noviembre noche
                
                imprimir_valores('NOVIEMBRE',temperaturah,humedadh,temperatura_sonda,temp_noviembre_noche_calor,humedad_noviembre_noche,temp_noviembre_noche_sala)
          
                if None in higrometro():#imprimimos datos higrometro
                    temperaturah=temp_noviembre_noche_calor
                    humedadh=humedad_noviembre_noche

#bloque reles 
                if temperaturah<temp_noviembre_noche_calor: #usamos temperatura higrometro
                    GPIO.output(pin_rele_1,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_1,GPIO.HIGH)
                    
                if humedadh<humedad_noviembre_noche:
                    GPIO.output(pin_rele_3,GPIO.LOW)
                else:
                    GPIO.output(pin_rele_3,GPIO.HIGH)
                
                if temperatura_sonda<temp_noviembre_noche_sala: #usamos temperatura sonda
                    GPIO.output(pin_rele_2,GPIO.LOW)
		
                else:
                    GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
                GPIO.output(pin_rele_4,GPIO.HIGH)
                
    
    elif mes==12 and [dia,mes] not in [dias_invierno]:
        #temperaturas variando cada dia
        temp_diciembre_dia_sala=temp_noviembre_dia_sala - dia*0.05
        temp_diciembre_noche_sala=temp_noviembre_noche_sala - dia*0.05
        temp_diciembre_dia_calor=temp_noviembre_dia_calor - dia*0.05
        temp_diciembre_noche_calor=temp_noviembre_noche_calor - dia*0.05
        humedad_diciembre_dia=humedad_noviembre_dia + dia*0.5
        humedad_diciembre_noche=humedad_noviembre_noche + dia*0.5
        
        
        if (hora in luz_diciembre) or (hora==9 and minuto>=30):
           
            imprimir_valores('DICIEMBRE',temperaturah,humedadh,temperatura_sonda,temp_diciembre_dia_calor,humedad_diciembre_dia,temp_diciembre_dia_sala)
            if None in higrometro():#imprimimos datos higrometro
                temperaturah=temp_diciembre_dia_calor
                humedadh=humedad_diciembre_dia
#bloque reles
            if temperaturah<temp_diciembre_dia_calor: #usamos temperatura higrometro
                GPIO.output(pin_rele_1,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_1,GPIO.HIGH)
                
            if humedadh<humedad_diciembre_dia:
                GPIO.output(pin_rele_3,GPIO.LOW)
            else:
                GPIO.output(pin_rele_3,GPIO.HIGH)
	
            if temperatura_sonda<temp_diciembre_dia_sala: #usamos temperatura sonda
                GPIO.output(pin_rele_2,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_2,GPIO.HIGH)
            #luz
            GPIO.output(pin_rele_4,GPIO.LOW)
       
        else:#diciembre noche
          
            imprimir_valores('DICIEMBRE',temperaturah,humedadh,temperatura_sonda,temp_diciembre_noche_calor,humedad_diciembre_noche,temp_diciembre_noche_sala)
            if None in higrometro():#imprimimos datos higrometro
                temperaturah=temp_diciembre_dia_calor
                humedadh=humedad_diciembre_dia
                    
#bloque reles         
            if temperaturah<temp_diciembre_noche_calor: #usamos temperatura higrometro
                GPIO.output(pin_rele_1,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_1,GPIO.HIGH)
                    
            if humedadh<humedad_diciembre_noche:
                GPIO.output(pin_rele_3,GPIO.LOW)
            else:
                GPIO.output(pin_rele_3,GPIO.HIGH)

            if temperatura_sonda<temp_diciembre_noche_sala: #usamos temperatura sonda
                GPIO.output(pin_rele_2,GPIO.LOW)
		
            else:
                GPIO.output(pin_rele_2,GPIO.HIGH)               
            GPIO.output(pin_rele_4,GPIO.HIGH)#luz
            
    infile=open('log.txt','r')
    #outfile=write('hora=%d:%d.%s,                                temp_cpu=%s,cpu_used=%s, ram_used=%s, temp_h=%.2f, humedad=%.2f, temp_sonda=%.2f\n'%(hora,minuto,str(ahora.second),str(CPU_temp),str(CPU_usage),str(RAM_used),temperaturah,humedadh,temperatura_sonda))

    a=[]
    for i in infile:
        a.append(i)
    
    a.append('hora=%d:%d.%s,                                temp_cpu=%s,cpu_used=%s, ram_used=%s, temp_h=%.2f, humedad=%.2f, temp_sonda=%.2f\n'%(hora,minuto,str(ahora.second),str(CPU_temp),str(CPU_usage),str(RAM_used),temperaturah,humedadh,temperatura_sonda))
    infile.close()
    #titulo=str(ahora.year)+ str(ahora.month) +str(ahora.day)
    outfile=open('log.txt','r+')
    
    for l in a:
        outfile.write(l)

    outfile.close()
       
