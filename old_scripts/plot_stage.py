#!/usr/bin/env python

# Import the offline visualiser
from anuga.visualiser import OfflineVisualiser
from numpy import sqrt
import sys

if len(sys.argv) > 1:
   sww_filename = sys.argv[1]
else:    
   sww_filename =raw_input('Input sww filename:\n')

vis = OfflineVisualiser(sww_filename)

# Specify the height-based-quantities to render.
# Remember to set dynamic=True for time-varying quantities
vis.render_quantity_height("elevation", zScale=100.0, offset = 5.0, opacity=1, dynamic=False)
vis.render_quantity_height("stage", zScale=100.0, dynamic=True,opacity=0.3)

# Colour the stage:
vis.colour_height_quantity('stage', (lambda q:q['stage'], -0.5, 0.5))

#vis.colour_height_quantity('stage', (lambda q:sqrt(((q['xmomentum']/(q['stage']-q['elevation'])) ** 2) +
#                                             ((q['ymomentum']/(q['stage']-q['elevation'])) ** 2)), 0, 0.5))

# Start the visualiser (in its own thread).
vis.start()

# Wait for the visualiser to terminate before shutting down.
vis.join()
