import csv
import os
import matplotlib.pyplot as plt

plotting = False
fat_list = []
csv_dir = 'outputs'

def mpki(unit, insts):
	return 1000 * unit / insts

def list_avg(list):
	sum = 0
	for e in list:
		sum += e
	return sum/len(list)

def get_runtime(timelist):
	return timelist[len(timelist) - 1] - timelist[0]

def calculate_and_save_plots(csv_filename):

	inst_cnt_list = []
	cycle_cnt_list = []
	l1_miss_list = []
	l3_miss_list = []
	branch_miss_list = []
	timestamps = []

	ipc = []
	branch_mpki = []
	l1_mpki = []
	l3_mpki = []
	time = []

	with open(csv_filename, 'rb') as csvfile:
		normalized_plot_reader = csv.DictReader(csvfile, delimiter=',', quotechar='"')

		for row in normalized_plot_reader:
			try:
				timestamps.append(float(row["Timestamp"]))
			except:
				timestamps.append(timestamps[len(timestamps) - 1])

			try:
				inst_cnt_list.append(float(row["instructions"]))
			except:
				if len(inst_cnt_list) > 0:
					inst_cnt_list.append(inst_cnt_list[len(inst_cnt_list) - 1])
				else:
					inst_cnt_list.append(0)

			try:
				l1_miss_list.append(float(row["L1-dcache-load-misses"]))
			except:
				l1_miss_list.append(l1_miss_list[len(l1_miss_list) - 1])

			try:
				l3_miss_list.append(float(row["LLC-load-misses"]))
			except:
				l3_miss_list.append(l3_miss_list[len(l3_miss_list) - 1])

			try:
				branch_miss_list.append(float(row["branch-misses"]))
			except:
				branch_miss_list.append(branch_miss_list[len(branch_miss_list) - 1])

			try:
				cycle_cnt_list.append(float(row["cpu-cycles"]))
			except:
				cycle_cnt_list.append(cycle_cnt_list[len(cycle_cnt_list) - 1])

		time_offset = timestamps[0]
		for t in timestamps:
			time.append(t - time_offset)

		last_inst = 0
		last_cyc = 0
		for inst,cycles in zip(inst_cnt_list, cycle_cnt_list):
			ipc.append((last_inst+inst)/(last_cyc + cycles))
			last_inst = inst
			last_cyc = cycles

		for l1_miss, l3_miss, brnch_miss, inst in zip(l1_miss_list, l3_miss_list, branch_miss_list, inst_cnt_list):
			l1_mpki.append(mpki(l1_miss, inst))
			l3_mpki.append(mpki(l3_miss, inst))
			branch_mpki.append(mpki(brnch_miss, inst))

		# start looking only after the norm part
		data_container = csv_filename.split('norm_')[1]
		data_container = data_container.split('.csv')[0]
		# should be left with <threads>_<divider>
		data_container = data_container.split('-')

		thread = data_container[0]
		divider = data_container[1]

		if int(thread) > 1:
			thread_noun = 'threads'
		else:
			thread_noun = 'thread'

		if int(divider) > 1:
			divider_noun = '/' + str(divider)
		else:
			divider_noun = ''

		fat_list.append((thread, divider, str(list_avg(ipc)), str(list_avg(l1_mpki)), str(list_avg(l3_mpki)), str(list_avg(branch_mpki)), str(get_runtime(time))))

		if plotting:
			plt.plot(time, ipc, 'k')
			plt.ylabel('IPC')
			plt.xlabel('Time')
			plt.grid()
			plt.title('IPC over Time - ' + thread + ' ' + thread_noun + '  - input size X' + divider_noun)
			plt.savefig(csv_dir + '/figures/ipc_'+ thread + '_' + thread_noun + '_' + 'div_' + divider + '.png')
			plt.clf()

			l1plt, = plt.plot(time, l1_mpki, 'k', label='L1 MPKI')
			l3plt, = plt.plot(time, l3_mpki, 'r', label='L3 MPKI')
			plt.ylabel('Cache MPKI')
			plt.xlabel('Time')
			plt.grid()
			plt.title('L1,L3 MPKI over Time - ' + thread + ' ' + thread_noun + '  - input size X' + divider_noun)
			plt.legend(handles=[l1plt, l3plt])
			plt.savefig(csv_dir + '/figures/l1l3mpki_'+ thread + '_' + thread_noun + '_' + 'div_' + divider + '.png')
			plt.clf()

			plt.plot(time, branch_mpki, 'k')
			plt.ylabel('Branch Cache MPKI')
			plt.xlabel('Time')
			plt.grid()
			plt.title('Branch MPKI over Time - ' + thread + ' ' + thread_noun + '  - input size X' + divider_noun)
			plt.savefig(csv_dir + '/figures/branchmpki_'+ thread + '_' + thread_noun + '_' + 'div_' + divider + '.png')
			plt.clf()

for filename in os.listdir(csv_dir):
    if filename.endswith(".csv") and filename.startswith("norm"): 
        csv_filename = os.path.join(csv_dir, filename)
        calculate_and_save_plots(csv_filename)
        continue
    else:
        continue

fat_list = sorted(fat_list, key=lambda x: int(x[0]))

thread_one = sorted(fat_list[0:5], key=lambda x: int(x[1]))
thread_two = sorted(fat_list[5:10], key=lambda x: int(x[1]))
thread_four = sorted(fat_list[10:15], key=lambda x: int(x[1]))
thread_eight = sorted(fat_list[15:20], key=lambda x: int(x[1]))

thread_list = [thread_one, thread_two, thread_four, thread_eight]

for t in thread_list:
	thread = t[0][0]
	ipc_list = []
	l1_list = []
	l3_list = []
	branch_list = []
	runtime_list = []

	for d in t:
		ipc_list.append(d[2])
		l1_list.append(d[3])
		l3_list.append(d[4])
		branch_list.append(d[5])
		runtime_list.append(d[6])		

	print("**********************************************************************")
	print("Run: " + thread + " thread(s): ")
	print("\nAverage IPC:")
	print("X: " + ipc_list[0] + "\nX/4: " + ipc_list[1] + "\nX/16: " + ipc_list[2] + "\nX/64: " + ipc_list[3] + "\nX/256: " + ipc_list[4])
	print("\nRuntime (seconds): ")
	print("X: " + runtime_list[0] + "\nX/4: " + runtime_list[1] + "\nX/16: " + runtime_list[2] + "\nX/64: " + runtime_list[3] + "\nX/256: " + runtime_list[4])	
	print("\nAverage L1 MPKI: ")
	print("X: " + l1_list[0] + "\nX/4: " + l1_list[1] + "\nX/16: " + l1_list[2] + "\nX/64: " + l1_list[3] + "\nX/256: " + l1_list[4])
	print("\nAverage L3 MPKI: ")
	print("X: " + l3_list[0] + "\nX/4: " + l3_list[1] + "\nX/16: " + l3_list[2] + "\nX/64: " + l3_list[3] + "\nX/256: " + l3_list[4])
	print("\nAverage Branch MPKI: ")
	print("X: " + branch_list[0] + "\nX/4: " + branch_list[1] + "\nX/16: " + branch_list[2] + "\nX/64: " + branch_list[3] + "\nX/256: " + branch_list[4])	

