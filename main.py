from numpy import pi
from objects import functions, plotters, runners, transforms


xy_ranges = [
	{
		"min": -2,
		"max": 2,
		"segments": 160,
	},
	{
		"min": -2,
		"max": 2,
		"segments": 160,
	},
]

'''
data_file = "mandelbrot_2pi_xy.json"
video_file_directory = "mandelbrot_videos_2pi_xy"

rotations = {
	"segments": 720,
	"transforms": [
		{
			"min": 0,
			"max": 2 * pi,
			"transform": transforms.rotate_around_x_y
		},
	],
}
'''

'''
'''
#data_file = "mandelbrot_2pi_xw_2pi_yz.json"
data_file = "cubic_2pi_xw_2pi_yz.json"

#video_file_directory = "mandelbrot_videos_2pi_xw_2pi_yz"
video_file_directory = "complex_cubic_videos_2pi_xw_2pi_yz"
video_file_directory = "videos"

#file_label = "mandelbrot"
file_label = "cubic"

rotations = {
	"segments": 720,
	"transforms": [
		{
			"min": 0,
			"max": 2 * pi,
			"transform": transforms.rotate_around_x_zj
		},
		{
			"min": 0,
			"max": 2 * pi,
			"transform": transforms.rotate_around_y_zr
		},
	],
}

basis_vectors = [
	[1, 1, 0, 0],
	[0, 0, 1, 0],
	[0, 0, 0, 1],
	[1, 0, 0, 0],
]

output_element = 2


def main():
	# Main function for this script


	# If desired, un-comment this code block to run a transform and write the data
	'''
	#fr = runners.FunctionRunner(functions.mandelbrot(2, 250))
	fr = runners.FunctionRunner(functions.complex_cubic(1, 2, -1, 0, 0.75))
	#fr = runners.FunctionRunner(functions.complex_square())
	fr.compute_points(xy_ranges)
	fr.animate_rotation(rotations)
	#fr.animate_rotation(rotations, basis_vectors)
	fr.write("animation_frames", data_file)
	'''

	# If desired, un-comment this code bloc to generate a group of transform animations shown from various angles
	'''
	'''
	fp = plotters.FunctionPlotter(input_file=data_file, color_scheme="rainbow")
	for elevation in range(0, 91, 5):
		for azimuth in range(0, 91, 5):
			fp.write_video(True, output_element, None, f"{video_file_directory}/cubic_{str(elevation).zfill(2)}_{str(azimuth).zfill(2)}.mp4", elevation, -azimuth,  -45, 30)


if (__name__ == "__main__"):
	# This file was called directly as a script, not imported as a library, run its main function
	main()
