# -*- encoding=utf8 -*-
import os
import subprocess

def merge_fastq(samplelist, output_dir, outputfile):


    if samplelist == "":
        print ("No fastq files in input folder")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    f1 = ""
    for x in samplelist:
        f1 = f1 + " " + x

    cmd = 'cat ' + f1 + ' > ' + outputfile
    tst = subprocess.Popen(cmd, shell=True)
    tst.wait()


def reverse_complementary(work_dir, inputfile, outputfile):


    input = os.path.join(work_dir, inputfile)
    output = os.path.join(work_dir, outputfile)
    cmd = 'gunzip -c' + ' ' + input + ' ' + '| fastx_reverse_complement -z -o' + ' ' + output
    tst2 = subprocess.Popen(cmd, shell=True)
    tst2.wait()




