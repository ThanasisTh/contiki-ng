from posixpath import split
import shutil
import os
import time 
from file_utils import replace_string_in_file

if os.path.isdir("/home/thanasis/"):
    contiki_dir = "/home/thanasis/repos/contiki-ng/"
    file_dir = "/home/thanasis/repos/contiki-ng/logs/"
    stats_dir = "/home/thanasis/repos/contiki-ng/logs/stats/"
    tsch_dir = "/home/thanasis/repos/contiki-ng/os/net/mac/tsch/"
    build_dirs = ["/home/thanasis/repos/contiki-ng/examples/6tisch/simple-node/", 
                  "/home/thanasis/repos/contiki-ng/examples/6tisch/udp-tsch/"
                 ]
else: 
    contiki_dir = "{}/contiki-ng/".format(os.getenv('HOME'))
    file_dir = contiki_dir + "logs/"
    stats_dir = contiki_dir + "logs/stats/"
    tsch_dir = contiki_dir + "os/net/mac/tsch/"
    build_dirs = [contiki_dir + "examples/6tisch/simple-node/",
                  contiki_dir + "examples/6tisch/udp-tsch/"
                 ]
if not os.path.isdir(file_dir):
    os.mkdir(file_dir)
    os.mkdir(stats_dir)
    
# seeds = []
seeds = [0, 1, 10, 20, 38, 127, 304, 856, 1000, 123456]
seeds += [715, 5874, 8128, 42069, 67234, 80085, 84123, 98989, 99999, 933933]
seeds += [222, 420, 5254, 6969, 7945]
seeds.sort()
# seeds = [123456]

# algorithms = ['default', 'calculate_channel', 'calculate_range', 'scan_fixed', 'iterate_through']
algorithms = ['calculate_range', 'default', 'calculate_channel']

schedules = ['minimal',
             'orchestra'
            ]

out_of_range_duration = [
                         20000000, 
                         80000000
                        ] # time in seconds mobile nodes stay out of range, should convert to microseconds for .csc file

seq_lengths = [
                'TSCH_HOPPING_SEQUENCE_8_8', 
                'TSCH_HOPPING_SEQUENCE_4_4'
              ]

for build_dir in build_dirs:
    simulation_file = build_dir + build_dir.split("/")[-2] + ".csc"

    for schedule in schedules: 
        if schedule == 'orchestra':
            replace_string_in_file(build_dir + "Makefile", 'MAKE_WITH_ORCHESTRA ?=', 1, split_index=-1)
        elif schedule == 'minimal':
            replace_string_in_file(build_dir + "Makefile", 'MAKE_WITH_ORCHESTRA ?=', 0, split_index=-1)

        for wander_duration in out_of_range_duration:
            replace_string_in_file(simulation_file, 'var mobile_node_rejoin', str(wander_duration)+';', split_index=-1, separator=" = ")
            print("---------------- running sim with node remaining outside range for " + str(wander_duration/1000000) + "seconds-----------------")

            for algorithm in algorithms:
                shutil.copy(build_dir + '0tsch_' + algorithm + '.c', tsch_dir + 'tsch.c')
                # clean previous mote built and replace tsch.c with algorithm (not needed because cooja cleans the build on its own now)
                # if os.path.isdir(build_dir):
                #     shutil.rmtree(build_dir)
                # os.remove(tsch_dir + 'tsch.c')

                for length in seq_lengths:
                    replace_string_in_file(tsch_dir + 'tsch-conf.h', '#define TSCH_DEFAULT_HOPPING_SEQUENCE TSCH_HOPPING', length, split_index=-1)
                    print('------------------------------------------------------------------------------------------------------------------------')
                    print('running setup: ' + build_dir.split("/")[-2] + "|" + schedule + "|" + length + "|" + str(wander_duration))
                    print('------------------------------------------------------------------------------------------------------------------------')

                    for seed in seeds:  
                        # if not os.path.isdir(file_dir + "seed:" + str(seed)):
                        #     os.mkdir(file_dir + "/seed:" + str(seed) + "/")
                        # if not os.path.isdir(file_dir + "seed:" + str(seed) + "/" + schedule):
                        #     os.mkdir(file_dir + "/seed:" + str(seed) + "/" + schedule + "/")
                        if not os.path.isdir(file_dir + "seed:" + str(seed) + "/" + simulation_file.split(".")[0].split("/")[-1] + "/" + schedule + "/" 
                                    + length.split("_HOPPING_SEQUENCE_")[-1] + "/" + str(wander_duration)):
                            os.makedirs(file_dir + "/seed:" + str(seed) + "/" + simulation_file.split(".")[0].split("/")[-1] + "/" + schedule + "/" 
                                    + length.split("_HOPPING_SEQUENCE_")[-1] + "/" + str(wander_duration) + "/")
                            
                        else:
                            delete_previous_results = "find " + file_dir + " -name 'Best result*' -type f -delete"
                            os.system(delete_previous_results)
                        
                        if not os.path.isfile(file_dir + "seed:" + str(seed) + "/" + simulation_file.split(".")[0].split("/")[-1] + "/" + schedule + "/" 
                                        + length.split("_HOPPING_SEQUENCE_")[-1] + "/" + str(wander_duration) + "/6-star-seed:" + str(seed) + "-" + algorithm + "-" + schedule + ".testlog"):
                            print("\n ########### Now running simulation with algorithm " + algorithm + ", schedule: " + schedule + " and random seed: " + str(seed) + " ##############\n")
                            command = "java -jar ~/contiki-ng/tools/cooja/dist/cooja.jar -nogui=" + simulation_file + " -random-seed={}".format(seed)
                            os.system(command)
                            shutil.copy(contiki_dir + "COOJA.testlog", file_dir + "seed:" + str(seed) + "/" + simulation_file.split(".")[0].split("/")[-1] + "/" + schedule + "/" 
                                        + length.split("_HOPPING_SEQUENCE_")[-1] + "/" + str(wander_duration) + "/6-star-seed:" + str(seed) + "-" + algorithm + "-" + schedule + ".testlog")   
                        
                            time.sleep(1) 