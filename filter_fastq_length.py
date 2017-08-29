#!/usr/bin/env python
# Miten Jain (miten@soe.ucsc.edu)
# filter_fastq_length.py

import sys, time, glob, os
import numpy
from optparse import OptionParser

# using generator and yield function to read 4 lines at a time
def getStanza (infile):
    while True:
        fasta_id = infile.readline().rstrip()
        fasta_seq = infile.readline().rstrip()
        qual_id = infile.readline().rstrip()
        qual_scr = infile.readline().rstrip()
        if fasta_id != '':
            yield [fasta_id, fasta_seq, qual_id, qual_scr]
        else:
            print >> sys.stderr, 'Warning: End of Sequence'
            break

########################################################################
# Main
# Here is the main program
########################################################################

def main(myCommandLine=None):

    t0 = time.time()

    #Parse the inputs args/options
    parser = OptionParser(usage='usage: ./filter_fastq_length.py --in ./fastq --low 0 --high  \
                                        1000000 --out out.fastq', version='%prog 0.0.1')

    #Options
    parser.add_option('--in', dest='infile', help='input fastq (required)', default='')
    parser.add_option('--low', dest='low', help='low read length cutoff', type=int, \
                        default=0)
    parser.add_option('--high', dest='high', help='high read length cutoff', type=int, \
                        default=100000)
    parser.add_option('--out', dest='outfile', help='output fastq, default stdout', default='')

    #Parse the options/arguments
    options, args = parser.parse_args()

    #Print help message if no input
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    print >> sys.stderr, options

    inFile = options.infile
    low_cut = int(options.low)
    high_cut = int(options.high)
    outFile = options.outfile

    if outFile == '':
        outputFile = sys.stdout
    else:
        outputFile = open(outFile, 'w')

    slice_stats = []
    count = 0
    len_list = []
    inputFile = open(inFile, 'r')
    for stanza in getStanza(inputFile):
        length = len(stanza[1])
        len_list.append(length)
        if length > low_cut and length < high_cut: 
            count += 1
            print >> outputFile, stanza[0]
            print >> outputFile, stanza[1]
            print >> outputFile, stanza[2]
            print >> outputFile, stanza[3]
            slice_stats.append(len(stanza[1]))
    inputFile.close()

    if not outputFile == sys.stdout:
        outputFile.close()

    print >> sys.stderr, '# reads', '# bases', '# reads (slice)', '# bases (slice)', 'median length (slice)'
    print >> sys.stderr, len(len_list), numpy.sum(len_list), len(slice_stats), numpy.sum(slice_stats), numpy.median(slice_stats)

    print >> sys.stderr, '\n', 'total time for the program %.3f' % (time.time()-t0)

if (__name__ == '__main__'):
    main()
    raise SystemExit
