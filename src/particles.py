class Particle(object):
    def __init__(self, **kwargs):
        self.p_initial = kwargs.get('p_initial')
        self.tandip = kwargs.get('tandip')
        self.kappa = kwargs.get('kappa')
        self.tandip_err = kwargs.get('tandip_err')
        self.kappa_err = kwargs.get('kappa_err')
        self.ph = kwargs.get('ph')
        self.ms_x = kwargs.get('ms_x')
        self.ms_y = kwargs.get('ms_y')
        self.ms_z = kwargs.get('ms_z')
        self.ms_dx = kwargs.get('ms_dx')
        self.ms_dy = kwargs.get('ms_dy')
        self.ms_dz = kwargs.get('ms_dz')
        self.emc_x = kwargs.get('emc_x')
        self.emc_y = kwargs.get('emc_y')
        self.emc_z = kwargs.get('emc_z')
        self.emc_dx = kwargs.get('emc_dx')
        self.emc_dy = kwargs.get('emc_dy')
        self.emc_dz = kwargs.get('emc_dz')
        self.phi = kwargs.get('phi')
        self.dphi = kwargs.get('dphi')

class Event(object):
    def __init__(self, particles):
        self.num = len(particles)
        self.particles = particles

# class K0sEvent(Event):
#     def __init__(self, particles):
#         super.__init__(particles)
