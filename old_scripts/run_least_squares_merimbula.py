
from anuga.fit_interpolate.fit import fit_to_mesh_file
from anuga.file_conversion.xya2pts import xya2pts

alpha = 5
mesh_file = 'merimbula_10785.tsh'
xya_point_file = 'meri0.xya'
pts_point_file = 'meri0.pts'
mesh_output_file = 'merimbula_10785_%g.tsh'%alpha

print mesh_output_file

#xya2pts(xya_point_file)







fit_to_mesh_file(mesh_file, pts_point_file, mesh_output_file,
                     alpha=alpha, verbose= True,
                     expand_search = False,
                     precrop = False)


from anuga import Domain
from anuga.abstract_2d_finite_volumes.pmesh2domain import pmesh_to_domain_instance


#-------
# Domain
filename = mesh_output_file
print 'Creating domain from', filename
domain = pmesh_to_domain_instance(filename, Domain)
print "Number of triangles = ", len(domain)
