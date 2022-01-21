import random

# 1. fiddle with statistics to stop everything in a run from getting high - chance of run terminating based on run length and size
# 2. slice by reference instead of copying

class sorterManager:
	def generateInput(self, sizePower, sortedRunLengthPower, unsortedRunLengthPower):
		self.input = []
		self.inputLength = 10**sizePower

		runNext = random.choice([True, False])

		#print(runNext)

		while len(self.input) < self.inputLength:
			if runNext:
				runLength = int(random.random()*10**sortedRunLengthPower)
				#print("add a run, length =", runLength)
			else:
				runLength = int(random.random()*10**unsortedRunLengthPower)
				#print("add some randomly ordered stuff, length =", runLength)

			newPortion = []

			while len(newPortion) < runLength:
				newChar = int(random.random()*self.inputLength)
				if len(newPortion) == 0:
					newPortion.append(newChar)
				elif newChar >= newPortion[-1] or not runNext:
					newPortion.append(newChar)

			#print(newPortion)
			self.input += newPortion
			#break

		print(self.input)

	def mergeSort2(self):
		self.wIP = []

		# partition the input
		for i in self.input:
			self.wIP.append([i])

		print(self.wIP)

		# loop over itterative rounds
		while len(self.wIP) > 1:
			# loop through input
			i = 0
			while i < len(self.wIP):
				if len(self.wIP) - i >= 2:
					print(self.wIP[i], self.wIP[i+1])
					
					leftInput = self.wIP.pop(i)
					rightInput = self.wIP.pop(i)

					self.wIP.insert(i, self.merge2([leftInput, rightInput]))
				elif len(self.wIP) - i == 1:
					print(self.wIP[i])

				i += 1

			print(self.wIP)
			#input()

	def mergeSort3(self):
		self.wIP = []

		# partition the input
		for i in self.input:
			self.wIP.append([i])

		print(self.wIP)

		# loop over itterative rounds
		while len(self.wIP) > 1:
			# loop through input
			i = 0
			while i < len(self.wIP):
				if len(self.wIP) - i >= 3:
					print(self.wIP[i], self.wIP[i+1], self.wIP[i+2])
					
					leftInput = self.wIP.pop(i)
					centreInput = self.wIP.pop(i)
					rightInput = self.wIP.pop(i)

					self.wIP.insert(i, self.merge3([leftInput, centreInput, rightInput]))
				elif len(self.wIP) == 2:
					print("handle the thing")
					print(self.wIP)
					print("sections to merge:", len(self.wIP))
					#return self.wIP
					
					self.wIP = [self.merge2(self.wIP)]
					print("after:")
					print(self.wIP)
					break


				i += 1

		print()
		print("sorted array:")
		print(self.wIP[0])
		return self.wIP

	def mergeSort4(self):
		self.wIP = []

		# partition the input
		for i in self.input:
			self.wIP.append([i])

		print(self.wIP)

		# loop over itterative rounds
		while len(self.wIP) > 1:
			# loop through input
			i = 0
			while i < len(self.wIP):
				if len(self.wIP) - i >= 4:
					print(self.wIP[i], self.wIP[i+1], self.wIP[i+2], self.wIP[i+3])
					
					leftInput = self.wIP.pop(i)
					centreLeftInput = self.wIP.pop(i)
					centreRightInput = self.wIP.pop(i)
					rightInput = self.wIP.pop(i)

					self.wIP.insert(i, self.merge4([leftInput, centreLeftInput, centreRightInput, rightInput]))
				elif len(self.wIP) == 2:
					print("handle the thing")
					print(self.wIP)
					print("sections to merge:", len(self.wIP))
					#return self.wIP
					
					self.wIP = [self.merge2(self.wIP)]
					print("after:")
					print(self.wIP)
					break


				i += 1

		print()
		print("sorted array:")
		print(self.wIP[0])
		return self.wIP

	



	@staticmethod
	def merge2(mergeInput):
		output = []

		while len(mergeInput[0]) > 0 and len(mergeInput[1]) > 0:
			print("merge:", mergeInput[0][0], "and", mergeInput[1][0])

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

		print(output)
		print()

		return output

	# not the best implementation - uses tripple comparison instead of 2 uses of merge2
	@staticmethod
	def merge3(mergeInput):
		output = []

		while len(mergeInput[0]) > 0 and len(mergeInput[1]) > 0 and len(mergeInput[2]) > 0:
			print("merge:", mergeInput[0][0], "and", mergeInput[1][0], "and", mergeInput[2][0])

			if mergeInput[0][0] <= mergeInput[1][0] and mergeInput[0][0] <= mergeInput[2][0]:
				output.append(mergeInput[0].pop(0))
			elif mergeInput[1][0] <= mergeInput[0][0] and mergeInput[1][0] <= mergeInput[2][0]:
				output.append(mergeInput[1].pop(0))
			else:
				output.append(mergeInput[2].pop(0))

		# only one array can be empty, so merge the two remaining arrays
		
		print("current input:", output, mergeInput)

		for i in range(len(mergeInput)):
			if len(mergeInput[i]) == 0:
				mergeInput.pop(i)
				break

		print("after scrubbing:", output, mergeInput)

		output += sorterManager.merge2(mergeInput)

		print("plus the tail:", output)
		print()

		return output

	@staticmethod
	def merge4(mergeInput):
		output = []

		while len(mergeInput[0]) > 0 and \
		      len(mergeInput[1]) > 0 and \
		      len(mergeInput[2]) > 0 and \
		      len(mergeInput[3]) > 0:

			print("merge:", mergeInput[0][0], ",", mergeInput[1][0], ",", mergeInput[2][0], "and", mergeInput[3][0])

			print("continue from here")
			exit(0)

			if mergeInput[0][0] <= mergeInput[1][0] and mergeInput[0][0] <= mergeInput[2][0]:
				output.append(mergeInput[0].pop(0))
			elif mergeInput[1][0] <= mergeInput[0][0] and mergeInput[1][0] <= mergeInput[2][0]:
				output.append(mergeInput[1].pop(0))
			else:
				output.append(mergeInput[2].pop(0))

		# only one array can be empty, so merge the two remaining arrays
		
		print("current input:", output, mergeInput)

		for i in range(len(mergeInput)):
			if len(mergeInput[i]) == 0:
				mergeInput.pop(i)
				break

		print("after scrubbing:", output, mergeInput)

		output += sorterManager.merge2(mergeInput)

		print("plus the tail:", output)
		print()

		return output




ourSM = sorterManager()
ourSM.generateInput(2.73, 0.1, 0.6)
ourSM.mergeSort4()

print()
print("complete")
print("length:", len(ourSM.input))