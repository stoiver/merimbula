from anuga import plot_polygons, read_polygon


weed_zones = [
    "weed_zone.047",
    "weed_zone.002",
    "weed_zone.012",
    "weed_zone.035",
    "weed_zone.008",
    "weed_zone.010",
    "weed_zone.013",
    "weed_zone.015",
    "weed_zone.019",
    "weed_zone.018",
    "weed_zone.024",
    "weed_zone.026",
    "weed_zone.027",
    "weed_zone.032",
    "weed_zone.031",
    "weed_zone.033",
    "weed_zone.034",
    "weed_zone.036",
    "weed_zone.037",
    "weed_zone.038",
    "weed_zone.040",
    "weed_zone.041",
    "weed_zone.042",
    "weed_zone.043",
    "weed_zone.044",
    "weed_zone.045",
    "weed_zone.046",
    "weed_zone.001",
    "weed_zone.020",
    "weed_zone.021",
    "weed_zone.022",
    "weed_zone.023",
    "weed_zone.025",
    "weed_zone.016",
    "weed_zone.017",
    "weed_zone.003",
    "weed_zone.006",
    "weed_zone.007",
    "weed_zone.009",
    "weed_zone.004",
    "weed_zone.039",
    "weed_zone.028",
    "weed_zone.029",
    "weed_zone.030",
    "weed_zone.005",
    "weed_zone.011",
    "weed_zone.014",
]

print('Read weed zone polygons')
weed_polygons = {}
for zone in weed_zones:
    weed_polygons[zone] = read_polygon('../weed_zones/'+zone, delimiter=" ")

import pprint

#pprint.pprint(weed_polygons)


print('Convert to list of polygons')
weed_zones_polygons = []
for zone in weed_polygons:
    weed_zones_polygons.append(weed_polygons[zone])

#pprint.pprint(weed_zones_polygons)

print('plot weed polygons')
plot_polygons(weed_zones_polygons)
