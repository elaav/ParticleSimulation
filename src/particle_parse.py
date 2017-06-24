import argparse
import re

from particles import Event, K0sEvent, Pi0Event

__author__ = 'goddess'

def parse_args():
    parser = argparse.ArgumentParser(description='Running the particle simulation.')
    parser.add_argument('-o', '--sim_out', help='The output file path from the gimel simulation', default='')
    parser.add_argument('-p', '--particle', help='Particle name', required=True)
    return parser.parse_args()

def separate_events(file_name, particle):
    with open(file_name, 'r') as f:
        text = f.read()
        data_start_point = text.find("initiate random event generator")
        particles = text[data_start_point:].split(particle)[1:]
    return particles

def parse_output_naively(file_name, particle):
    # assuming one particle per event
    particles = separate_events(file_name, particle)
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

def event_type_factory(particle):
    if particle == 'k-short':
        return K0sEvent
    elif particle == 'pi-0':
        return Pi0Event
    else:
        return Event

def parse_ms_coords(lines):
    ms_coords = []
    current_lines = lines
    while '              ====================' in current_lines:
        coord_line = 2 + current_lines.index('              ====================')
        # [x, dx, y, dy, z, dz, phi, dphi, [tracks]]
        ms_coords.append([
            current_lines[coord_line].split()[2],
            current_lines[coord_line].split()[4],
            current_lines[coord_line + 1].split()[2],
            current_lines[coord_line + 1].split()[4],
            current_lines[coord_line + 2].split()[2],
            current_lines[coord_line + 2].split()[4],
            current_lines[coord_line + 4].split()[1],
            current_lines[coord_line + 4].split()[3],
            [int(current_lines[coord_line - 3].split()[1]), int(current_lines[coord_line - 3].split()[3])],
        ])

        current_lines = current_lines[coord_line + 4:]
    return ms_coords

def parse_ms_data(lines):
    ms_data = []
    current_lines = lines
    while ' *                             Fit Parameters                              *' in current_lines:
        kappa_line = 1 + current_lines.index(
            ' *                             Fit Parameters                              *')
        tandip_line = kappa_line + 3
        kappa_err_line = 1 + current_lines.index(' *                             Fit Error Matrix  ')
        tandip_err_line = kappa_err_line + 3

        # [kappa, kappa_err, tandip, tandip_err]
        ms_data.append([
            current_lines[kappa_line].split()[1],
            current_lines[kappa_err_line].split()[-1],
            current_lines[tandip_line].split()[1],
            current_lines[tandip_err_line].split()[-1],
        ])

        current_lines = current_lines[tandip_err_line+1:]
    return ms_data

def parse_emc_data(lines):
    emc_data = []
    if '    NO.  PULSE HEIGHT      X              Y              Z        YWIDTH  ZWIDTH' in lines:
        ph_line = 1 + lines.index(
            '    NO.  PULSE HEIGHT      X              Y              Z        YWIDTH  ZWIDTH')
        while re.match('     \d', lines[ph_line]):
            splitted_data = lines[ph_line].strip()[2:].strip().split()
            # [ph, x, dx, y, dy, z, dz]
            emc_data.append([splitted_data[0],
                             splitted_data[1],
                             splitted_data[2][3:],
                             splitted_data[3],
                             splitted_data[4][3:],
                             splitted_data[5],
                             splitted_data[6][3:],
                             ])
            ph_line += 1
    return emc_data

def extract_events(file_name, particle):
    events = []
    events_text = separate_events(file_name, particle)
    EventType = event_type_factory(particle)
    for event in events_text:
        lines = event.split('\n')
        # Pulse Height
        emc_data = parse_emc_data(lines)
        # Kappa and tandip
        ms_data = parse_ms_data(lines)
        # Final coordinates of the vertex
        ms_coords = parse_ms_coords(lines)

        events.append(EventType(emc_data, ms_data, ms_coords, event))
    return events

def get_mass(files_list, particle):
    events = []
    for file_name in files_list:
        events += (extract_events(file_name, particle))
    events = [event for event in events if event.is_main_chain()]
    mass = []
    for event in events:
        mass.append(event.get_mass())
    return mass

def get_k0s_output(files_list, output_file=None):
    events = []
    particle = 'k-short'
    for file_name in files_list:
        events += (extract_events(file_name, particle))
    events = [event for event in events if event.is_main_chain()]
    if not output_file:
        output_file = "{0}_data.txt".format(particle)
    with open(output_file, 'w') as fout:
        fout.write('Event\t\tkappa[cm]\t\tkappa_err[cm]\t\ttandip\t\ttandip_err\t\tphi[rad]\n')
        i = 1
        for event in events:
            ms_data, coords = event.get_ms_data_and_coords()
            fout.write("{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}\n".format(
                i,
                ms_data[0][0],
                ms_data[0][1],
                ms_data[0][2],
                ms_data[0][3],
                coords[6]
            ))
            fout.write("{0}\t\t{1}\t\t{2}\t\t{3}\t\t{4}\t\t{5}\n".format(
                i,
                ms_data[1][0],
                ms_data[1][1],
                ms_data[1][2],
                ms_data[1][3],
                coords[6]
            ))
            i += 1

if __name__ == "__main__":
    args = parse_args()
    particle = args.particle
    output_file_name = args.sim_out
    if not output_file_name:
        output_file_name = particle + '_out.txt'
    parse_output_naively(output_file_name, particle)