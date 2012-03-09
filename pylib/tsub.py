#!/usr/bin/python
import multiprocessing as mp
import os
import time
import sys
from pprint import pprint

def run_command(cmd):
    #delegate command exit code to child exit code
    ret = os.system(cmd)
    #os.system high 8 bit is the exit code where the first bit is coredump status
    #see doc for os.system
    ec = ret >> 8 & ~(1<<7)
    #we don't use this but just in case when we need them
    #core = (ret >> 8 & (1<<7)) == 0
    #killsig = ret & 0x11111111
    sys.exit(ec)

def run(jobs,maxjob=None,poll_interval=1.0):
    maxjob = mp.cpu_count() if maxjob is None else maxjob
    processes = [mp.Process(target=run_command,args=(j,)) for j in jobs if not j.startswith('#')]
    jobleft = range(len(processes))
    running = set()
    finished = []
    exitcodes = [ 0 for x in processes ]
    while len(finished) < len(processes):
        #we can submit more job and there are more jobs to run
        if len(running) < maxjob and len(jobleft):
            to_run = jobleft.pop(0)
            processes[to_run].start()
            running.add(to_run)
            print 'Submit: '+str(to_run)
        
        for p_index in list(running): #check if the process finished
            process = processes[p_index]
            if not processes[p_index].is_alive():#process finished
                #remove from running add to finished and write exit code
                running.remove(p_index)
                finished.append(p_index)
                process.join()
                exitcode = process.exitcode
                if exitcode is None: print 'No it should not reach here'
                exitcodes[p_index] = exitcode
                print 'Finished('+str(exitcode)+'): '+str(p_index)
        time.sleep(poll_interval)#will check again later
    return exitcodes
    
def main():
    if (len(sys.argv) != 2):
        print 'Usage: %s filename'%sys.argv[0]
        sys.exit(1)
    f=open(sys.argv[1])
    jobs = [ j.rstrip('\n') for j in f ]
    f.close()
    exitcodes = run(jobs)
    failed = [ (i+1,x,jobs[i]) for i,x in enumerate(exitcodes) if x!=0]
    if len(failed)!=0:
        print "Warning: the following jobs has non zero exit code"
        pprint(failed)
    print 'Done.'
if __name__ == '__main__':
    main()
