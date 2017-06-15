import argparse

from src.particles import Particle

__author__ = 'goddess'

def parse_args():
    parser = argparse.ArgumentParser(description='Running the particle simulation.')
    parser.add_argument('-o', '--sim_out', help='The output file path from the gimel simulation', default='')
    parser.add_argument('-p', '--particle', help='Particle name', required=True)
    return parser.parse_args()

def separate_particles(file_name):
    with open(file_name, 'r') as f:
        text = f.read()
        data_start_point = text.find("initiate random event generator")
        particles = text[data_start_point:].split(particle)[1:]
    return particles

def parse_output_naively(file_name, particle):
    particles = separate_particles(file_name)
    with open("{0}_data.txt".format(particle), 'w') as fout:
        fout.write('momentum[GeV]\tkappa\tkappa_err\ttandip\ttandip_err\tPH\n')
        for p in particles:
            lines = p.split('\n')
            p = lines[0].strip()
            ph = 0
            if '    NO.  PULSE HEIGHT      X              Y              Z        YWIDTH  ZWIDTH' in lines:
                ph_line = 1 + lines.index(
                    '    NO.  PULSE HEIGHT      X              Y              Z        YWIDTH  ZWIDTH')
                ph = lines[ph_line].strip()[2:].strip().split(' ')[0]

            kappa = 0
            tandip = 0
            kappa_err = 0
            tandip_err = 0
            if ' *                             Fit Parameters                              *' in lines:
                kappa_line = 1 + lines.index(
                    ' *                             Fit Parameters                              *')
                tandip_line = kappa_line + 3
                kappa = lines[kappa_line][2:].strip().split(' ')[0]
                tandip = lines[tandip_line][2:].strip().split(' ')[0]
                kappa_err_line = 1 + lines.index(' *                             Fit Error Matrix  ')
                tandip_err_line = kappa_err_line + 3
                kappa_err = lines[kappa_err_line].split(' ')[-1]
                tandip_err = lines[tandip_err_line].split(' ')[-1]
            fout.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\n".format(p, kappa, kappa_err, tandip, tandip_err, ph))

        print "Number of particles injected: {0}".format(len(particles))

def extract_particles(file_name):
    particles = []
    particles_text = separate_particles(file_name)
    for particle in particles_text:
        data = {}
        #data['']
        particles.append(Particle())
    return particles

if __name__ == "__main__":
    args = parse_args()
    particle = args.particle
    output_file_name = args.sim_out
    if not output_file_name:
        output_file_name = particle + '_out.txt'
    parse_output_naively(output_file_name, particle)