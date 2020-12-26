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
URL = "https://min-api.cryptocompare.com/data/histominute?fsym=BTC&tsym=USD&aggregate=5&limit=3"
'''

wait = .01 # time to pause between motor steps
pos = 1 # stepper motor position (values 0 to 8)
motor_factor = 3 # volume multiplication factor for num of motor steps()


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
  #global count # current counter
  num = num * motor_factor
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

#---END MOTOR CONTROL CODE

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
# and send to motor
def volume_diff(new_volume, prev_volume):
  volume_diff = new_volume - prev_volume
  steps(volume_diff) # Send to motor
  print('Volume difference: ',volume_diff)


prev_volume = load_volume()
print('Previous volume: ',prev_volume)
#---END LOADING AND CALCULATING VOLUME DIFFERENCES---

# ---BEGIN BTC VOLUME CHECK CODE---
# get BTC market volume using the Cryptocompare 5 MINUTE API
def get_BTC_5_min_volume():
  try:
    r = requests.get(URL)
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

#---END BTC VOLUME CHECK CODE---

'''
def test_motor():
  global prev_volume
  print('Previous volume: ',prev_volume)
  new_volume = int(input('Input a new volume: '))
  #---TEST THAT NEW VOLUME IS NOT LARGER THAN 3000---
  if new_volume <= 3000:
    write_volume(str(new_volume))
    volume_diff(new_volume,prev_volume) # Calculate and send diff to motor
  else:
    print('5 minute volume exceeds 3000!')
    print('Setting volume to 3000')
    new_volume = 3000
    write_volume(str(new_volume))
    volume_diff(new_volume,prev_volume) # Calculate and send diff to motor
  #---END NEW VOLUME TEST
  prev_volume = new_volume
'''

def run_motor(new_volume):
  global prev_volume
  print('Previous volume: ',prev_volume)
  #---TEST THAT NEW VOLUME IS NOT LARGER THAN 3000---
  if new_volume <= 3000:
    write_volume(str(new_volume))
    volume_diff(new_volume,prev_volume) # Calculate and send diff to motor
  else:
    print('5 minute volume exceeds 3000!')
    print('Setting volume to 3000')
    new_volume = 3000
    write_volume(str(new_volume))
    volume_diff(new_volume,prev_volume) # Calculate and send diff to motor
  #---END NEW VOLUME TEST
  prev_volume = new_volume



'''
while True: # main loop
  tijd = time.localtime() #create a struct_time object
  if tijd[4] in interval_List: #and check if the number of minutes is in the interval_List
    time, new_volume = get_BTC_5_min_volume()
    print()
    vol_time = convert_seconds(time)
    print(vol_time)
    print('5 minute volume: ', new_volume)
    logging.info('From: {}, Vol: {}'.format(vol_time, new_volume))
    run_motor(new_volume) # Send new_volume to motor 
    time.sleep(65) # wait a bit more than a minute to escape if = true

  else:
    time.sleep(5)

'''


