#!/usr/bin/env python3

import random
import time
from threading import Thread, Event
import queue

class EventThread(Thread):
	def __init__(self):
		self._run = Event()
		super().__init__()

	def join(self):
		self._run.clear()
		return super().join()

	def start(self):
		self._run.set()
		super().start()

class Writer(EventThread):
	def __init__(self, input, filename = 'history.txt'):
		self._q = input
		self._filename = filename
		super().__init__()

	def run(self):
		f = open(self._filename, 'a')
		while self._run.is_set():
			try:
				timestamp, num = self._q.get(timeout = 5)
			except queue.Empty:
				pass
			else:
				 f.write('Time: {} Number: {}\n'.format(time.ctime(timestamp), num))
		f.close()

class RGen(EventThread):
	def __init__(self, output):
		self._history = []
		self._numbers = [1, 2, 3, 4, 5]
		self._prob = [0.5, 0.25, 0.15, .05, .05]
		self._output = output
		random.seed()
		super().__init__()

	def _rand_gen(self):
		return (random.choices(self._numbers, weights=self._prob, k=1).pop())

	def random(self):
		num = self._rand_gen()
		self._history.insert(0, num)
		if len(self._history) > 100:
			self._history.pop()
		timestamp = time.time()
		self._output.put((timestamp, num))
		return time.ctime(timestamp), num

	def freq(self, *args):
		nums = args if args else range(1,6)
		return ['{} = {}%'.format(n, int(round((self._history.count(n) / len(self._history)) * 100))) for n in nums]

	def run(self):
		while self._run.is_set():
			print(self.random())
			time.sleep(1)

def gen_random(workers = 5):
	q = queue.PriorityQueue()
	w = Writer(q)
	w.start()
	r = [RGen(q) for x in range(workers)]
	print('Press Enter to exit...')
	for x in r:
		x.start()
	return w, r

writer, workers = gen_random()
input()
for w in workers:
	w.join()
writer.join()
for w in workers:
	print(w.freq())
