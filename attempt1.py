from time import time
import sorterManager

class attempt1:
	def __init__(self, input):
		self.input = input

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

		leftInput = attempt1.merge2([mergeInput.pop(0), mergeInput.pop(0)])

		output = attempt1.merge2([leftInput, mergeInput.pop(0)])

		return output

	# merges four inputs using merge2
	@staticmethod
	def merge4(mergeInput):
		output = []

		leftInput = attempt1.merge2([mergeInput.pop(0), mergeInput.pop(0)])
		rightInput = attempt1.merge2([mergeInput.pop(0), mergeInput.pop(0)])

		output = attempt1.merge2([leftInput, rightInput])

		return output




ourSM = sorterManager.sorterManager()
print("input")
input = ourSM.generateInput(5, 0.1, 0.6)
print(input)
print()

startTime = time()
ourA1 = attempt1(input)

print("output:")
print(ourA1.mergeSort2())
totalTime = time() - startTime
print("time cost:", totalTime)