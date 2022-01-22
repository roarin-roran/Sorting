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

	# * * * * * * * * * * * * * *
	# * * * * * SORTERS * * * * *
	# * * * * * * * * * * * * * *

	# sorts an input using two way merging
	def mergeSort2(self):
		self.wIP = self.input

		# loop over itterative rounds
		while len(self.wIP) > 1:
			# loop through input
			i = 0
			while i < len(self.wIP):
				if len(self.wIP) - i >= 2:
					leftInput = self.wIP.pop(i)
					rightInput = self.wIP.pop(i)

					self.wIP.insert(i, self.merge2([leftInput, rightInput]))

				i += 1
		return self.wIP[0]

	# sorts an input using three way merging
	def mergeSort3(self):
		self.wIP = self.input

		# loop over itterative rounds
		while len(self.wIP) > 1:
			# loop through input
			i = 0
			while i < len(self.wIP):
				if len(self.wIP) - i >= 3:
					leftInput = self.wIP.pop(i)
					centreInput = self.wIP.pop(i)
					rightInput = self.wIP.pop(i)

					self.wIP.insert(i, self.merge3([leftInput, centreInput, rightInput]))
				# handle the end
				elif len(self.wIP) == 2:
					self.wIP = [self.merge2(self.wIP)]
					break

				i += 1
		return self.wIP[0]

	# sorts an input using four way merging
	def mergeSort4(self):
		self.wIP = self.input

		# loop over itterative rounds
		while len(self.wIP) > 1:
			# loop through input
			i = 0
			while i < len(self.wIP):
				if len(self.wIP) - i >= 4:
					leftInput = self.wIP.pop(i)
					centreLeftInput = self.wIP.pop(i)
					centreRightInput = self.wIP.pop(i)
					rightInput = self.wIP.pop(i)

					self.wIP.insert(i, self.merge4([leftInput, centreLeftInput, centreRightInput, rightInput]))
				# handle the end
				elif len(self.wIP) == 3:
					self.wIP = [self.merge3(self.wIP)]
					break
				elif len(self.wIP) == 2:
					self.wIP = [self.merge2(self.wIP)]
					break

				i += 1

		return self.wIP[0]

	# * * * * * * * * * * * * * * * * * *
	# * * * * * SUPPORT METHODS * * * * *
	# * * * * * * * * * * * * * * * * * *

	# merges two inputs
	@staticmethod
	def merge2(mergeInput):
		output = []

		while len(mergeInput[0]) > 0 and len(mergeInput[1]) > 0:
			if mergeInput[0][0] <= mergeInput[1][0]:
				output.append(mergeInput[0].pop(0))
			else:
				output.append(mergeInput[1].pop(0))

		# if there's anything left in either array, there's nothing left in the other one,
		# and it's all greater than the output array

		if len(mergeInput[0]) > 0:
			output += mergeInput[0]
		elif len(mergeInput[1]) > 0:
			output += mergeInput[1]

		return output

	# merges three inputs using merge2
	@staticmethod
	def merge3(mergeInput):
		output = []

		leftInput = sorterManager.merge2([mergeInput.pop(0), mergeInput.pop(0)])

		output = sorterManager.merge2([leftInput, mergeInput.pop(0)])

		return output

	# merges four inputs using merge2
	@staticmethod
	def merge4(mergeInput):
		output = []

		leftInput = sorterManager.merge2([mergeInput.pop(0), mergeInput.pop(0)])
		rightInput = sorterManager.merge2([mergeInput.pop(0), mergeInput.pop(0)])

		output = sorterManager.merge2([leftInput, rightInput])

		return output




ourSM = sorterManager()
print("input")
print(ourSM.generateInput(1, 0.1, 0.6))
print()
print("output:")
print(ourSM.mergeSort4())
