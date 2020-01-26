import subprocess
import time
import os
import signal
import sys
import random

# COMPRESSION SIZE LOOKUP TABLE
# The bounds on byte location depends on variables
COMPRESSION_SIZE = {
    'IDLE': 1,
    'ABS_1e2': 165724480,
    'ABS_1e3': 282474401,
    'PW_1e2': 81505624,
    'PW_1e3': 138572647,
    'PSNR_30': 70238798,
    'PSNR_60': 75895303
}

# Calls C Program, checks to see if it finished near instantly.
# If not then wait the timeout period and check every .1 seconds.
def popen_timeout(command, timeout):
    p = subprocess.Popen(command, stdout=subprocess.PIPE)
    time.sleep(.03)
    if p.poll() is not None:
        return p.communicate(), p.pid
    else:
        for t in range(timeout*10):
            time.sleep(.1)
            if p.poll() is not None:
                return  p.communicate(), p.pid
        p.kill()
        return ["Timeout"], p.pid

def main():
    # Start RAPL
    print("Starting experiment ...")
    cmd = ['sudo','./rapl_plot', 
            sys.argv[1],
            sys.argv[2],
            sys.argv[3],
            sys.argv[4],
            sys.argv[5],
            sys.argv[6],
            sys.argv[7],
            sys.argv[8],
    ]

    try: 
        compression_arg = sys.argv[9]
    except:
        print("Please enter a valid compression value: ['ABS_1e2','ABS_1e3','PW_1e2','PW_1e3','PSNR_30','PSNR_60']")
        exit(0)
    byte_loc = random.randint(0,COMPRESSION_SIZE[compression_arg])
    flip_loc = random.randint(0,7)

    print("Byte Location: ",byte_loc)
    print("Flip Location: ",flip_loc)
    SZcmd = ['bash', '/users/gfwilki/Compression_Injection-Power_Experiment/injection_experiments.sh', str(sys.argv[9]),  str(byte_loc), str(flip_loc)]
    #SZcmd = ['bash', '/users/gfwilki/Compression_Injection-Power_Experiment/injection_experiments.sh', str(compression_arg), str(byte_loc), str(flip_loc)]
    timeout_limit = 7 # If taking too long bc injection broke stuff, go ahead and kill experiment

    rapl = subprocess.Popen(cmd, stdin = subprocess.PIPE, stdout=subprocess.PIPE)
    
    # Call suprocess to run SZ
    #print("Starting SZ")
    #time.sleep(1)
    #p = subprocess.Popen(SZcmd, stdin = subprocess.PIPE, stdout=subprocess.PIPE)
    proc_result, child_process_id = popen_timeout(SZcmd, timeout_limit)    
    #time.sleep(1)
    #print(p.communicate()) # You can use this to confirm that it worked
    #print("Ending SZ")

    #child_process_id.kill()
    print("Ending experiment...")


if __name__ == '__main__':
	main()

