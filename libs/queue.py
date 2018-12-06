class queue():

	def __init__(self):
		self.elements = []

	def enqueue(self, data):
		self.elements.append(data)
		return True

	def dequeue(self):
		return self.elements.pop(0)
