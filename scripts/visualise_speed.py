#!/usr/bin/env python
##########
# Demonstration of the VTK sww Visualiser
# Jack Kelly
# September 2006
##########

# Import the offline visualiser
from anuga.visualiser import OfflineVisualiser
from vtk import vtkCubeAxesActor2D
from Numeric import sqrt

o = OfflineVisualiser("domain.sww")


# Specify the height-based-quantities to render.
# Remember to set dynamic=True for time-varying quantities
o.render_quantity_height("elevation", zScale=0.0, offset = 0.0, opacity=0.5, dynamic=False)
o.render_quantity_height("stage", zScale=100.0, dynamic=True)

# Colour the stage:
o.colour_height_quantity('stage', (lambda q:q['stage'], -0.5, 0.5))
#o.colour_height_quantity('stage', (0.0,0.0, 0.5))

#o.colour_height_quantity('stage', (lambda q:sqrt(((q['xmomentum']/(q['stage']-q['elevation'])) ** 2) +
#                                             ((q['ymomentum']/(q['stage']-q['elevation'])) ** 2)), 0, 0.5))

# Start the visualiser (in its own thread).
o.start()

# Wait for the visualiser to terminate before shutting down.
o.join()
