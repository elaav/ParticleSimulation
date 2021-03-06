from subprocess import Popen, PIPE, STDOUT
import time
import argparse

__author__ = 'goddess'

def parse_args():
    #TODO add particles list
    parser = argparse.ArgumentParser(description='Running the particle simulation.')
    parser.add_argument('-o', '--output', help='Output file path', default='')
    parser.add_argument('-p', '--particle', help='Particle name', required=True)
    parser.add_argument('-n', '--num', help='Number of measurements', default=150, type=int)
    parser.add_argument('-s', '--sleep', help='Time to sleep between commands', default=0.3, type=float)
    parser.add_argument('-m', '--momentum', help='The initial particle momentum', default=4, type=float)
    return parser.parse_args()

def inject_particle(proc, particle, momentum, meas_num, sleep_time=0.3):
    print "Particle: {0}, p={1}GeV".format(particle, momentum)
    for i in xrange(meas_num):
        if (i + 1) % 100 == 0:
            print "{0}/{1} injected".format(i+1, meas_num)
        proc.stdin.write('{0} {1}\n'.format(particle, momentum))
        time.sleep(sleep_time)
        proc.stdin.write('inject\n')
        time.sleep(sleep_time)

def main():
    args = parse_args()
    particle = args.particle
    output_file_name = args.output
    if not output_file_name:
        output_file_name = particle + '_out.txt'
    num = args.num
    momentum = args.momentum
    sleep_time = args.sleep

    print "Initiating program..."
    
    with open(output_file_name, 'w') as f:
        p = Popen(['./gimel'], stdout=f, stdin=PIPE, stderr=STDOUT)
        p.stdin.write('1\n')
        time.sleep(1)
        # change only the magnetic field
        p.stdin.write('y\n')
        time.sleep(1)
        p.stdin.write('y\n')
        time.sleep(1)
        p.stdin.write('3\n')
        time.sleep(1)
        p.stdin.write('n\n')
        time.sleep(1)
        p.stdin.write('n\n')
        time.sleep(1)
        p.stdin.write('n\n')
        time.sleep(3)
        print "Starting injections"
        inject_particle(p, particle, momentum, num, sleep_time)
        time.sleep(1)
        p.stdin.write('exit\n')
        time.sleep(1)
        p.stdin.close()

    #print "Parsing the data..."
    #parse_output(output_file_name, particle)
    #print "The data table is in file '{0}'".format(particle + '_data.txt')
    print "You can enjoy your full data with the file '{0}':)".format(output_file_name)

if __name__ == "__main__":
    main()


