import os
import glob
import subprocess

# single fastq file as input

def bowtie2_single(work_dir, input_dir, output_dir, idx):

    input_dir = os.path.join(work_dir, input_dir)
    output_dir = os.path.join(work_dir, output_dir)
    filename = glob.glob(os.path.join(input_dir,"*.fastq"))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in filename:
        j = os.path.basename(i)
        output_f = os.path.join(output_dir, (j + ".sam"))
        cmd = 'bowtie2 -x' + ' ' + idx + ' ' + '-U' + ' ' + i + ' ' + '-S' + ' ' + output_f
        tst3 = subprocess.Popen(cmd, shell=True)
        tst3.wait()

# paired fastq file as input

def bowtie2_pair(work_dir, input_dir, output_dir, idx):
    input_dir = os.path.join(work_dir, input_dir)
    output_dir = os.path.join(work_dir, output_dir)
    R1_filename = glob.glob(os.path.join(input_dir, "*_R1.fastq"))
    R2_filename = glob.glob(os.path.join(input_dir, "*_R1.fastq"))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for R1 in R1_filename:
        R2 = os.path.basename(R1)
        R2 = R2.replace("_R1.fastq", "_R2.fastq")
        R2 = os.path.join(input_dir, R2)
        if R2 in R2_filename:
            j = os.path.basename(R1)
            output_f = os.path.join(output_dir, (j + ".sam"))
            cmd = 'bowtie2 -x' + ' ' + idx + ' ' + '-1' + ' ' + R1 + ' ' + '-2' + ' ' + R2 + ' ' + '-S' + ' ' + output_f
            tst4 = subprocess.Popen(cmd, shell=True)
            tst4.wait()
