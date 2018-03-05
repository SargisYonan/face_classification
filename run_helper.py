from optparse import OptionParser

parser = OptionParser()

parser.add_option("-t", "--threads", dest="threads",
                  help="Select number of threads to run training on", default=1)
parser.add_option("-d", "--divider", dest="divider", default=1,
                  help="size to divide the input size that is ~1T instructions")

(options, args) = parser.parse_args()

threads = int(options.threads)
divider = int(options.divider)


to_append = "\"python face_classifier/src/throughput.py -d " + str(divider*threads) + "\" "

argument = ""
for i in range(0, threads):
	argument += to_append

print argument
