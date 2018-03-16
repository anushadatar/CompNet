#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# Bit rate in bits/second.
bit_rate = 1000
rate = 1/bit_rate

GPIO.setmode(GPIO.BCM)
# Set both of the pins.
GPIO.setup(1, GPIO.IN)
GPIO.setup(0, GPIO.OUT)

# Locking Sequence : 7 1s
# Unlocking Sequence : 7 0S (stop transmitting)


# GPIO.input(1) returns a boolean True if high voltage, False if low voltage.
# GPIO.output(0, GPIO.HIGH) sets the pin to high.
def main():
	message = "Never gonna give you up"
	if (GPIO.input(1)):
		print("receiving")	
		# Set the received sequence to be 7 ones if you receive any pulse. 
		# This way, we can continuously check whether or not the other side
		# is still transmitting without potentially missing values. 
		received =  [1] * 7
		# Unlocking sequence : 7 continous zeroes (start transmitting).
		while sum(received[-7:]) > 0:
				if GPIO.input(1):
					received.append(1)
				else:
					received.append(0)
				time.sleep(rate)
		print(translateFromASCII(received[14:]))
	else:
		print("transmitting")
		# Locking sequence 
		message_list = [1] * 7
		message_list.extend(encodeData(message))
		unlock_sequence = [0] * 7
		message_list.extend(unlock_sequence)
		for bit in message_list:
			if (bit == 0):
				GPIO.output(0, GPIO.LOW)
			else:
				GPIO.output(0, GPIO.HIGH)
			time.sleep(rate)
	


def encodeData(data):
	
    # Turn the text into a list of chrs
    data = list(data)
    # Turn the list of chrs into a list of binary
    temp = []
    for char in data:
        # Conversion: chr --> ASCII --> binary
        temp.append("{0:b}".format(int(ord(char))))
    data = temp
    # Make sure all the binary values (bytes) have the same length (7 bits)
    temp = []
    for byte in data:
        if len(byte) > 7:
            print("Byte length error!")
            break
        while len(byte) < 7:
            byte = "0"+byte
        temp.append(byte)
    data = temp
    # Convert the binary terms into a single string
    dataString = ""
    for byte in data:
        dataString += byte
    # Convert the string into a list of single numbers
    data = list(dataString)
    print("Data encoded")
    return data

def translateFromASCII(bits):
    message = ""
    while len(bits) >= 7:
        # Grab the current byte
        byte = bits[:7]
        # Remove the current byte from the array
        bits = bits[7:]
        # Convert the byte into a base 2 integer
        byte = int(''.join(byte), 2)
        # Convert from ASCII base 2 into chr
        char = chr(byte)
        # Add to <message>
        message += char
    return message


while True:
	main()
