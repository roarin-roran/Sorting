import math



# todo:
# 1. askSeb use a global variable to reduce changes to sinkingTime in popMin?
# 2. todo - add galloping mode


class tournamentTree:
	def __init__(self, inputArray, outputArray, runs):
		self.inputArray = inputArray
		self.outputArray = outputArray
		self.runs = runs

		self.numElements = self.runs[-1][1] - self.runs[0][0]



	# adds infinities to the end of each run, updating the run array
	def addInfs(self):
		# append infinity to the end of each run, updating the run start positions.
		j = 0
		for i in self.runs:
			i[0] += j
			i[1] += j

			self.inputArray.insert(i[1], math.inf)

			j += 1

	# removes the infinities from the end of runs, repairing the main array
	# the run array is NOT repaired - it shouldn't be needed after merging.
	def removeInfs(self):
		j = 0
		for i in self.runs:
			self.inputArray.pop(i[1] - j)

			j += 1


	# merges using a simple elementwise comparison - used for dev and as a baseline
	def simpleMerge(self):
		# overwritten portion of workingOutPos starts at the start of
		# the set of runs
		workingOutPos = self.runs[0][0]

		# while there are still runs
		while len(self.runs) > 1:
			# find the run with the smallest first index

			# initialise to the first run
			minRun = 0
			for i in range(len(self.runs) - 1):
				# if the first element is smaller, update it.
				if self.inputArray[self.runs[i+1][0]] < self.inputArray[self.runs[minRun][0]]:
					minRun = i + 1

			# move that element to the output
			self.outputArray[workingOutPos] = self.inputArray[self.runs[minRun][0]]
			workingOutPos += 1

			# increment position in this run
			self.runs[minRun][0] += 1

			# if the current and end pos of that run are now equal,
			# remove it from the list
			if self.runs[minRun][0] == self.runs[minRun][1]:
				self.runs.pop(minRun)

		# copy remaining run over - no need to pay the overheads of comparing 
		while self.runs[0][0] != self.runs[0][1]:
			self.outputArray[workingOutPos] = self.inputArray[self.runs[0][0]]
			self.runs[0][0] += 1
			workingOutPos += 1

# NOTE: stability condition is NOT written into tree, must be written into popMin
# askSeb - views on this

	# initiates the tHeap variable using the first value of each run
	def constructTHeap(self):
		# initialise heap with blank values - this declares a list that's the correct size (unless ints go over the standard max)
		# [run number, first element, position within the run]
		self.tHeap = [[0,0,0]]*len(self.runs)

		for nextGap in range(len(self.runs)):
			# define the element we're sinking
			sinkingElement = [nextGap, self.inputArray[self.runs[nextGap][0]],self.runs[nextGap][0]]
			
			# get the path to the next free space
			path = tournamentTree.getPath(nextGap)

			# for every element in the path
			for j in path:
				# if there's something in the slot
				if self.tHeap[j] != [0,0,0]:
					# see whether it's larger than what we're sinking
					# note that generation order enforces stability during heap creation
					if self.tHeap[j][1] > sinkingElement[1]:
						temp = self.tHeap[j]
						self.tHeap[j] = sinkingElement
						sinkingElement = temp
				# if there's nothing in the slot
				else:
					# add the element we're holding
					self.tHeap[j] = sinkingElement
					break


	# gets the path through a binary heap to a given gap
	@staticmethod
	def getPath(gap):
		# start at the bottom
		path = [gap]

		# find parents, until we reach the root
		while gap > 0:
			gap = math.floor(gap/2)
			path.append(gap)

		# flip and return
		path.reverse()
		return path

	def popMin(self):
		# askSeb add try catch here to deal with nonexistent tHeap?

		# element to be returned
		minElement = self.tHeap[0][1]
		# used to test for stability, if needed
		minElementOrigin = self.tHeap[0][0]

		# update the run that was popped from
		self.tHeap[0][2] += 1
		self.tHeap[0][1] = self.inputArray[self.tHeap[0][2]]

		# initialise with the first sinking step - first node only has one child
		parent = 0
		child  = 1
		sinkingTime = self.isFirstRunLarger(parent, child)
		
		# until sinking is complete
		while sinkingTime:
			# swap the parent and child
			temp = self.tHeap[parent]
			self.tHeap[parent] = self.tHeap[child]
			self.tHeap[child] = temp

			parent = child
			leftChild = 2*parent
			rightChild = 2*parent + 1

			# if the right right child exists, they both do
			if rightChild < len(self.tHeap):

				# returns true if second element is smaller - method needs renaming
				if self.isFirstRunLarger(leftChild, rightChild):
					child = rightChild
				else:
					child = leftChild

				# use the smaller child to work out whether you need to keep sinking
				sinkingTime = self.isFirstRunLarger(parent, child)
			# if the left child exists and the right doesn't, it is the smallest
			elif leftChild < len(self.tHeap):
				child = leftChild

				sinkingTime = self.isFirstRunLarger(parent, child)
			# if neither child exists, we're at the bottom
			else:
				sinkingTime = False

		return minElement, minElementOrigin


	# returns true iff firstRun is larger
	def isFirstRunLarger(self, firstRun, secondRun):
		# if elements aren't the same size, that decides the matter
		if self.tHeap[firstRun][1] > self.tHeap[secondRun][1]:
			return True
		# if they're the same size - use run number (stability criterion)
		elif self.tHeap[firstRun][1] == self.tHeap[secondRun][1]:
			if self.tHeap[firstRun][0] > self.tHeap[secondRun][0]:
				return True

		# default, if we haven't returned yet - return false
		return False


	# merges all entered runs
	def merge(self):
		# add infinities to the end of runs
		self.addInfs()

		# overwrite the output from the start of the first run onwards
		ourputArrayLocation = self.runs[0][0]

		# for all elements
		for i in range(self.numElements):
			# pop the minimum value from our heap, which will repair itself automatically
			self.outputArray[ourputArrayLocation] = self.popMin()[0]
			ourputArrayLocation += 1

		# remove the infinities from the ends of runs, because 
		self.removeInfs()

		return self.outputArray






#ourInput = [16,17,12,13,3,9,12,34,12,65,34,76,8,12,4,31]

#ourTT = tournamentTree(ourInput, ourInput.copy(), [[0,2],[2,4]])
#ourTT = tournamentTree(ourInput, ourInput.copy(), [[0,2],[2,4],[4,6]])
#ourTT = tournamentTree(ourInput, ourInput.copy(), [[0,2],[2,4],[4,6],[6,8]])
#ourTT = tournamentTree(ourInput, ourInput.copy(), [[0,2],[2,4],[4,6],[6,8],[8,10]])
#ourTT = tournamentTree(ourInput, ourInput.copy(), [[0,2],[2,4],[4,6],[6,8],[8,10],[10,12]])





#ourTT.simpleMerge()
#print(ourTT.outputArray)

#ourTT.constructTHeap()
#print(ourTT.tHeap)

#ourTT.merge()

#for i in range(12):
#	print(ourTT.popMin())

#print(ourTT.tHeap)
