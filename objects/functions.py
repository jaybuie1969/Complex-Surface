import numpy as np

from typing import Dict, List, Tuple, Union

def generate_orthonormal_bases(basis:List[List[Union[int, float]]], rotate_basis:Dict[str, Union[int, float, List[int]]], return_vector_set:bool=False) -> Union[np.ndarray, Tuple[np.ndarray, np.ndarray]]:
	"""
	This function starts with an initial basis and then generates a rotated set of orthonormal bases according to the other incoming parameter
	The rotation being done is a simple rotation around a subspace (point, line, plane, etc.)

	Parameters
	----------
	basis : List[List[Union[int, float]]]
		A simple list of lists, with each internal list being one vector and the entire object making up a basis vector set
	rotate_basis:Dict[str, Union[int, float, List[int]]]
		A Dict object containing the parameters to use for rotating the initial basis object to generate each orthonormal in the set of bases to be returned
		The Dict object contains the following parameters
		* rotate_vector - the vector in the initial basis that gets rotated for each rotation
		* rotate_elements - the elements in the vector being rotated that get transformed during each rotation
		* min - the starting angle of rotation
		* max - the ending angle of rotation
		* segments - the number of segments between the minimum angle and the maximum angle
	return_vector_set : bool, default False
		A boolean flag to indicate whether only the generated orthnormal bases should be returned, or also return the generated vector sets as well

	Returns
	-------
	np.ndarray :The computed set of orthonormal bases
	"""

	# Initialize a set of segments + 1 copies of the initial incoming basis vectors, these will be rotated as per the parameters in the rotate_basis argument
	# x segments need x+1 endpoints
	n = rotate_basis["segments"] + 1
	vector_set = np.repeat(np.array(basis).T[ : , : , np.newaxis], n, axis=2).astype(float)

	# Initialize the set of transforms with all zeros and then set the relevant values to one for the rotating vector's elements that are not being transformed
	transforms = np.zeros(vector_set.shape)
	for i in range(vector_set.shape[1]):
		if (i not in rotate_basis["rotate_elements"]):
			transforms[i, i] = np.ones(n)

	# Set an array up of rotation angles between the rotate_basis min and max parameters and use them to set the values of rotating vector's elements that are being transformed
	angles = np.linspace(rotate_basis["min"], rotate_basis["max"], rotate_basis["segments"] + 1)
	transforms[rotate_basis["rotate_elements"][0], rotate_basis["rotate_elements"][0]] = np.cos(angles)
	transforms[rotate_basis["rotate_elements"][0], rotate_basis["rotate_elements"][1]] = -np.sin(angles)
	transforms[rotate_basis["rotate_elements"][1], rotate_basis["rotate_elements"][0]] = np.sin(angles)
	transforms[rotate_basis["rotate_elements"][1], rotate_basis["rotate_elements"][1]] = np.cos(angles)

	# Iterate through the initialized set of basis vectors and apply the generated transforms to the vector being rotated
	for i in range(transforms.shape[2]):
		vector_set[ : , rotate_basis["rotate_vector"], i] = transforms[ : , : , i] @ vector_set[ : , rotate_basis["rotate_vector"], i]

	# Convert each basis in the rotated set into an orthonormal basis using Numpy's implementation of the Gramm-Schmidt method
	orthonormals = np.zeros(vector_set.shape)
	for i in range(vector_set.shape[2]):
		orthonormals[ : , : , i], r = np.linalg.qr(vector_set[ : , : , i])

	return orthonormals if (not return_vector_set) else (orthonormals, vector_set)


def simple_complex_square(*args) -> Tuple[np.array]:
	"""
	This function squares a set of complex numbers and returns the results

	Parameters
	----------
	*args (List[numpy.array]) : set of unnamed arguments that are all numpy.array objects
		This should be a set of two equal-sized numpy arrays of numbers,
		The first represents the real portion of the incoming real complex numbers
		The second represents a the imarginary portion of the incoming complex numbers
		If the numbr of unnamed prameters is not exactly two, no computation is done

	Returns
	-------
	Tuple[np.array]
		A tuple of two numpy arrays that consist of the squared inputs
		The first array is the real portion of the result
		The second array is the imaginary portin of the result
	"""

	result = None
	if (len(args) == 2):
		result = (args[0] + (1j * args[1])) ** 2

	return (np.real(result), np.imag(result), ) if (result is not None) else None


class mandelbrotWithLastBailout():
	bailout:Union[int, float] = None
	iterations_max:int = None

	def __init__(self, bailout:Union[int, float], iterations_max:int):
		self.bailout = bailout
		self.iterations_max = iterations_max

	def compute(self, *args) -> Tuple[np.array]:
		result = None

		if (len(args) == 2):
			args_set = (args[0] + (1j * args[1]))
			result = np.zeros(args_set.shape)

			for i in range(self.iterations_max):
				result = np.where((np.abs(result) < self.bailout) == True, (result**2) + args_set, result)

		return (np.real(result), np.imag(result), ) if (result is not None) else None



class mandelbrot():
	bailout:Union[int, float] = None
	iterations_max:int = None

	def __init__(self, bailout:Union[int, float], iterations_max:int):
		self.bailout = bailout
		self.iterations_max = iterations_max

	def compute(self, *args) -> Tuple[np.array]:
		result = None

		if (len(args) == 2):
			args_set = (args[0] + (1j * args[1]))
			result = np.zeros(args_set.shape)

			for i in range(self.iterations_max):
				result = np.where((np.abs(result) < self.bailout) == True, (result**2) + args_set, result)

		if (result is not None):
			result = np.where((np.abs(result) >= self.bailout) == True, (0 + 0j), result)

		return (np.real(result), np.imag(result), ) if (result is not None) else None


class complex_square():
	a:Union[int, float, complex] = None
	b:Union[int, float, complex] = None
	c:Union[int, float, complex] = None

	def __init__(self, a:Union[int, float, complex]=1, b:Union[int, float, complex]=0, c:Union[int, float, complex]=0):
		self.a = a
		self.b = b
		self.c = c

	def compute(self, *args) -> Tuple[np.array]:
		result = None

		if (len(args) == 2):
			arg_set = (args[0] + (1j * args[1]))
			result = (self.a * (arg_set ** 2)) + (self.b * arg_set) + self.c

		return (np.real(result), np.imag(result), ) if (result is not None) else None


class complex_cubic():
	a:Union[int, float, complex] = None
	b:Union[int, float, complex] = None
	c:Union[int, float, complex] = None
	d:Union[int, float, complex] = None
	offset:Union[int, float, complex] = None

	def __init__(self, a:Union[int, float, complex]=1, b:Union[int, float, complex]=0, c:Union[int, float, complex]=0, d:Union[int, float, complex]=0, offset:Union[int, float, complex]=0):
		self.a = a
		self.b = b
		self.c = c
		self.d = d
		self.offset = offset

	def compute(self, *args) -> Tuple[np.array]:
		result = None

		if (len(args) == 2):
			arg_set = (args[0] + (1j * args[1])) - self.offset
			result = (self.a * (arg_set ** 3)) + (self.b * (arg_set ** 2)) + (self.c * arg_set) + self.d

		return (np.real(result), np.imag(result), ) if (result is not None) else None
