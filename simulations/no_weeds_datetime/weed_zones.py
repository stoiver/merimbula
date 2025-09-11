
import anuga

# Set default friction values
#   Sand bed
w = 0.01
#   Saltmarsh
g = 0.060
#   Paddle weed
y = 0.025
#   Eel grass
r = 0.035
#   Mangroves
c = 0.065
#   Strap weed
b = 0.040


#-------------------------------
# Setup Friction (due to weeds)
#-------------------------------
def image_points_to_northing_eastings(points):
    #print points
    n = len(points)

    z = []
    for i in range(n):
        #print i
        z.append([0,0])
        z[i][0] = 755471.4 + (points[i][0] + 3250.)/1.125
        z[i][1] = 5910260.0 + (points[i][1] + 1337.)/1.12

    return z

def set_friction_from_weed_zones(domain, weed_dir, location='centroids'):

    #-----------------------------------------------
    #   Set the whole region to a constant value
    #-----------------------------------------------
    weed_zoneall = image_points_to_northing_eastings([[-2269,-1337],[1894,-1339],[1894,2946],[-2669,2946]])

    #---------------------------------------
    #      Read friction polygon boundaries
    #---------------------------------------
    weed_zone47  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.047'),delimiter=' '))
    weed_zone2   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.002'),delimiter=' '))
    weed_zone12  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.012'),delimiter=' '))
    weed_zone35  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.035'),delimiter=' '))
    weed_zone8   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.008'),delimiter=' '))
    weed_zone10  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.010'),delimiter=' '))
    weed_zone13  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.013'),delimiter=' '))
    weed_zone15  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.015'),delimiter=' '))
    weed_zone19  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.019'),delimiter=' '))
    weed_zone18  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.018'),delimiter=' '))
    weed_zone24  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.024'),delimiter=' '))
    weed_zone26  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.026'),delimiter=' '))
    weed_zone27  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.027'),delimiter=' '))
    weed_zone32  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.032'),delimiter=' '))
    weed_zone31  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.031'),delimiter=' '))
    weed_zone33  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.033'),delimiter=' '))
    weed_zone34  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.034'),delimiter=' '))
    weed_zone36  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.036'),delimiter=' '))
    weed_zone37  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.037'),delimiter=' '))
    weed_zone38  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.038'),delimiter=' '))
    weed_zone40  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.040'),delimiter=' '))
    weed_zone41  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.041'),delimiter=' '))
    weed_zone42  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.042'),delimiter=' '))
    weed_zone43  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.043'),delimiter=' '))
    weed_zone44  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.044'),delimiter=' '))
    weed_zone45  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.045'),delimiter=' '))
    weed_zone46  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.046'),delimiter=' '))
    weed_zone1   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.001'),delimiter=' '))
    weed_zone20  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.020'),delimiter=' '))
    weed_zone21  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.021'),delimiter=' '))
    weed_zone22  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.022'),delimiter=' '))
    weed_zone23  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.023'),delimiter=' '))
    weed_zone25  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.025'),delimiter=' '))
    weed_zone16  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.016'),delimiter=' '))
    weed_zone17  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.017'),delimiter=' '))
    weed_zone3   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.003'),delimiter=' '))
    weed_zone6   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.006'),delimiter=' '))
    weed_zone7   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.007'),delimiter=' '))
    weed_zone9   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.009'),delimiter=' '))
    weed_zone4   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.004'),delimiter=' '))
    weed_zone39  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.039'),delimiter=' '))
    weed_zone28  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.028'),delimiter=' '))
    weed_zone29  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.029'),delimiter=' '))
    weed_zone30  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.030'),delimiter=' '))
    weed_zone5   = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.005'),delimiter=' '))
    weed_zone11  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.011'),delimiter=' '))
    weed_zone14  = image_points_to_northing_eastings(anuga.read_polygon(anuga.join(weed_dir,'weed_zone.014'),delimiter=' '))

    domain.set_quantity('friction',anuga.Polygon_function([  \
        (weed_zone15,  g), (weed_zone19, c), (weed_zone18, g), (weed_zone24, c), \
        (weed_zone26,  r), (weed_zone27, g), (weed_zone32, c), (weed_zone31, g), \
        (weed_zone33,  r), (weed_zone34, g), (weed_zone36, r), (weed_zone37, g), \
        (weed_zone38,  g), (weed_zone40, r), (weed_zone41, b), (weed_zone42, r), \
        (weed_zone43,  r), (weed_zone44, r), (weed_zone45, b), (weed_zone46, r), \
        (weed_zone1,   w), (weed_zone20, w), (weed_zone21, w), (weed_zone22, w), \
        (weed_zone23,  w), (weed_zone25, w), (weed_zone16, w), (weed_zone17, w), \
        (weed_zone3,   w), (weed_zone6,  w), (weed_zone7,  w), (weed_zone9,  w), \
        (weed_zone4,   b), (weed_zone39, b), (weed_zone28, r), (weed_zone29, b), \
        (weed_zone30,  b), (weed_zone5,  b), (weed_zone11, b), (weed_zone14, b) ]), \
        location=location)