#!/usr/bin/env python3

import random

def rand_gen():
	numbers = [1, 2, 3, 4, 5]
	prob = [0.5, 0.25, 0.15, .05, .05]
	random.seed()
	print(random.choices(numbers, weights=prob, k=1).pop())
