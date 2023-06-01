import numpy as np

DEBUG_MODE = True
float_formatter = "{:.4f}".format
np.set_printoptions(formatter={'float_kind':float_formatter})

class QSystem:

	'''
	Quantum Qubit System Simulator
	Author: Abi Jebarson A
	This is a "Why not?" project on a simple quantum computer simulator with some basic gates and so many ways to go wrong.
	This is totally ideal meaning noiseless. So only intended for learning Quantum Computing basics. 
	You won't even be needing this for learning. I mean... there are so many advanced and quantum simulators out there. Use them if you want to learn.
	Use with caution. I do not do many error handling here.
	Currently Used Gates: X Y Z H
	'''

	# Might need... might not need.. idk
	sB = {'0':np.array([1.,0.]), '1':np.array([0.,1.])}
	hB = {'+':np.array([1.,1.])/np.sqrt(2), '1':np.array([1.,-1.])/np.sqrt(2)}
	nhB = {'+':np.array([1.,1j])/np.sqrt(2), '1':np.array([1.,-1j])/np.sqrt(2)}

	# Gates in Matrix form
	Xm = np.array([[0, 1], [1, 0]])
	Ym = np.array([[0, 1j], [-1j, 0]])
	Zm = np.array([[1, 0], [0, -1]])	
	Hm = (1/np.sqrt(2))*np.array([[1, 1], [1, -1]])	
	Im = np.eye(2)

	def __init__(self, qbn, cbn):
		self.qbn = int(qbn)
		self.cbn = int(cbn)
		self.qb = [self.sB['0']]*self.qbn # Used only for initial states.
		self.cb = [0]*self.cbn
		# This is the Joined n-Qubits that supports entanglement. i.e. ONE BIG VECTOR of 2^qbn
#Change JQB
		self.jqs = self.__multi_kronek(self.qb)
		if DEBUG_MODE: print(f'QSystem Created with {qbn} qubits and {cbn} classical bits.')

	def set_qstate(self, state, qn):
		'''
		Don't use this after initial stage.
		I mean... use it anytime. Nothing will happen after the initial state change.
		(I'm not gonna put any initial state check. You're on your own.)
		'''
		if (qn < self.qbn):
			temp = self.qb[qn]
			self.qb[qn] = state
			self.jqs = self.__multi_kronek(self.qb)
			if DEBUG_MODE: print(f"State at q{qn} changed from {temp} to {self.qb[qn]}")
		else:
			print(f"Qubit q{qn} doesn't exist ")

	def set_initstate(self, states):
		'''
		This method can be used to set all Initial states of qubits at once.
		Warning: Using this after initial state would override your previous entanglements and any gate transformations.
		If left without any state for an index, nothing will be done to that state.
		If this is the first time setting the initial state, it will be in ket 0 state.
		'states' can be given in 'tuple' or 'list' form. it will be converted to np.array anyways.
		'''
		for i in np.arange(qbn):
			self.qb[i] = np.array(states[i])
		self.jqs = self.__multi_kronek(self.qb)

	# SECTION: 1
	# This Section is for Mathematical stuff
	def __multi_kronek(self, states):
		'''
		assuming the 'states' to be in a python list
		'''
		if len(states)>=2:
			return np.kron(states.pop(0), self.__multi_kronek(states))
		else:
			return states[0]

	def __operate(self, gate, state):
		return gate.dot(state)
		# return gate.matmul(state)

	def operate_on_qn(self, gate, qn):
		'''
		Intended for internal use. Didn't make private since it can be useful for any external unitary transform.
		'''
		dummyNI = [self.Im]*self.qbn 
		dummyNI[qn] = gate
		final_operator = self.__multi_kronek(dummyNI)
		if DEBUG_MODE: print(f"Operating something... \n{final_operator}\n on \n{self.jqs}")
		self.jqs = self.__operate(final_operator, self.jqs)

	# SECTION: 2
	# This Section is for implementing the gates
	def x(self, qn):
		'''
		NOT Gate.
		Pauli X-Gate. 
		Rotates about the X-axis pi rad in the Bloch Sphere.
		'''
		self.operate_on_qn(self.Xm, qn)
		if DEBUG_MODE: print(f"X-gate Done - State: {self.jqs}")

	def y(self, qn):
		'''
		Pauli Y-Gate. 
		Rotates about the Y-axis pi rad in the Bloch Sphere.
		'''
		self.operate_on_qn(self.Ym, qn)
		if DEBUG_MODE: print(f"Y-gate Done - State: {self.jqs}")

	def z(self, qn):

		'''
		Pauli Z-Gate. 
		Rotates about the Z-axis pi rad in the Bloch Sphere.
		Almost identity transform, except it changes the sign of ket 1. 
		'''
		self.operate_on_qn(self.Zm, qn)
		if DEBUG_MODE: print(f"Z-gate Done - State: {self.jqs}")

	def h(self, qn):
		'''
		We can think about this as converting to Hadamard Basis. i.e. applies hadamard transformation.
		In bloch sphere, rotate the vector pi/2 rad about Y axis. Z (ket 0) goes to X (ket +)...etc
		This gives equal probability
		
		'''
		self.operate_on_qn(self.Hm, qn)
		if DEBUG_MODE: print(f"H-gate Done - State: {self.jqs}")

	def __str__(self):
		'''
		INFORMATION
		'''
		str_intro = "\nQuantum Qubit System:\n====================\n"
		str_qubit = f"\tQubits: {self.qbn}\n"
		str_clbit = f"\tClassical Bits: {self.cbn}\n"
		str_basis = f"\tBasis: {[np.base_repr(x, base=2, padding=(self.qbn if x==0 else int(self.qbn-len(str((np.base_repr(x, base=2))))))) for x in range(2**self.qbn)]}\n"
		str_curst = f"\tCurrent State:{self.jqs}\n" 
		str_curcb = f"\tClassical Bits:{self.cb}\n"
		return str_intro+str_qubit+str_clbit+str_basis+str_curst+str_curcb

qs = QSystem(3,3)

qs.h(0)

print(qs)