import os
import compile_all_benign

path_to_perf_scripts = "./perf_scripts_benign/"
path_to_perf_scripts_malware = "./perf_scripts_malware/"
path_to_benign_log_file = "./log_file_benign/"
path_to_malware_log_file = "./log_file_malware/"
indicator_list = ["ls", "ps", "netstat", "who", "pwd"]
path_to_malware_file = "../Malware_Program/"

def generate_benign():
    if not os.path.exists(compile_all_benign.benign_program_directory):
        compile_all_benign.compile_benign()
    list_of_benign = os.listdir(compile_all_benign.benign_program_directory)
    if not os.path.exists(path_to_perf_scripts):
        os.makedirs(path_to_perf_scripts)
    num_observations = 50
    num_indicators = len(indicator_list)
    files_run = []
    for item in list_of_benign:
        log_file = item + ".txt"
        with open(path_to_perf_scripts + item + ".sh", "w") as f:
            files_run.append(path_to_perf_scripts + item + ".sh")
            for i in xrange(num_indicators):
                for j in xrange(num_observations):
                    f.write("3>>" + path_to_benign_log_file+log_file + " perf stat --log-fd 3 --append -e cycles,instructions,cache-references,cache-misses,branches,branch-misses " + indicator_list[i] + " & " + compile_all_benign.benign_program_directory + item + "\nsleep 1s\necho -en \"\\n\"\n")
    with open("run_all_benign.sh", "w") as f:
        for file in files_run:
            f.write(file + "\n")
    os.system("chmod +x -R ../Offline")

def generate_malware():
    list_of_malware = os.listdir(path_to_malware_file)
    if not os.path.exists(path_to_perf_scripts_malware):
        os.makedirs(path_to_perf_scripts_malware)
    num_observations = 50
    num_indicators = len(indicator_list)
    files_run = []
    for item in list_of_malware:
        log_file = item + ".txt"
        with open(path_to_perf_scripts_malware + item + ".sh", "w") as f:
            files_run.append(path_to_perf_scripts_malware + item + ".sh")
            for i in xrange(num_indicators):
                for j in xrange(num_observations):
                    f.write("3>>" + path_to_malware_log_file+log_file + " perf stat --log-fd 3 --append -e cycles,instructions,cache-references,cache-misses,branches,branch-misses " + indicator_list[i] + " & " + path_to_malware_file + item + "\nsleep 1s\necho -en \"\\n\"\n")
    with open("run_all_malware.sh", "w") as f:
        for file in files_run:
            f.write(file + "\n")
    os.system("chmod +x -R ../Offline")
    os.system("chmod +x -R ../Malware_Program")