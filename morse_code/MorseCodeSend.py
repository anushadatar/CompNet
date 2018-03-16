#!/usr/bin/env python

import time
import RPi.GPIO as GPIO


duration = 0.5

class Safeguards:
	def __enter__(self):
		return self
	def __exit__(self, *rabc):
		GPIO.cleanup()
		print("Safe exit succeeded")
		return not any(rabc)

morse = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',
		'a': '.-',     'b': '-...',   'c': '-.-.',                             
  		'd': '-..',    'e': '.',      'f': '..-.',                              
  		'g': '--.',    'h': '....',   'i': '..',                                
        'j': '.---',   'k': '-.-',    'l': '.-..',                              
		'm': '--',     'n': '-.',     'o': '---',                               
		'p': '.--.',   'q': '--.-',   'r': '.-.',                               
		's': '...',    't': '-',      'u': '..-',                               
		'v': '...-',   'w': '.--',    'x': '-..-',                              
 		'y': '-.--',   'z': '--..',                           
        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.' 
        }

def morse_string(input_string):

	morse_string = ''
	for letter in input_string:
		if letter == ' ':
			morse_string += '__'
		else:	
			morse_string += morse[letter]
			morse_string += '_'
	return morse_string



def prepare_pin(pin=17):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)

def turn_high(pin):
	GPIO.output(pin, GPIO.HIGH)

def turn_low(pin):
	GPIO.output(pin, GPIO.LOW)
def delay(duration):
	time.sleep(duration)

def blink_sentence(sentence, sampling_rate = 0.5, pin=17):
	prepare_pin(pin)
	for character in sentence:
		if character == '-':
			turn_high(pin)
			delay(duration*2)
			turn_low(pin)
			delay(duration)
		elif character == '.':
			turn_high(pin)
			delay(duration)
			turn_low(pin)
			delay(duration)
		elif character == '_':
			turn_low(pin)
			delay(duration)
		else:
			print(character)
			print("Error translating sentence.")


if __name__ == '__main__':
	with Safeguards():
		prepare_pin(17)
		print("Turning Low")
		turn_low(17)
		time.sleep(1)
		print("Turning high")
		turn_high(17)
	#	string_val = morse_string('okay')
	# 	blink_sentence(string_val)
