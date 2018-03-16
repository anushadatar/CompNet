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
		string_val = morse_string('okay')
		blink_sentence(string_val)
