#! python3
import sys
import argparse

parser = argparse.ArgumentParser(description="Filter changetext.log from rubbish lines.")
parser.add_argument("inputfile")
parser.add_argument("outputfile")
args = parser.parse_args(sys.argv[1:])

f_out = open(args.outputfile, "xb")
with open(args.inputfile, "rb") as file:
    file.seek(0, 2)  # Rewind to the end of file
    total_size = file.tell()
    multiplier = 1 if total_size < 1024**3 else 10
    file.seek(0)
    prev_percent = 0
    for line in file:
        pos = file.tell()
        if b"-->" in line:
            f_out.write(line)

        percent = int(pos / total_size * 100 * multiplier) / multiplier
        if percent > prev_percent:
            print("%s%%" % percent, file=sys.stderr)
            prev_percent = percent
