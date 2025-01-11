# This library is intended to hold a set of different runners for functions, including being able to set up the initial blocks of parameters and handling the desire transformes

import json
import numpy as np
import os

from math import cos, sin
from pathlib import Path
from re import split
from typing import Any, Callable, Dict, List, Tuple, Union

class FunctionRunner:
	# This class is the first, generic runner for a function
	# It does not define the function, only a framework for running and transforming the desired function

	fn:Union[Callable, object] = None

	# By default, write any desired output to the following file
	default_output_directory:str = "./json/"
	output_file:Path = Path(f"{default_output_directory}output.json")

	ranges:List[Dict[str, float]] = None
	computed_points:Dict = None
	animation_frames:Dict = None

	def __init__(self, fn:Union[Callable, object], **kwargs) -> None:
		"""
		Parameters
		----------
		fm : Callable
			The function that will be used by this function runner instance
		**kwargs : Dict[str, Any]
			A set of configuration parmeters in parameter name: value format
			Right now, the only useful configuration parameter is the output file to which computed data would be written

		Returns
		-------
		None
			The __inti__ method does not return anything
		"""

		self.fn = fn

		if (("output_file" in kwargs) and (kwargs["output_file"] != "")):
			output_file = self.check_file_path(kwargs["output_file"])
			if (output_file is not None):
				self.output_file = output_file

	def check_file_path(self, file_name:str) -> Path:
		"""
		This function checks to make sure a file_name is a valid path
		The file itself does not have to exist, but the directory path leading to it does

		Parameters
		----------
		file_name : str
			The intended full path (including directory if not using the default directory) for the intended file path

		Returns
		-------
		pathlib.Path : A full Python path generated from the incoming file name
			If file_name is None, an empty string or includes an invalid directory path, the returned value is None
		"""

		checked_file_name = None

		if ((file_name is not None) and (file_name != "")):
			# The file_name paramter is not None and not an empty string, check it

			file_list = split(r"/|\\", file_name)
			if (len(file_list) == 1):
				# file_name is only a file name without any directory path, place it in the default directory and set checked_file_ame
				checked_file_name = Path(self.default_output_directory + file_name)
			elif (os.path.isdir("/". join(file_list[0 : -1]))):
				# file_name includes a valid directory path, set checked_file_name
				checked_file_name = Path(file_name)

		return checked_file_name

	def build_coordinates(self, ranges:List[Dict[str, float]]) -> Tuple[np.array]:
		"""
		This method takes in a set of ranges (start, end, number of segments in the range) and returns a numpy mesh grid of the generated coordinates
		The method is designed to take in N sets of ranges and return the appropriate mesh grid
		While two or three dimensions would be the norm, it can be more

		Parameters
		----------
		ranges : List[Dict[st, float]]
			A list of desired number ranges to use in the generated mesh grid
			Each dict in the list contains three key/value pairs:
				min : The low end of this range
				max : The high end o this range
				segments : The number of segments between the min and max (N segments means N + 1 points are used)

		Returns
		-------
		Tuple[np.array] : The generated mesh grid for the incoming ranges
		"""

		coordinates = None
		if (len(ranges) > 1):
			arrays = []
			for number_range in ranges:
				arrays.append(np.linspace(number_range["min"], number_range["max"], number_range["segments"] + 1))

			coordinates = np.meshgrid(*arrays)
		elif (len(ranges) == 1):
			# If only one range was passed in return a simple line space instead
			coordinates = np.linspace(number_range["min"], number_range["max"], number_range["segments"] + 1)

		return coordinates

	def compute_points(self, ranges:List[Dict[str, float]])->None:
		"""
		This method takes in the desired range of initial coordinate points and produces a numpy array of the full input / output coordinates

		Parameters
		----------
		ranges : List[Dictpstr, float]
			A list of desired number ranges to use in the generated mesh grid
			Each dict in the list contains three key/value pairs:
				min : The low end of this range
				max : The high end o this range
				segments : The number of segments between the min and max (N segments means N + 1 points are used)

		Returns
		-------
		None : The resulting computed points are saved within this object, not output
		"""

		coordinates:Tuple[np.array] = self.build_coordinates(ranges)
		if (coordinates is not None):
			# A set of initial coordinates was generated, run the function and save the computed points (initial coordinates and outputs)
			results:Tuple[np.array] = self.fn(*coordinates) if (callable(self.fn)) else self.fn.compute(*coordinates)

			if (results is not None):
				points_list = list(coordinates)
				for result in results:
					points_list.append(result)

				self.computed_points = {
					"ranges": ranges,
					"points": np.array(points_list)
				}

	def animate_rotation(self, rotations:Dict, basis_vectors:List[List]=None)->None:
		"""
		This method takes the points computed by this runner's function and then applies a given set of transforms to those points, rotating it around a set of angles
		speficied by the incoming rotations and basis_vectors objects
		This transforms are then saved as individual data frames, suitable for images or animations

		Parameters
		----------
		rotations : Dict
			The set of rotation parameters that will be performed on the points computed from the function run by this object
			The  object includes a value for the number of segments through which the rotation will be done and a list of transforms used for the rotations
			Each transform object includes a starting angle, an ending angle and a transformation matrix that will be appled at each step of the rotation
			All transformation matricies need to be square and have their dimensions match the length of each computed point vector
		basis_vectors : List[List], defaults to None
			An optional set of basis vectors that, if present, are converted to an orthonormal set and used as a projection for the animated frames
			The basis vectors need to be a square matrix or the same size as the rotation matrices in the rotations argument

		Returns
		-------
		None : The resulting transformed frames to data are saved within this object, not output
		"""

		if ((self.computed_points is not None) and (len(self.computed_points["points"].shape) > 0)):
			rotators = list()
			for i, rotation in enumerate(rotations["transforms"]):
				# Initialize the rotator for this transform
				rotators.append(np.zeros([len(rotation["transform"]), len(rotation["transform"][0]), rotations["segments"] + 1]))

				# Set a line of angles for this rotation and then iterate over every row and row element in the transform to build this rotator
				thetas = np.linspace(rotation["min"], rotation["max"], rotations["segments"] + 1)
				for j, row in enumerate(rotation["transform"]):
					for k, element in enumerate(row):
						# Each element is assumed to be either a string or a number, handle each type appropriately

						if (type(element) == str):
							if (element == "cos"):
								rotators[i][j, k, : ] = np.cos(thetas)
							elif (element == "-cos"):
								rotators[i][j, k, : ] = -np.cos(thetas)
							elif (element == "sin"):
								rotators[i][j, k, : ] = np.sin(thetas)
							elif (element == "-sin"):
								rotators[i][j, k, : ] = -np.sin(thetas)
							else:
								raise Exception(f"Invalid multiplier {multiplier} in transform at row {row_counter}, column {column_counter}")
						else:
							rotators[i][j, k, : ] = np.full(thetas.shape, np.float64(element))

			# Initialize the overall rotator that will be a composit set of all rotations
			composite_rotator = np.zeros(rotators[0].shape)

			# If a set of basis vectors have been passed into this method call and the size of the basis vector set matches that of the transforms from rotations,
			# convert the basis vector set into an orthonormal basis to use as a projection of this hyperdimensional space to a three-dimensional subspace
			orthonormal_basis = None
			has_orthonormal_basis = False
			if (
				(basis_vectors is not None)
				and (type(basis_vectors) == list)
				and (len(basis_vectors) == composite_rotator.shape[0])
				and (type(basis_vectors[0]) == list)
				and (len(basis_vectors[0]) == composite_rotator.shape[1])
			):
				orthonormal_basis, r = np.linalg.qr(np.array(basis_vectors))
				has_orthonormal_basis = True

			# Iterate over the desired number of rotation segments (plus one to include all endpoints) as the first step toward building the full compsite rotator object
			for i in range(rotations["segments"] + 1):
				frame_rotator = None

				# Now iterate over each rotator that has been built from the desired transforms in the incoming rotations argument and use those to build this single frame of the composite rotator
				for j, rotator in enumerate(rotators):
					if (j == 0):
						frame_rotator = rotator[ : , : , i]
					else:
						frame_rotator = frame_rotator @ rotator[ : , : , i]

				if (has_orthonormal_basis):
					# An orthonormal basis has been generated from the incoming basis_vectors argument, apply it to this rotator section
					frame_rotator = frame_rotator @ orthonormal_basis

				composite_rotator[ : , : , i] = frame_rotator

			# Initialize the object's set of animation frames before running the rotations
			self.animation_frames = dict()
			self.animation_frames["ranges"] = self.computed_points["ranges"]
			self.animation_frames["frames"] = np.empty(tuple((rotations["segments"] + 1, *self.computed_points["points"].shape)))

			# First, iterate over the composite rotator to apply each rotator frame to the computed points
			for i in range(composite_rotator.shape[-1]):

				# Next, iterate over the computed points' x-coordinate iterator position and y-coordinate iterator position (in that order) to get each computed point vector
				# Then apply the current rotator frame matirx to it and save the resulting vector in its appropriate animation frame
				for j in range(self.computed_points["points"].shape[-2]):
					for k in range(self.computed_points["points"].shape[-1]):
						self.animation_frames["frames"][i, : , j, k] = composite_rotator[ : , : , i] @ self.computed_points["points"][ : , j, k]

	def write(self, object_name:str, output_file:str=None):
		"""
		This method writes the specified generated data object to the specified output file

		Parameters
		----------
		object_name : str
			The name of the data object to be written, currently the only two valid values are "computed points" and "animation_frames"
		output_file : str
			Thr full path of the output file to which the data object will be written
			If it is not included in the method call, the object's default output file path will be used

		Returns
		-------
		None : A file will probably be saved, but the method itself returns nothing
		"""

		to_be_written = None

		# Make sure that a valid output file destination will be used
		output_file = self.check_file_path(output_file)
		if (output_file is None):
			output_file = self.output_file

		if (object_name == "computed_points"):
			if (self.computed_points is not None):
				# The computed points are being written and the object has been built, create a JSON-friendly version of the computed points
				to_be_written = dict()
				to_be_written["ranges"] = self.computed_points["ranges"]
				to_be_written["points"] = self.computed_points["points"].tolist()
			else:
				raise Exception("The computed_points object is empty and cannot be written")
				
		elif (object_name == "animation_frames"):
			if (self.animation_frames is not None):
				# The animation frames are being written and the object has been built, create a JSON-friendly version of the animation frames
				to_be_written = dict()
				to_be_written["ranges"] = self.animation_frames["ranges"]
				to_be_written["frames"] = self.animation_frames["frames"].tolist()
			else:
				raise Exception("The animation_frames object is empty and cannot be written")

		else:
			raise Exception("A valid computed object's name needs to be specified in order to write it out to a file")

		# If we have made it to this point without raising an exception, something should be ready to be written to the output file, write it out now
		if (to_be_written is not None):
			with open(output_file, "w") as f:
				json.dump(to_be_written, f, indent=4)
