import random

PROCESS_RUNS = False

# misc todo:
# 1. fiddle with statistics to stop everything in a run from getting high - chance of run terminating based on run length and size
# 2. slice by reference instead of copying

# plan
# 1. peeksort
# 2. powersort
# 3. consolidation
# 4. analysis

class sorterManager:
	# * * * * * * * * *  * * * * * * * * *
	# * * * * * INPUT GENERATION * * * * *
	# * * * * * * * * *  * * * * * * * * *

	# generates an unsorted input, formatted for the sorters
	def generateInput(self, sizePower, sortedRunLengthPower, unsortedRunLengthPower):
		self.input = []
		self.inputLength = 10**sizePower

		# initialise run toggle
		runNext = random.choice([True, False])

		while len(self.input) < self.inputLength:
			# determines the length of the next run of sorted/unsorted inputs
			if runNext:
				runLength = int(random.random()*10**sortedRunLengthPower)
			else:
				runLength = int(random.random()*10**unsortedRunLengthPower)

			# constructs the new portion
			newPortion = [int(random.random()*self.inputLength)]
			while len(newPortion) < runLength:
				newChar = int(random.random()*self.inputLength)
				if newChar >= newPortion[-1] or not runNext:
					newPortion.append(newChar)

			self.input += newPortion

		# because of the run system, length can be slightly overshot - delete surplus elements
		while len(self.input) > self.inputLength:
			self.input.pop(-1)

		# wrap for output - each presorted element needs wrapping in square brackets (whether or not runs are detected)
		if PROCESS_RUNS:
			self.input = ourSM.processRuns()
		else:
			processedInput = []
			for i in self.input:
				processedInput.append([i])

			self.input = processedInput


		return self.input

	# detects runs in an input and partitions them with square brackets
	def processRuns(self):
		# initialise
		runProcessedInput = []
		run = [self.input[0]]
		firstStep = True
		
		# wraps all runs
		for i in self.input:
			# ignore first step
			if firstStep:
				firstStep = False
			# if in the run - add it on
			elif i >= run[-1]:
				run.append(i)
			# if it's broken the run, append and reset
			else:
				runProcessedInput.append(run)
				run = [i]

		# last char can't break last run, so tack the last run on
		runProcessedInput.append(run)

		return runProcessedInput



