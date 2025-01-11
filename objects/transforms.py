rotate_around_x_y = [
	[1, 0, 0, 0],
	[0, 1, 0, 0],
	[0, 0, "cos", "-sin"],
	[0, 0, "sin", "cos"],
]

rotate_around_x_zr = [
	[1, 0, 0, 0],
	[0, "cos", 0, "-sin"],
	[0, 0, 1, 0],
	[0, "sin", 0, "cos"],
]

rotate_around_x_zj = [
	[1, 0, 0, 0],
	[0, "cos", "-sin", 0],
	[0, "sin", "cos", 0],
	[0, 0, 0, 1],
]

rotate_around_y_zr = [
	["cos", 0, 0, "-sin"],
	[0, 1, 0, 0],
	[0, 0, 1, 0],
	["sin", 0, 0, "cos"]
]

rotate_around_y_zj = [
	["cos", 0, "-sin", 0],
	[0, 1, 0, 0],
	["sin", 0, "cos", 0],
	[0, 0, 0, 1],
]

rotate_around_zr_zj = [
	["cos", "-sin", 0, 0],
	["sin", "cos", 0, 0],
	[0, 0, 1, 0],
	[0, 0, 0, 1],
]
