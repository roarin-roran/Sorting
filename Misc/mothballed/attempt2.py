import sorterManager
import math

class attempt2:
	# * * * * * * * * * * * * * *
	# * * * * * SORTERS * * * * *
	# * * * * * * * * * * * * * *
	def mergeSort2(self):
		print("first make an input, parameters should be passed when the sorter is created")
		print()

		self.output = self.input.copy()

		mergeUnit = 1

		while mergeUnit < len(self.input):
			for i in range(math.ceil(len(self.input)/(2*mergeUnit))):
				print("before (ms2 loop)", self.output[(2*mergeUnit*i):(2*mergeUnit*i)+mergeUnit], self.output[(2*mergeUnit*i)+mergeUnit:(2*mergeUnit*i)+2*mergeUnit])
				print(self.output)



				leftInput = self.output[2*mergeUnit*i:mergeUnit*(2*i + 1)]
				rightInput = self.output[mergeUnit*(2*i+1):2*mergeUnit*(i+1)]

				self.output[2*mergeUnit*i:2*mergeUnit*(i+1)] = self.merge2(leftInput, rightInput)



				print("after (ms2 loop)", self.output[(2*mergeUnit*i):(2*mergeUnit*i)+mergeUnit], self.output[(2*mergeUnit*i)+mergeUnit:(2*mergeUnit*i)+2*mergeUnit])
				print(self.output)

				print()

			mergeUnit *= 2


	# * * * * * * * * * * * * * * * * * *
	# * * * * * SUPPORT METHODS * * * * *
	# * * * * * * * * * * * * * * * * * *
	@staticmethod
	def merge2(leftInput, rightInput):
		output = []

		print("m2 before", leftInput, rightInput, output)

		while len(leftInput) > 0 and len(rightInput) > 0:
			if leftInput[0] <= rightInput[0]:
				output.append(leftInput.pop(0))
			else:
				output.append(rightInput.pop(0))

		output += leftInput
		output += rightInput

		print("m2 after ", leftInput, rightInput, output)

		return output



	


ourMS = attempt2()
ourMS.input = [77,1,65,34,5,7,3,23,47]

ourMS.mergeSort2()


