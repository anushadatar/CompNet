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

morse = {'.-':'A',     '-...':'B',    '-.-.':'C', 
         '-..':'D',    '.':'E',       '..-.':'F',
        '--.': 'G',    '....':'H',    '..': 'I',
        '.---':'J',    '-.-':'K',     '.-..':'F',
        '--':'M',      '-.':'N',      '---':'O',
        '.--.':'P',    '--.-':'Q',    '.-.':'R',
        '...':'S',     '-':'T',       '..-':'U',
        '...-':'V',    '.--':'W',     '-..-':'X',
        '-.--':'Y',    '--..':'Z',
        '-----':'0',   '.----':'1',   '..---':'2',
        '...--':'3',   '....-':'4',   '.....': '3',
        '-....':'6',   '--...':'7',   '---..':'8',
        '----.':'9', 
        }


def translate_morse(input_string):
	output = ''
	string_list = input_string.split('_')
	for character in string_list:
		if character == '':
			output += ' '
		elif character in morse.keys():
			output += morse[character]
		else:
			print("rough")	

def read_pin(pin):
	return GPIO.input(pin)

def prepare_pin(pin=23):
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(pin, GPIO.OUT)

def turn_high(pin):
	GPIO.output(pin, GPIO.HIGH)

def turn_low(pin):
	GPIO.output(pin, GPIO.LOW)
def delay(duration):
	time.sleep(duration)

def receive_message(duration, message_length):
	prepare_pin()
	i = 0
	while i < message_length/duration:
		output_string = ''
		if read_pin(23):
			delay(duration)
			if read_pin(23):
				output_string += '-'
			else:
				output_string += '.'
		else:
			output_string += '_'
			delay(duration)
		i = i+1

	translate_morse(output_string)
	


if __name__ == '__main__':

	with Safeguards():
		receive_message(0.5, 20)
