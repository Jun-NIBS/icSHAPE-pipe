#!/usr/bin/env python
#-*- coding:utf-8 -*-

import GAP
import sys
import numpy
import getopt
import os
import version

from StatisticPlot import *

Usage = """
transSHAPEStatistics - Statistics the RNA distribution of transcript-based SHAPE
=================================================================================
\x1b[1mUSAGE:\x1b[0m 
  %s -g genomeCoor.bed -i transSHAPE.out -o report.pdf

\x1b[1mHELP:\x1b[0m        
  -g                    <String>
                                A genome-coor based annotation file: hg38.genomeCoor.bed (generated by parseGTF)

  -i                    <String>
                                Input a transSHAPE file produced by genSHAPEToTransSHAPE
  -o                    <String>
                                Output statistics to PDF file (default: report.pdf)

\x1b[1mVERSION:\x1b[0m
    %s

\x1b[1mAUTHOR:\x1b[0m
    Li Pan

""" % (sys.argv[0], version.Version)


def init():
    params = { 'inputFile': None, 'reportFile': 'report.pdf', 'annotation': None }
    opts, args = getopt.getopt(sys.argv[1:], 'hi:g:o:')
    for op, value in opts:
        if op == '-h':
            print >>sys.stdout, Usage;
            sys.exit(-1)
        # Basic Parameters
        elif op == '-i':
            params['inputFile'] = os.path.abspath(value)
        elif op == '-g':
            params['annotation'] = os.path.abspath(value)
        elif op == '-o':
            params['reportFile'] = os.path.abspath(value)
        
        else:
            print >>sys.stderr, "Error: unrecognized parameter: "+op
            print >>sys.stdout, Usage;
            sys.exit(-1)
    # check
    if (not params['inputFile']) or (not params['annotation']):
        print >>sys.stderr, "Error: Please specify -i -g"
        print >>sys.stdout, Usage
        sys.exit(-1)
    
    return params

def loadicSHAPE(file_name):
    SHAPE = {}
    for line in open(file_name):
        arr = line.strip().split()
        trans_id = arr[0]
        shape = arr[3:]
        SHAPE[ trans_id ] = shape
    return SHAPE

def main():
    params = init()
    
    print "Start load icSHAPE file..."
    SHAPE = loadicSHAPE(params['inputFile'])
    
    print "Start load annotation file..."
    Parser = GAP.init(params['annotation'])
    
    print "Start statistic..."
    PlotTransSHAPEStatistics(SHAPE, Parser, params['reportFile'])


if __name__ == '__main__':
    main()


