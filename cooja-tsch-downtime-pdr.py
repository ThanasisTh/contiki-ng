import enum
from time import time
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.patches import Patch
import json
import os
from matplotlib.backends.backend_pdf import PdfPages
from numpy import e
import numpy as np
import sys



def time_to_msec(time):
    time_in_msec = 0
    if len(time)<=9:
        time_in_msec += int(time.split(".")[1])
        time_in_msec += int(time.split(":")[1].split(".")[0]) * 1000
        time_in_msec += int(time.split(":")[0]) * 60000
    else:
        time_in_msec += int(time.split(".")[1])
        time_in_msec += int(time.split(":")[2].split(".")[0]) * 1000
        time_in_msec += int(time.split(":")[1]) * 60000
        time_in_msec += int(time.split(":")[0]) * 3600000
    return time_in_msec
            
# dir paths
contiki_dir = "{}/repos/contiki-ng/".format(os.getenv('HOME'))
file_dir = contiki_dir + "logs/"
stats_dir = contiki_dir + "logs/stats/"
result_file = file_dir + 'final results.json'

compare_against = 'default'

ignore_algs = [
               'scan_fixed', 
               'iterate_through', 
            #    'calculate_range'
              ]

ignore_schedule = [
                    # 'minimal'
                    # 'orchestra'
                  ]

ignore_build = [
                # 'simple-node',
                # 'udp-tsch'
               ]

ignore_length = [
                # '4_4',
                # '8_8'
                ]

ignore_outtime = [
                #   '20000000',
                #   '80000000'
                 ]

ftr = [60,1]

# find simulation seeds from created log dirs
seed_dirs = [seed[0] for seed in os.walk(file_dir)]
seed_dirs.sort()

# save count of best algorithm per schedule
pre_setup_scores = {}

