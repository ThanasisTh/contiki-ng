import shutil
import os
import time 

if os.path.isdir("/home/thanasis/"):
    contiki_dir = "/home/thanasis/repos/contiki-ng/"
    file_dir = "/home/thanasis/repos/contiki-ng/logs/"
    stats_dir = "/home/thanasis/repos/contiki-ng/logs/stats/"
    tsch_dir = "/home/thanasis/repos/contiki-ng/os/net/mac/tsch/"
    build_dir = "/home/thanasis/repos/contiki-ng/examples/6tisch/simple-node/build/"
else: 
    contiki_dir = "{}/contiki-ng/".format(os.getenv('HOME'))
    file_dir = contiki_dir + "logs/"
    stats_dir = contiki_dir + "logs/stats/"
    tsch_dir = contiki_dir + "os/net/mac/tsch/"
    build_dir = contiki_dir + "examples/6tisch/simple-node/build/"
if not os.path.isdir(file_dir):
    os.mkdir(file_dir)
    os.mkdir(stats_dir)

# seeds = [0, 123456]
seeds = [0, 1, 10, 20, 35, 127, 304, 856, 1000, 123456]
algorithms = ['default', 'calculate_channel']
guard_times = [1100, 2200, 3300]

for algorithm in algorithms:

    # clean previous mote built and replace tsch.c with algorithm
    # if os.path.isdir(build_dir):
    #     shutil.rmtree(build_dir)
    # os.remove(tsch_dir + 'tsch.c')
    
    shutil.copy(build_dir + '../0tsch_' + algorithm + '.c', tsch_dir + 'tsch.c')
    for seed in seeds:
        if not os.path.isdir(file_dir + "seed:" + str(seed)):
            os.mkdir(file_dir + "/seed:" + str(seed) + "/")
        print("\n ########### Now running simulation with algorithm " + algorithm + " and random seed: " + str(seed) + " ##############\n")
        command = "java -jar ~/contiki-ng/tools/cooja/dist/cooja.jar -nogui=examples/6tisch/simple-node/rpl-tsch-cooja-6-star.csc -random-seed={}".format(seed)
        os.system(command)
        shutil.copy(contiki_dir + "COOJA.testlog", file_dir + "seed:" + str(seed) + "/6-star-seed:" + str(seed) + "-" + algorithm + ".testlog")   
        
        time.sleep(5) 
