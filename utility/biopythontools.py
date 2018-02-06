
from Bio import SeqIO
from Bio import Seq
import gzip
import operator
import os


#

Q5 = ["TAATGTGG",
              "GCACTCAG",
              "AACAGCGG",
              "CCATATGA",
              "TGGAAAGC",
              "AGCAACGC",
              "CCCTTGCA",
              "CCCTCTTG",
              "TTCGAGCC",
              "AGTAGTTA"]

Q7R = ["ATGCGGAT",
        "ACTTCAAT",
        "ACGCAGAG",
        "TGCGTATC",
        "CGAACGTA",
        "AGGATTCA",
        "TTATAGCC",
        "AGGTTGTG",
        "GAGGCTGA",
        "AACAATCC"]

Q5_name = []
Q7_name = []
filenames = []

for i in range(1,11):
    Q5_name.append("Q5_" + str(i))
    Q7_name.append("Q7_" + str(i))
for i in range(0,100):
    filenames.append(Q5_name[i//10] + "_" + Q7_name[i%10] + ".fastq")


#

def hamdist(str1, str2):
    diffs = 0
    for ch1, ch2 in zip(str1, str2):
        if ch1 != ch2:
            diffs += 1
    return diffs

#

def joint_barcode_splitter_trimmer(work_dir, file_R1, file_R2, directory, mismatch = 3, plus = 37, minus = -28):
    # parameter

    directory = os.path.join(work_dir, directory)
    input_R1 = os.path.join(work_dir, file_R1)
    input_R2 = os.path.join(work_dir, file_R2)

    if not os.path.exists(directory):
        os.makedirs(directory)

    filedata = {filename: open(os.path.join(directory, filename), 'w') for filename in filenames} # filenames need figureout

    i = 1
    rec2 = SeqIO.parse(gzip.open(input_R2, 'rt'), "fastq")

    for record in SeqIO.parse(gzip.open(input_R1, 'rt'), "fastq"):
        if i < 100:
            record2 = rec2.__next__()  # for python 2 is next()
            # if record2.id == record.id:
            # print "yes"
            sequence = str(record.seq)
            letter_annotations = record.letter_annotations
            sequence2 = str(record2.seq)
            letter_annotations2 = record2.letter_annotations

            #
            Q5_diff = []
            Q7_diff = []

            for index, value in enumerate(Q5):
                Q5_diffs = hamdist(sequence[:8], value)
                Q5_diff.append(Q5_diffs)

            for index, value in enumerate(Q7R):
                Q7_diffs = hamdist(sequence2[-8:], value)
                Q7_diff.append(Q7_diffs)

            Q5_min_index, Q5_min_value = min(enumerate(Q5_diff), key=operator.itemgetter(1))
            Q7_min_index, Q7_min_value = min(enumerate(Q7_diff), key=operator.itemgetter(1))

            # print (Q5_min_index, Q5_min_value, Q7_min_index, Q7_min_value)

            if (Q5_min_value < mismatch) & (Q7_min_value < mismatch):
                # print ("yes")
                record.letter_annotations = {}
                new_sequence = sequence[plus:] + sequence2[:minus]
                record.seq = Seq.Seq(new_sequence)
                new_letter_annotations = {'phred_quality': (
                            letter_annotations['phred_quality'][plus:] + letter_annotations2['phred_quality'][:minus])}
                record.letter_annotations = new_letter_annotations

                f_name = filenames[Q5_min_index * 10 + Q7_min_index]
                SeqIO.write(record, filedata[f_name], "fastq")
                # print (record)
        else:
            break

        # i = i + 1 # just for program test

    print('Out of loop')

    for file in filedata.values():
        file.close()


def joint_barcode_splitter_trimmer_withttaa(work_dir, file_R1, file_R2, directory, mismatch = 3, plus = 37, minus = -28, left = 2, right = 12):
    # parameter

    directory = os.path.join(work_dir, directory)
    input_R1 = os.path.join(work_dir, file_R1)
    input_R2 = os.path.join(work_dir, file_R2)


    if not os.path.exists(directory):
        os.makedirs(directory)

    filedata = {filename: open(os.path.join(directory, filename), 'w') for filename in filenames}
    print(filenames)

    i = 1
    rec2 = SeqIO.parse(gzip.open(input_R2, 'rt'), "fastq")
    # print (input[:])

    for record in SeqIO.parse(gzip.open(input_R1, 'rt'), "fastq"):
        if i < 100:
            record2 = rec2.__next__()  # for python 2 is next()
            # if record2.id == record.id:
            # print "yes"
            sequence = str(record.seq)
            letter_annotations = record.letter_annotations
            sequence2 = str(record2.seq)
            letter_annotations2 = record2.letter_annotations

            #
            Q5_diff = []
            Q7_diff = []

            for index, value in enumerate(Q5):
                Q5_diffs = hamdist(sequence[:8], value)
                Q5_diff.append(Q5_diffs)

            for index, value in enumerate(Q7R):
                Q7_diffs = hamdist(sequence2[-8:], value)
                Q7_diff.append(Q7_diffs)

            Q5_min_index, Q5_min_value = min(enumerate(Q5_diff), key=operator.itemgetter(1))
            Q7_min_index, Q7_min_value = min(enumerate(Q7_diff), key=operator.itemgetter(1))

            # print (Q5_min_index, Q5_min_value, Q7_min_index, Q7_min_value)

            str1 = sequence[(plus - left):(plus + right)]

            if (Q5_min_value < mismatch) & (Q7_min_value < mismatch) & (str1.find("TTAA") > -1):
                # print ("yes")
                record.letter_annotations = {}
                new_sequence = sequence[plus:] + sequence2[:minus]
                record.seq = Seq.Seq(new_sequence)
                new_letter_annotations = {'phred_quality': (
                            letter_annotations['phred_quality'][plus:] + letter_annotations2['phred_quality'][:minus])}
                record.letter_annotations = new_letter_annotations

                f_name = filenames[Q5_min_index * 10 + Q7_min_index]
                SeqIO.write(record, filedata[f_name], "fastq")
                # print (record)
        else:
            break

        # i = i + 1 # just for program test

    print('Out of loop')

    for file in filedata.values():
        file.close()

