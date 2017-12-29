#!/usr/bin/env python3

import random
import time

class RGen():
	def __init__(self):
		self._history = []
		self._numbers = [1, 2, 3, 4, 5]
		self._prob = [0.5, 0.25, 0.15, .05, .05]
		random.seed()

	def _rand_gen(self):
		return (random.choices(self._numbers, weights=self._prob, k=1).pop())

	def random(self):
		num = self._rand_gen()
		self._history.insert(0, num)
		if len(self._history) > 100:
			self._history.pop()
		return num

	def freq(self, *args):
		nums = args if args else range(1,6)
		return ['{} = {}%'.format(n, int(round((self._history.count(n) / len(self._history)) * 100))) for n in nums]

	def run(self):
		print(self.random())

	def write(self, filename = 'history.txt'):
		if (len(self._history) == 0):
			print('List empty, generate a number first')
		else:
			f = open(filename, 'a')
			f.write('Time: {} Number: {}\n'.format(time.ctime(), self._history[0]))
			f.close()
