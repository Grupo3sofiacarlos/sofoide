# importamos las librerias importantes
import os
import glob
import time
import serial

os.system("modprobe w1-gpio") #parametros para el funcionamiento de los pines
os.system('modprobe w1-therm')
base_dir= "/sys/bus/w1/devices/"
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
def read_temp_raw():	#funcion recoleccion de datos
	f= open(device_file, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()	#funcion oreganizacion y modelacion del dato
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
		return temp_c
class Sensor():
	temperatura = read_temp()
mitemp= Sensor()

arduino = serial.Serial("/dev/ttyACM0",9600)
arduino.flushInput()
while True:
	try:
		lineBytes = arduino.readline()
		datos= lineBytes.decode("utf-8").strip()
		print(datos)
		print("la temperatura es : "+str(mitemp.temperatura)+" °C")
		time.sleep(0.5)
	except keyboardInterrupt:
		break
