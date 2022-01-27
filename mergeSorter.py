import math

class mergeSorter:
	def __init__(self, input):
		self.input = input 

		self.ping = input.copy()
		self.pong = input.copy()
		# current array is always from the *last* execution of the loop
		self.pingCurrent = True

	# * * * * * * * * * * * * * * * * * *
	# * * * * * SUPPORT METHODS * * * * *
	# * * * * * * * * * * * * * * * * * *

	def getCurrentArray(self):
		if self.pingCurrent:
			return self.ping
		else:
			return self.pong

	def getWorkingOutArray(self):
		if not self.pingCurrent:
			return self.ping
		else:
			return self.pong

	def sendToOutput(self, value):
		self.getWorkingOutArray()[self.workingOutPos] = value
		self.workingOutPos += 1


	# * * * * * * * * * * * * * *
	# * * * * * MERGERS * * * * *
	# * * * * * * * * * * * * * *

	def merge2(self, start, mid, end):
		# the left run and modified section of the working our array start at start of the relevent section
		leftPos = start
		self.workingOutPos = start
		# the midpoint is defined as the start of the right hand run
		rightPos = mid

		# while you're still inside both runs
		while leftPos < mid and rightPos < end:
			# if the next LH element is smaller than the next RH element
			if self.getCurrentArray()[leftPos] < self.getCurrentArray()[rightPos]:
				# use it
				self.sendToOutput(self.getCurrentArray()[leftPos])
				leftPos += 1
			else:
				self.sendToOutput(self.getCurrentArray()[rightPos])
				rightPos += 1

		# when one option is removed, fill whatever remains
		for i in range(mid - leftPos):			
			self.sendToOutput(self.getCurrentArray()[leftPos])
			leftPos += 1

		for i in range(end - rightPos):
			self.sendToOutput(self.getCurrentArray()[rightPos])
			rightPos += 1

	# * * * * * * * * * * * * * *
	# * * * * * SORTERS * * * * *
	# * * * * * * * * * * * * * *

	# merge sort, merging two elements at a time
	def mergeSort2(self):
		runLength = 1

		while runLength <= len(self.input):
			for i in range(math.ceil(len(self.input)/(2*runLength))):
				# beginning of a run is assumed to be safe
				start = runLength*2*i

				# middle must be less than the end of the array or the second element has no contents
				mid    = runLength*(2*i+1)
				if mid > len(self.input):
					break

				# end must be capped at the length of the array to prevent overruns
				end   = runLength*(2*i+2)
				if end > len(self.input):
					end = len(self.input)

				self.merge2(start, mid, end)

			# swap between the ping array and pong array after all operations are complete
			self.pingCurrent = not self.pingCurrent

			runLength *= 2

		return self.getCurrentArray()



ourMS = mergeSorter([17,16,13,12,9,3,12,34,65,12,34,76,8,12,31,4])

print("before:")
print(ourMS.getCurrentArray())

ourMS.mergeSort2()

print()
print("after:")
print(ourMS.getCurrentArray())

