from math import sqrt, cos, acos

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
    def __init__(self, emc_data, ms_data, ms_coords):
        self.emc_data = emc_data
        self.ms_data = ms_data
        self.ms_coords = ms_coords

class K0sEvent(Event):
    def is_pi_plus_minus(self):
        return (len(self.ms_data) == 3 or len(self.ms_data) == 2) and len(self.ms_coords) >= 1

    def get_ms_data_and_coords(self):
        if self.is_pi_plus_minus():
            phis = [coords[6] for coords in self.ms_coords]
            max_phi = max(phis)
            max_phi_index = phis.index(max_phi)
            # if len(self.ms_data) == 2:
            #     pass
            if max_phi_index == 0:
                # Track 1 and 2
                return (self.ms_data[0:2], self.ms_coords[max_phi_index])
            elif max_phi_index == 1:
                # Track 1 and 3
                return ([self.ms_data[0], self.ms_data[2]], self.ms_coords[max_phi_index])
            else:
                # Track 2 and 3
                return (self.ms_data[1:3], self.ms_coords[max_phi_index])
        return (self.ms_data, self.ms_coords)

    def get_mass(self):
        if self.is_pi_plus_minus():
            a1 = 9.946917 #cm
            da1 = 8.703541
            a2 = 523.073125 #cm/GeV
            da2 = 6.691826
            m1 = 139.57061 * 10**(-3) #GeV
            m2 = m1
            ms_data, coords = self.get_ms_data_and_coords()
            p1m = a1 + a2*float(ms_data[0][0])
            p1 = p1m * sqrt(float(ms_data[0][2])**2 + 1)
            p2m = a1 + a2 * float(ms_data[1][0])
            p2 = p2m * sqrt(float(ms_data[1][2])**2 + 1)
            phi = float(coords[6])
            return m1**2 + m2**2 + 2*sqrt((m1**2 + p1**2)*(m2**2+p2**2)) - 2*p1*p2*cos(phi)
        return 0

class Pi0Event(Event):
    def is_gamma_gamma(self):
        return len(self.ms_data) == 0 and len(self.emc_data) == 2

    def get_mass(self):
        if self.is_gamma_gamma():
            a1 = -15.38373
            a2 = 48.52774
            da1 =  2.989187
            da2 =  0.1122469
            m1 = 0  # GeV
            m2 = m1
            # emc_data: [ph, x, dx, y, dy, z, dz]
            p1 = a1 + a2 * float(self.emc_data[0][0])
            p2 = a1 + a2 * float(self.emc_data[1][0])
            ax = float(self.emc_data[0][1])
            bx = float(self.emc_data[1][1])
            ay = float(self.emc_data[0][3])
            by = float(self.emc_data[1][3])
            az = float(self.emc_data[0][5])
            bz = float(self.emc_data[1][5])
            adotb =  ax * bx + ay * by + az * bz
            absa = sqrt( ax * ax + ay * ay + az * az )
            absb = sqrt( bx * bx + by * by + bz * bz )
            phi = acos( adotb / (absa * absb) )
            return m1 ** 2 + m2 ** 2 + 2 * sqrt((m1 ** 2 + p1 ** 2) * (m2 ** 2 + p2 ** 2)) - 2 * p1 * p2 * cos(phi)
        return 0

