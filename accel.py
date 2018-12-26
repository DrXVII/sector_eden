#!/bin/python3

import sys

earth_g = 9.8 #meters per second
k_earth_g = 1000*earth_g
m_earth_g = 1000*k_earth_g

km = 1000
au = km*(1.496e+8)

sec = 1
minute = sec*60
hour = minute*60
day = hour*24

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == '-i' or sys.argv[1] == '--interactive_mode':
            accel, max_time, desired_dist, print_amt = interactive_input()
    elif len(sys.argv) == 6:
        if sys.argv[1] == '-c' or sys.argv[1] == '--command_mode':
            accel, max_time, desired_dist, print_amt = get_cli_params()
    elif len(sys.argv) > 1:
        print('incorrect number of arguments provided')
        exit()
    else:
        print('using default parameters')
        accel = 10*k_earth_g
        max_time = 2*hour
        desired_dist = 3*au
        #desired_dist = 100*au
        print_amt = 30

    speed, dist, time_taken = traveltime_calc(desired_dist, accel, max_time, print_amt)

    print('\n*** SUMMARY ***')
    print('time taken: {:02}:{:02}:{:02} ({:.2f}d)'.format(int(time_taken/hour), int(time_taken % hour / minute), int(time_taken % minute / sec), time_taken/day))
    print('speed reached: {:.2f}km/s'.format(speed/km))
    print('distance travelled: {:.0f}km ({:.6f}au)'.format(dist/km, dist/au))
    print('acc: {:.2f}g'.format(accel/earth_g))

    if dist < desired_dist: print("WARNING: Failed to reach target in time")

#print_amt - how many lines to print of the intermediate calculations
def traveltime_calc(desired_dist, accel, max_time, print_amt):
    speed = 0
    dist = 0
    time_taken = 0

    print_interval = max_time / print_amt

    for i in range(0, max_time):
        speed += accel
        dist += speed

        if (i+1) % print_interval == 0:
            time_taken = i + 1
            time_str = "{:02}:{:02}:{:02}".format(int(time_taken/hour), int(time_taken % hour / minute), int(time_taken % minute / sec), time_taken/day)
            print('t:{} s:{:.4f}km/s d:{:.2f}km (au: {:.6f})'.format(time_str, speed/km, dist/km, dist/au))

        if desired_dist != 0 and dist*2 >= desired_dist:
            time_taken = i + 1
            break

    max_speed = speed
    dist *= 2
    time_taken *=2
    return speed, dist, time_taken

def interactive_input():
    accel = float(input('input acceleration in Gs: ')) * earth_g
    max_time = int(float(input('input max time available in hours: ')) * hour)
    desired_dist = float(input('input desired distance in AUs: ')) * au
    print_amt = 30

    return accel, max_time, desired_dist, print_amt

def get_cli_params():
    accel        = float(sys.argv[2]) * earth_g
    max_time     = int(float(sys.argv[3]) * hour)
    desired_dist = float(sys.argv[4]) * au
    print_amt    = float(sys.argv[5])
            
    return accel, max_time, desired_dist, print_amt

main()