def main():
    for seed_dir in seed_dirs[1:]:
        seed = seed_dir.split(":")[1]
        build_dirs = [build[0] for build in os.walk(seed_dir) if build[0].split("/")[-1] not in ignore_build]
        
        for build_dir in build_dirs[1:]:
            build = build_dir.split("/")[-1]
            schedule_dirs = [schedule[0] for schedule in os.walk(build_dir) if schedule[0].split("/")[-1] not in ignore_schedule]

            for schedule_dir in schedule_dirs[1:]:
                schedule = schedule_dir.split("/")[-1]
                hop_length_dirs = [length[0] for length in os.walk(schedule_dir) if length[0].split("/")[-1] not in ignore_length]

                for hop_length_dir in hop_length_dirs[1:]:
                    hop_length = hop_length_dir.split("/")[-1]
                    outtime_dirs = [outtime[0] for outtime in os.walk(hop_length_dir) if outtime[0].split("/")[-1] not in ignore_outtime]

                    for outtime_dir in outtime_dirs[1:]:
                        outtime = int(outtime_dir.split("/")[-1])/1000000
                        setup = build + "|" + schedule + "|" + hop_length + "|" + str(outtime)
                        pp = PdfPages(outtime_dir + "/seed:" + seed + "-" + setup + "-downtimes.pdf")
                        filenames = [f for f in os.listdir(outtime_dir) if (f.split('.')[-1] == 'testlog' and f.split('.')[0].split('-')[-2] not in ignore_algs)]
                        algorithms = [file_name.split(".")[0].split("-")[-2] for file_name in filenames]
                        scores = {}
                        result = "Best result for " + schedule + ": "
                        min = 200

                        if setup not in pre_setup_scores.keys():
                            pre_setup_scores[setup] = {}
                            pre_setup_scores[setup][compare_against] = {}

                        print("## Analyzing results for seed: " + seed + " with setup: " + setup)
                        for idx, file_name in enumerate(filenames): 
                            algorithm = file_name.split(".")[0].split("-")[-2]
                            if algorithm not in pre_setup_scores[setup].keys() and algorithm != compare_against:
                                pre_setup_scores[setup][algorithm] = [0, 0]
                                scores[algorithm] = 0
                                pre_setup_scores[setup][compare_against][algorithm] = [0, 0]

                            filepath = outtime_dir + "/" + file_name

                            packets = []
                            node_IDs = []
                            end_to_end_prr = []
                            downtime = []
                            jointime = []

                            # asn drift stuff
                            timestamps = {}
                            time_space = []

                            with open(filepath, 'r') as file:
                                for line in file:
                                    # collect seed
                                    if line[0] == 'R':
                                        random_seed = int(line.split(":")[1])
                                    split = line.split("\t")
                                    # collect node ids
                                    if len(split) == 3: 
                                        current_nodeID = int(split[1].split(":")[1])
                                        if current_nodeID not in node_IDs:
                                            node_IDs.append(int(current_nodeID))
                                    # collect asn drift calculation stuff
                                    if "current asn: .000" in line:
                                        drift_id = split[1].split(":")[-1]
                                        minutes = "{:02d}".format(int(split[0])//60000) + ':' + "{:d}".format(int(split[0])%60000//10000)
                                        if minutes not in timestamps.keys():
                                            timestamps[minutes] = {} 
                                            # convert logs' timedeltas to seconds for xticks
                                            time_space.append(int(split[0])//1000)
                                        if str(drift_id) not in timestamps[minutes].keys():
                                            timestamps[minutes][str(drift_id)] = {
                                                                                'milliseconds': int(split[0])%10000,
                                                                                'asn': int(split[-1].split(".")[-1], 16)
                                                                                }
                            node_IDs.sort()
                            
                            if algorithm != 'default':            
                                pp_asn = PdfPages(outtime_dir + "/seed:" + seed + "-" + setup + "-ASN Drifts.pdf")
                                diffs = {}
                                for id in [node for node in node_IDs if node != 1]:
                                    for timestamp in timestamps.keys():
                                        # print(timestamps[timestamp])
                                        try:
                                            diff = (timestamps[timestamp]['1']['asn'] - timestamps[timestamp][str(id)]['asn']
                                                    - (timestamps[timestamp]['1']['milliseconds'] - timestamps[timestamp][str(id)]['milliseconds'])/15)
                                            diffs[timestamp] = diff
                                        except Exception as e:
                                            print(e)
                                            print(timestamps[timestamp])
                                            print(timestamp)
                                            print(timestamps.keys())
                                            # sys.exit(1)

                                    fig = plt.figure(figsize=(10,6))
                                    ax_asn = fig.add_subplot(111)
                                    ax_asn.scatter(time_space, diffs.values())
                                    ax_asn.plot(time_space, diffs.values()) 
                                    plt.yticks()
                                    plt.xticks(time_space)         
                                    ax_asn.set_ylabel("ASN drift", fontsize=14)
                                    ax_asn.set_xlabel("Timestamps", fontsize=14)
                                    ax_asn.set_xticklabels(diffs.keys(), rotation=45)
                                    ax_asn.set_title("Node: " + str(id) + " - Seed: " + str(seed) + " - Algorithm: " + algorithm + " - Schedule: " + schedule)
                                    plt.grid(True, linestyle=':', color='k', axis='both')
                                    fig = plt.gcf()
                                    # plt.show()
                                    pp_asn.savefig(fig, bbox_inches='tight')
                                    plt.close(fig)
                                pp_asn.close()

                            # node_IDs = sorted(node_IDs)
                            disconnected = 0
                            total_sim_duration = 0

                            for id in node_IDs:
                                downtime_current = 0
                                with open(filepath, 'r') as file:
                                    for line in file:
                                        split = line.split("\t")
                                        if len(split) == 3: 
                                            # collect downtime calculation stuff
                                            if "ID:"+str(id) in line and "leaving the network, stats" in line:
                                                disconnected = 1
                                                time_left = int(split[0])    
                                            if "ID:"+str(id) in line and "association done" in line:
                                                joined = 1
                                                time_joined = int(split[0])
                                                if disconnected == 1:
                                                    downtime_current += time_joined - time_left
                                                    disconnected = 0

                                    if disconnected == 1 :
                                        downtime_current += total_sim_duration - time_left
                                        downtime.append(downtime_current)
                                        downtime_current = 0
                                        disconnected = 0
                                    else :
                                        downtime.append(downtime_current)
                                        downtime_current = 0
                                        disconnected = 0

                                total_sim_duration = int(line.split(":")[1])/1000

                            for i in range(len(downtime)):
                                downtime[i] = (100*downtime[i])/int(total_sim_duration)

                            print("Average mobile node downtime for " + file_name + ": " + str(sum(downtime)/(len(downtime)-1)))
                            if sum(downtime)/(len(downtime)-1) < min:
                                min = sum(downtime)/(len(downtime)-1)
                                min_algorithm = algorithm

                            scores[algorithm] = (sum(downtime)/(len(downtime)-1))

                            fig2 = plt.figure()
                            ax = fig2.add_axes([0,0,1,1])
                            my_cmap = plt.get_cmap("Dark2")

                            for id, k, col in zip(node_IDs[1:], downtime[1:], my_cmap.colors):
                                ax.bar(id, k, color='none', edgecolor=col, hatch="xxxxx", lw=1.4, zorder = 1,  align='center', width=0.6)
                                ax.bar(id, k, color='none', edgecolor='k', zorder=1, lw=1.4,  align='center', width=0.6)
                                
                            ax.set_xticks([2,3,4,5,6])
                            plt.yticks(fontsize=14)
                            ax.set_xticklabels(['2','3','4','5','6'], fontsize='14')
                            ax.yaxis.set_major_formatter(ticker.PercentFormatter(xmax=100, decimals = 0, symbol='%'))
                            ax.set_ylim([0,60])
                            ax.set_xlabel('Node ID', fontsize=14)
                            ax.set_ylabel('Downtime', fontsize=14)
                            plt.grid(True, linestyle=':', color='k', axis='y')
                            for axis in ['top','bottom','left','right']:
                                ax.spines[axis].set_linewidth(1.4)

                            ax.set_title("Seed: " + str(seed) + " - Algorithm: " + algorithm + " - Setup: " + setup)
                            fig2 = plt.gcf()
                            fig2.set_size_inches(5, 4)
                            pp.savefig(fig2, bbox_inches='tight')
                            plt.close(fig2)

                        for alg in [key for key in scores.keys() if key != compare_against]:
                            if scores[compare_against] > scores[alg]:
                                pre_setup_scores[setup][alg][0] += 1
                                pre_setup_scores[setup][alg][1] += scores[compare_against] - scores[alg]
                            else:
                                pre_setup_scores[setup][compare_against][alg][0] += 1
                                pre_setup_scores[setup][compare_against][alg][1] += scores[alg] - scores[compare_against]

                        result += min_algorithm + " - " + str(min)
                        open(outtime_dir + "/" + result, 'a').close()
                        print(result + '\n')
                        pp.close()

    with open(result_file, 'w') as file:
        file.write(json.dumps(pre_setup_scores))

def plot_pie(conf, x, y, ax, r=1): 
    # radius for pieplot size on a scatterplot
    ax.pie([25,25,25,25], center=(x,y), radius=r, colors=[colormapping[conf['build']], colormapping[conf['schedule']],
                                                             colormapping[conf['hop_length']], colormapping[conf['outtime']]])

if __name__ == '__main__':
    if not os.path.isfile(result_file):
        main()
    else:        
        results = {}
        schedules = []
        builds = []
        hopping_lengths = []
        outtimes = []
        algorithms = set()

        markers = ['o', '+']
        colormapping = {'simple-node':'gold', 'udp-tsch':'orange',
                    'minimal':'skyblue', 'orchestra':'darkcyan',
                    '4_4':'blueviolet', '8_8':'plum',
                    '20.0':'coral', '80.0':'firebrick'}
        legend_handles = [Patch(color=colormapping[key], label=key) for key in colormapping.keys()]

        with open(result_file, 'r') as file:
            pre_setup_scores = json.load(file)
            file.close()

        print("----------------------------------------------------")
        for setup in pre_setup_scores.keys():
            results[setup] = {alg: [pre_setup_scores[setup][alg][0], pre_setup_scores[setup][alg][1] - pre_setup_scores[setup][compare_against][alg][1]] for alg in pre_setup_scores[setup].keys() if alg != compare_against}
            print(setup + '\t- ' + str(results[setup]))
            # setup_confs.append({'setup': setup, 'build': setup.split("|")[0], 'schedule': setup.split("|")[1], 'hop_length': setup.split("|")[2], 'outtime': setup.split("|")[3]})
            if setup.split("|")[0] not in builds:
                builds.append(setup.split("|")[0]) 
            if setup.split("|")[1] not in schedules: 
                schedules.append(setup.split("|")[1])
            if setup.split("|")[2] not in hopping_lengths: 
                hopping_lengths.append(setup.split("|")[2])
            if setup.split("|")[3] not in outtimes: 
                outtimes.append(setup.split("|")[3])
            algorithms.update(set(results[setup].keys()))

        # print(algorithms)
        # print(setup_confs)

        for alg in algorithms:
            setup_confs = []
            for setup in pre_setup_scores.keys():
                if alg in results[setup].keys():
                    setup_confs.append({'setup': setup, 'build': setup.split("|")[0], 'schedule': setup.split("|")[1], 
                                                        'hop_length': setup.split("|")[2], 'outtime': setup.split("|")[3]})
            pp = PdfPages(file_dir + "/" + alg + "-results.pdf")
            fig = plt.figure(figsize=(14,8))
            ax = fig.add_subplot(111)
            count_values = []
            improvement_values = []
            for setup in results.keys():
                if alg in results[setup].keys():
                    count_values.append(results[setup][alg][0])
                    improvement_values.append(results[setup][alg][1])

            # scatter chart with pie marker to represent setup
            for idx, val in enumerate(count_values):
                plot_pie(setup_confs[idx], improvement_values[idx], val, ax, r=0.8)
            _ = ax.yaxis.set_ticks(range(int(min(count_values))-3, 25, 1))
            _ = ax.xaxis.set_ticks(range(int(min(improvement_values))-3, int(max(improvement_values))+7, 5))
            plt.legend(bbox_to_anchor=(0, 1.02, 1, 1.02), loc='lower left', ncol=len(colormapping), mode='expand', handles=legend_handles)
            ax.set_frame_on(True)
            plt.grid(True, linestyle=':', color='k', axis='both')
            ax.set_ylabel("Frequency of lower average downtime (Count)", fontsize=14)
            ax.set_xlabel("Improvement score over default TSCH", fontsize=14)
            ax.set_title("Overall results for algorithm: " + alg, pad=45)
            fig = plt.gcf()
            # plt.show()
            pp.savefig(fig, bbox_inches='tight')
            plt.close(fig)

            # scatter chart for build
            fig, axs = plt.subplots(4, figsize=(14,8))
            plt.tick_params(labelcolor="none", bottom=False, left=False)
            ax_build = axs[0]
            ax_schedule = axs[1]
            ax_hop_length = axs[2]
            ax_outtime = axs[3]
            # for idx, val in enumerate(count_values):
            #     if setup_confs[idx][]

            for key, build in enumerate(builds):
                indexes = [idx for idx, _ in enumerate(setup_confs) if setup_confs[idx]['build']==build]
                ax_build.scatter([improvement_values[i] for i in indexes], [count_values[i] for i in indexes], label=build, c=colormapping[build], s=100)
                indexes = [idx for idx, _ in enumerate(setup_confs) if setup_confs[idx]['schedule']==schedules[key]]
                ax_schedule.scatter([improvement_values[i] for i in indexes], [count_values[i] for i in indexes], label=schedules[key], c=colormapping[schedules[key]], s=100)
                indexes = [idx for idx, _ in enumerate(setup_confs) if setup_confs[idx]['hop_length']==hopping_lengths[key]]
                ax_hop_length.scatter([improvement_values[i] for i in indexes], [count_values[i] for i in indexes], label=hopping_lengths[key], c=colormapping[hopping_lengths[key]], s=100)
                indexes = [idx for idx, _ in enumerate(setup_confs) if setup_confs[idx]['outtime']==outtimes[key]]
                ax_outtime.scatter([improvement_values[i] for i in indexes], [count_values[i] for i in indexes], label=outtimes[key], c=colormapping[outtimes[key]], s=100)
            
            for i, j in enumerate(axs):
                j.set_title("Overall results for algorithm: " + alg + ", by " + list(setup_confs[0].keys())[i+1])
                j.set_ylabel("Count")
                j.set_xlabel("Improvement Score")
                j.set_ylim(0, int(max(count_values))+3)
                j.set_xlim(int(min(improvement_values))-5, int(max(improvement_values))+5)
                j.grid(True, linestyle=':', color='k', axis='both')
                j.legend(loc='lower right', )
            fig.tight_layout()
            pp.savefig(fig, bbox_inches='tight')
            pp.close()