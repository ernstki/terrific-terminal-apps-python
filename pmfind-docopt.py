#!/usr/bin/env python3
#
#  A framework for a simple command-line program using docopt for
#  input argument parsing, that plays nicely inside a Unix pipeline.
#
#  This toy example queries the PubMed index of scientific literature
#  for recent publications (from the first page of results) matching
#  one or more keywords supplied as arguments.
#
#  Example usage:
#
#    $ pmfind smoking
#    $ pmfind breast cancer
#    $ pmfind < keyword_list.txt > results.tsv
#    $ echo "term1 term2 term3" | pmfind
#
#  Author: Kevin Ernst
#  Date:   14 May 2020
#

"""
pmfind-docopt.py
    Search NCBI PubMed for given TERM(s), return a list of URLs and titles

Usage:
    pmfind-docopt.py [options] TERM...

Options:
    -h --help                shows this help

Problems?
    Please report bugs at https://bit.ly/tttapyc
"""

# try:
#Usage:
#    pmfind-docopt.py [options] (-i|--infile=FILE)
#Options:
#    -s SEP, --separator=SEP  separator for output records [default: tab]
#    -i FILE, --infile=FILE   read search terms from input file [default: stdin]

import os, sys
import docopt
from pmlib import pubmed_query

VERSION = '0.1'

def main():
    opts = docopt.docopt(__doc__, version=VERSION)

    #if opts['--separator'] == 'tab':
    #    opts['--separator'] = '\t'

    #if not opts['TERM'] and not opts['--infile']:
    #    for line in sys.stdin:
    #        opts['TERM'].append(line.strip())

    results = pubmed_query(opts['TERM'])

    if not results:
        print("No results. :-(", file=sys.stderr)
        sys.exit(1)

    for result in results:
        print(opts['--separator'].join(result))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nTerminating on interrupt.", file=sys.stderr)
