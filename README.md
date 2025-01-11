# Complex-Surface
Generates and graphs hyper-dimensional surfaces of complex functions

This python library was developed to give myself some practice generating the data for complex surfaces.  I then also gave it the ability to rotate that surface around any four-dimensional vector and generate a graph of that rotation's projection in to three dimensions.  Finally, it has the ability to create multiple graphs at different rotations and use those graphs as frames in a video.

The surface data generation and rotation has been split into a separate object from the graph/video generation.  This allows a surface's data set to be generated once and used to generate individual graphs or videos with differet color maps as desired.

The main.py script's main() method is messy and I make no apologies for it.  It got used as a sort of scratch pad, with things commented or un-commented as needed.
