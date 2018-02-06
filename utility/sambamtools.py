import os
import glob
import subprocess

def sam_to_bam(work_dir, input_dir, output_dir):

    input_dir = os.path.join(work_dir, input_dir)
    output_dir = os.path.join(work_dir, output_dir)
    filenames = glob.glob(os.path.join(input_dir, "*.sam"))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in filenames:
        filename = os.path.basename(i)
        filename = filename.replace(".sam", ".bam")
        output_f = os.path.join(output_dir, filename)

        cmd = 'samtools view -S -b' + ' ' + i + ' > ' + output_f
        tst5 = subprocess.Popen(cmd, shell=True)
        tst5.wait()


def bam_dedup(work_dir, input_dir, output_dir):

    input_dir = os.path.join(work_dir, input_dir)
    output_dir = os.path.join(work_dir, output_dir)
    filenames = glob.glob(os.path.join(input_dir, "*.bam"))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


    for i in filenames:
        filename = os.path.basename(i)
        filename = filename.replace(".bam", "_dedup.bam")
        output_f = os.path.join(output_dir, filename)
        cmd = 'samtools rmdup' + ' ' + i + ' ' + output_f
        tst6 = subprocess.Popen(cmd, shell=True)
        tst6.wait()


def bam_sorted(work_dir, input_dir, output_dir):

    input_dir = os.path.join(work_dir, input_dir)
    output_dir = os.path.join(work_dir, output_dir)
    filenames = glob.glob(os.path.join(input_dir, "*_dedup.bam"))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in filenames:
        filename = os.path.basename(i)
        filename = filename.replace("_dedup.bam", "_dedup_sorted.bam")
        output_f = os.path.join(output_dir, filename)
        cmd = 'samtools sort' + ' ' + i + ' > ' + output_f
        tst7 = subprocess.Popen(cmd, shell=True)
        tst7.wait()

def bam_index_generator(work_dir, input_dir, output_dir):

    input_dir = os.path.join(work_dir, input_dir)
    output_dir = os.path.join(work_dir, output_dir)
    filenames = glob.glob(os.path.join(input_dir, "*_dedup_sorted.bam"))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in filenames:
        filename = os.path.basename(i)
        filename = filename.replace("_dedup_sorted.bam", "_dedup_sorted.bam.bai")
        output_f = os.path.join(output_dir, filename)
        cmd = 'samtools index' + ' ' + i
        tst8 = subprocess.Popen(cmd, shell=True)
        tst8.wait()

def bam_to_bigwig(work_dir, input_dir, output_dir):

    input_dir = os.path.join(work_dir, input_dir)
    output_dir = os.path.join(work_dir, output_dir)
    filenames = glob.glob(os.path.join(input_dir, "*_dedup_sorted.bam"))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in filenames:
        filename = os.path.basename(i)
        filename = filename.replace("_dedup_sorted.bam", "_dedup_sorted.bw")

        output_f = os.path.join(output_dir, filename)
        cmd = 'bamCoverage -b' + ' ' + i + ' -o ' + output_f
        tst9 = subprocess.Popen(cmd, shell=True)
        tst9.wait()

def bam_to_bed(work_dir, input_dir, output_dir):

    input_dir = os.path.join(work_dir, input_dir)
    output_dir = os.path.join(work_dir, output_dir)
    filenames = glob.glob(os.path.join(input_dir, "*_dedup_sorted.bam"))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i in filenames:
        filename = os.path.basename(i)
        filename = filename.replace("_dedup_sorted.bam", "_dedup_sorted.bed")
        output_f = os.path.join(output_dir, filename)
        cmd = 'bedtools bamtobed -i' + ' ' + i + ' > ' + output_f
        tst10 = subprocess.Popen(cmd, shell=True)
        tst10.wait()