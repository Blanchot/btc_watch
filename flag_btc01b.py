# flag_btc1b.py (first test motor control and saving volume to file)
# Load from CLI: python3 -i flag_btc1b.py

# logging and main loop turned off
# based on 4 step 'Basic Stepper Code'
# and btc_volume01.py (for the BTC volume check code)

# Current range: 0 - 8600 steps
# Time to complete range approx. 1:30
# maximum 5 min volume I've seen up until now is 2500

import datetime
import time
import requests, json
# import sys # for logging
import os.path # for volume file check
import RPi.GPIO as GPIO

'''
import logging
format_string = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, filename='BTC_flag_log.log', format=format_string)
logging.info('Begin 5 Minute BTC Flag/Volume Log')

interval_List = (2,7,12,17,22,27,32,37,42,47,52,57) #times to check- 2 min after each 5 min interval
URL3 = "https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&aggregate=5&limit=3"
'''

wait = .01 # time to pause between motor steps
pos = 1 # values 0 to 8

#count = 0 # motor counter

GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(True)
GPIO.setwarnings(False)

# pins setup
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)

print('Use: test_motor()')

#---STEPPER MOTOR CONTROL CODE---
def step(pos):
  if pos==0:
    #print('Pos: 0')
    GPIO.output(18,0)
    GPIO.output(23,0)
    GPIO.output(24,0)
    GPIO.output(25,0)
  elif pos==1:
    #print('Pos: 1')
    GPIO.output(18,1)
    GPIO.output(23,0)
    GPIO.output(24,0)
    GPIO.output(25,0)
  elif pos==2:
    #print('Pos: 2')
    GPIO.output(18,0)
    GPIO.output(23,1)
    GPIO.output(24,0)
    GPIO.output(25,0)
  elif pos==3:
    #print('Pos: 3')
    GPIO.output(18,0)
    GPIO.output(23,0)
    GPIO.output(24,1)
    GPIO.output(25,0)
  elif pos==4:
    #print('Pos: 4')
    GPIO.output(18,0)
    GPIO.output(23,0)
    GPIO.output(24,0)
    GPIO.output(25,1)



def steps(num): # 4 STEP COUNTER-CLOCKWISE MOTOR ROTATION
  global pos # current position
  global count # current counter
  if num > 0:
    for i in range (0, abs(num)):
      step(pos)
      time.sleep(wait)
      #count += 1 #add 1 to counter
      #--- Begin code that determines direction of rotation
      if(pos == 1):
        pos = 5
      pos -= 1 #subtract 1 from motor pos
      #--- End code that determines direction of rotation
  else:
    for i in range (0, abs(num)):
      step(pos)
      time.sleep(wait)
      #count -= 1 #subtract 1 from counter
      #--- Begin code that determines direction of rotation
      pos += 1 # add 1 to motor pos
      if(pos >= 5):
        pos = 1
      #--- End code that determines direction of rotation
  step(0) # Turn motor off

#GPIO.cleanup()



#---LOADING AND CALCULATING VOLUME DIFFERENCES---
# loads prev_volume or initialises it if it doesn't exist
def load_volume():
  if os.path.isfile('volume.txt'):
    file_in = open('volume.txt','rt')
    prev_volume = int(file_in.read()) # convert string into integer
    file_in.close()
    return prev_volume
  else:
    file_out = open('volume.txt','wt')
    file_out.write('0')
    file_out.close()
    return 0


# write volume to file
def write_volume(s):
  file_out = open('volume.txt','wt')
  file_out.write(s)
  file_out.close()


# calculate difference between new_volume and prev_volume
def volume_diff(new_volume, prev_volume):
  volume_diff = new_volume - prev_volume
  steps(volume_diff) # Send to motor
  print('Volume difference: ',volume_diff)

  

prev_volume = load_volume()
print('Previous volume: ',prev_volume)

def test_motor():
  global prev_volume
  #prev_volume = load_volume()
  print('Previous volume: ',prev_volume)
  new_volume = int(input('Input a new volume: '))
  write_volume(str(new_volume))
  volume_diff(new_volume,prev_volume) # Calculates and sends diff to motor
  prev_volume = new_volume
  #return prev_volume





'''

# ---BTC VOLUME CHECK CODE 

# get BTC market volume using the Cryptocompare 5 MINUTE API
def get_BTC_5_min_volume():
  try:
    r = requests.get(URL3)
    market_volume_txt = json.loads(r.text)
    #time1 = json.loads(r.text)['Data'][0]['time']
    #volume1 = json.loads(r.text)['Data'][0]['volumefrom']
    #time2 = json.loads(r.text)['Data'][1]['time']
    #volume2 = json.loads(r.text)['Data'][1]['volumefrom']
    time3 = json.loads(r.text)['Data'][2]['time']
    volume3 = json.loads(r.text)['Data'][2]['volumefrom']
    return time3, volume3
    #time4 = json.loads(r.text)['Data'][3]['time']
    #volume4 = json.loads(r.text)['Data'][3]['volumefrom']
  except requests.ConnectionError:
    print("Error querying Cryptocompare API")


def convert_seconds(secs): #used in logging
  converted = datetime.datetime.fromtimestamp(secs).strftime('%Y-%m-%d %H:%M:%S')
  return converted



#---TEST CODE---
def test():
  get_BTC_5_min_volume()
  
'''


'''
while True: # main loop
  tijd = time.localtime() #create a struct_time object
  if tijd[4] in interval_List: #and check if the number of minutes is in the interval_List
    time3, volume3 = get_BTC_5_min_volume()
    print()
    vol_time = convert_seconds(time3)
    print(vol_time)
    print('5 minute volume: ', volume3)
    logging.info('From: {}, Vol: {}'.format(vol_time, volume3))
    
    #---SEND TO MOTOR CONTROL
    if volume3 < 2500:
      motor_steps = int(volume3 * 3)
      steps(motor_steps)
    else:
      motor_steps = 8000
    time.sleep(65) # wait a bit more than a minute to escape if = true

  else:
    time.sleep(5)

'''

'''
# CALIBRATION CODE

def autocalibrate(): #reverse 'last positions' for autocalibration
  global m0
  global m1
  global m2
  global m3
  f_in = open('last_positions', 'rt') 
  read_str = f_in.read()
  f_in.close()
  
  read_pos_list = read_str.split()
  print(read_pos_list)
  # turn each element of the list into an int and reverse its sign
  recalib_m0 = (int(read_pos_list[0])) * -1
  recalib_m1 = (int(read_pos_list[1])) * -1
  recalib_m2 = (int(read_pos_list[2])) * -1
  recalib_m3 = (int(read_pos_list[3])) * -1
  m0steps_8(recalib_m0)
  m1steps_8(recalib_m1)
  m2steps_8(recalib_m2)
  m3steps_8(recalib_m3)
  
  #Reset each motor to 0
  m0 = 0
  m1 = 0
  m2 = 0
  m3 = 0

#GPIO.cleanup()
'''
