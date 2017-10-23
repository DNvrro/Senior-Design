from smbus import SMBus
import time

b = SMBus(1) # /dev/i2c-1

address = 0x4c	# Address of the LTC 2990
mode1 = 0x58	#Battery monitoring mode (Voltage/Temp)
mode2 = 0x59
'''
    The update function below is defined for updating
    the values needed for the while loop in the
    monitor_battery.py program
    '''
def update():
 global r0,r1,r4,r5,r6,r7,r8,r9,ra,rb,re,rf,mode,address
 #b.write_byte_data(address, 0x01, mode)    # Initializes the IC and set mode	
 #b.write_byte_data(address, 0x02,0x00 ) # Trigger a data collection
 
 try:
	 if b.read_byte_data(address, 0x01) != mode1:
		 b.write_byte_data(address, 0x01, mode)
		 b.write_byte_data(address, 0x02, 0x00)
		 time.sleep(1)
 except IOError, error:
	print error

 b.write_byte_data(address, 0x01, mode1)
 b.write_byte_data(address, 0x02, 0x00)	
	
 r0 = b.read_byte_data(address, 0x00) # Status
 r1 = b.read_byte_data(address, 0x01) # Control - mode select
 r4 = b.read_byte_data(address, 0x04) # Temp. Int. MSB
 r5 = b.read_byte_data(address, 0x05) # Temp. Int. LSB
 r6 = b.read_byte_data(address, 0x06) # V1, V1 - V2 or TR1 MSB
 r7 = b.read_byte_data(address, 0x07) # V1, V1 - V2 or TR1 LSB
 r8 = b.read_byte_data(address, 0x08) # V2, V1 - V2 or TR1 MSB
 r9 = b.read_byte_data(address, 0x09) # V2, V1 - V2 or TR1 LSB
 ra = b.read_byte_data(address, 0x0a) # V3, V3 - V4 or TR2 MSB
 rb = b.read_byte_data(address, 0x0b) # V3, V3 - V4 or TR2 LSB

 re = b.read_byte_data(address, 0x0e) # Vcc MSB
 rf = b.read_byte_data(address, 0x0f) # Vcc LSB
 updated =[ra,rb,r4,r5,r6,r7]
 
 return updated

	
def temperature(msb,lsb):   #The function to calculate temperature 
  msb = format(msb, '08b')  #The msb is converted to a binary string
  msb = msb[3:]     #The msb is then shifted 3 places to the left
  lsb = format(lsb, '08b') #The lsb is converted to a binary string
  temp = msb + lsb  #temp is set equal to the sum of the two strings 
  temp = int(temp, 2)/16 #temp is converted to decimal value and then calculated
  return temp   #The value of temp is returned


def bat_volt(msb,lsb): #The function to calculate battery voltage is defined
	b.write_byte_data(address, 0x01, mode1) 
	b.write_byte_data(address, 0x02, 0x00)
	
	msb = format(msb, '08b')#The msb is converted to a binary string
	#print(msb)
	msb = msb[1:] #The msb is shifted to the left 1 place
	lsb = format(lsb, '08b') #The lsb is converted to a binary string
	#print(lsb)
	volt = msb + lsb #volt is set equal to the sum of the two strings
	volt = int(volt, 2) * 0.00030518 #volt is converted to decimal and then calculated
	return volt #The value of volt is returned
	
def voltage(msb,lsb):
  msb = format(msb, '08b')
  msb = msb[1:]
  lsb = format(lsb, '08b')
    
  volt = msb[1:] + lsb
  volt = int(volt, 2) * 0.00030518
  return volt	
	
def get_current(lsb, msb): #The function to calculate current is defined
	b.write_byte_data(address, 0x01, mode2) #Control register 0x59 is initialized to collect current data
	b.write_byte_data(address, 0x02, 0x00) #Data collection is triggered
	#print('r6 is ' + str(msb))
	#print('r7 is ' + str(lsb))
	msb = format(msb, '08b') #The msb is converted to a binary string
	msb = msb[2:] #The msb is shifted to the left 2 places
	lsb = format(lsb, '08b') #The lsb is converted to a binary string
	current = msb[1:] + lsb #current is set equal to the sum of the two strings
	current = (int(current, 2) * 0.00001942) /0.015 #current is converted to decimal,then calculated
		
	return current	#The value of current is returned
update() #update function is callled to initialize variables	
#print(r1)	

print ('from get_data \n ')
print "Ambient Temp. : %s Celsius" %temperature(r4,r5) #Calls the temperature function & calculates it using the bits from the registers
print "Battery Voltage : %s V" %bat_volt(r6,r7) #Calls the bat_volt function & calculates it using the bits from the registers
print "Battery Temp.: %s Celsius" %temperature(ra,rb) #Calls the temperature function & calculates temp using the bits from the registers
print "Current I-Bat : %s mA" %get_current(r6,r7) #Calls the get_current function & calculates it using the bits from the registers
vin = voltage(re,rf) + 2.5
print "VCC        : %s V" %vin #Prints voltage inputted from the Raspberry Pi
	
	
	

