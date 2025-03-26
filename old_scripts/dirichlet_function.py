class Dirichlet_Function(Boundary):
    """
    dirichlet function
    """


    def __init__(self, function=F, domain, verbose=False):
        import time
        from Numeric import array, zeros, Float
        from anuga.config import time_format
 

        Boundary.__init__(self)

        #Get x,y vertex coordinates for all triangles
        V = domain.vertex_coordinates

        #Compute midpoint coordinates for all boundary elements
        #Only a subset may be invoked when boundary is evaluated but
        #we don't know which ones at this stage since this object can
        #be attached to
        #any tagged boundary later on.

        if verbose: print 'Find midpoint coordinates of entire boundary'
        self.midpoint_coordinates = zeros( (len(domain.boundary), 2), Float)
        boundary_keys = domain.boundary.keys()


        xllcorner = domain.geo_reference.get_xllcorner()
        yllcorner = domain.geo_reference.get_yllcorner()        
        

        #Make ordering unique #FIXME: should this happen in domain.py?
        boundary_keys.sort()

        #Record ordering #FIXME: should this also happen in domain.py?
        self.boundary_indices = {}
        for i, (vol_id, edge_id) in enumerate(boundary_keys):

            base_index = 3*vol_id
            x0, y0 = V[base_index, :]
            x1, y1 = V[base_index+1, :]
            x2, y2 = V[base_index+2, :]
            
            #Compute midpoints
            if edge_id == 0: m = array([(x1 + x2)/2, (y1 + y2)/2])
            if edge_id == 1: m = array([(x0 + x2)/2, (y0 + y2)/2])
            if edge_id == 2: m = array([(x1 + x0)/2, (y1 + y0)/2])

            #Convert to absolute UTM coordinates
            m[0] += xllcorner
            m[1] += yllcorner
            
            #Register point and index
            self.midpoint_coordinates[i,:] = m

            #Register index of this boundary edge for use with evaluate
            self.boundary_indices[(vol_id, edge_id)] = i



        self.F = F
        self.domain = domain

        #Test
        q = self.F(0,self.midpoint_coordinates[0,:] )

        d = len(domain.conserved_quantities)
        msg = 'Values specified in function must be '
        msg += ' a list or an array of length %d' %d
        assert len(q) == d, msg


    def __repr__(self):
        return 'Dirichlet Function'


    def evaluate(self, vol_id=None, edge_id=None):
        """Return linearly interpolated values based on domain.time
	at midpoint of segment defined by vol_id and edge_id.
        """

        t = self.domain.time

        if vol_id is not None and edge_id is not None:
            i = self.boundary_indices[ vol_id, edge_id ]
            res = self.F(t, point_id = i)

            if res == NAN:
                x,y=self.midpoint_coordinates[i,:]
                msg = 'NAN value found in file_boundary at '
                msg += 'point id #%d: (%.2f, %.2f)' %(i, x, y)
                #print msg
                raise Exception, msg
            
            return res 
        else:
            #raise 'Boundary call without point_id not implemented'
            #FIXME: What should the semantics be?
            return self.F(t, self.midpoint_coordinates[i,:] ))



