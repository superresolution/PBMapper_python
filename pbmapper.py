# -*- encoding=utf8 -*-
"""
python pbmapper.py -i /media/changhao/Data/python_test -x /home/changhao/app/index/mm10

"""

import os
import glob
import sys
import argparse

from utility.fastqtools import merge_fastq, reverse_complementary
from utility.biopythontools import joint_barcode_splitter_trimmer_withttaa
from utility.mappingtools import bowtie2_single as bowtie2
from utility.sambamtools import sam_to_bam, bam_dedup, bam_index_generator, bam_sorted, bam_to_bigwig, bam_to_bed

# parameters
fastqc = Bowtie2 = fastx_toolbox = Cufflinks = DESeq = DEXSeq = GATK = GFold  = False
# argparse arguments
parser = argparse.ArgumentParser(description='A pipeline of PB insertion data analysis. <changhao1986@outlook.com>',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-i', '--input',
                    help = "",
                    required = True)
parser.add_argument('-x', '--index',
                    help = "genome index dir",
                    required = True)
# parser.add_argument('-b', '--barcode',
#                     help = "",
#                     required = True)
args = parser.parse_args()

# init
__VERSION__ = 'V0.1'

if not os.path.exists(args.input):
    sys.exit('ArgumentError:\tinput must be a file path.')

# fastq file merge
R1_files=glob.glob(os.path.join(args.input,"1_or_seq/R1*.fastq.gz"))
R2_files=glob.glob(os.path.join(args.input,"1_or_seq/R2*.fastq.gz"))
merge_fastq(R1_files, os.path.join(args.input, "2_merged"),os.path.join(args.input,"2_merged/R1.fastq.gz"))
merge_fastq(R2_files, os.path.join(args.input, "2_merged"),os.path.join(args.input,"2_merged/R2.fastq.gz"))
reverse complementary
reverse_complementary(args.input,"2_merged/R2.fastq.gz", "2_merged/R2_R.fastq.gz")
join splitter trimmer with ttaa detection
joint_barcode_splitter_trimmer_withttaa(args.input, "2_merged/R1.fastq.gz", "2_merged/R2_R.fastq.gz","5_joint_spliter_trimmer_withttaa")
# bowtie2
bowtie2(args.input, "5_joint_spliter_trimmer_withttaa", "6_bowtie2", args.index)
# samtools
sam_to_bam(args.input, "6_bowtie2", "6_bowtie2")
bam_dedup(args.input, "6_bowtie2", "7_bowtie2_dedup")
bam_sorted(args.input, "7_bowtie2_dedup", "8_bowtie2_dedup_sorted")
bam_index_generator(args.input, "8_bowtie2_dedup_sorted", "8_bowtie2_dedup_sorted")
# bamCoverage
bam_to_bigwig(args.input, "8_bowtie2_dedup_sorted", "9_bigwigfile")
# generate bedfile
bam_to_bed(args.input, "8_bowtie2_dedup_sorted", "10_bedfile")




##############################################################################################
# if not os.path.exists(args.output):
#     os.mkdir(args.output)

# if not os.path.exists(args.index):
#     sys.exit('ArgumentError:\tindex must be a file path.')

# if not os.path.isfile(args.barcode):
#     sys.exit('ArgumentError:\tbarcode must be a file.')

###############################################################################################