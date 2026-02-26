#!/usr/bin/env python3
"""
A framework for a simple command-line program using Click for input
argument parsing, that plays nicely inside a Unix pipeline.

This toy example queries the PubMed index of scientific literature for
recent publications matching one or more keywords supplied as arguments.

Example usage:

  $ pmfind smoking
  $ pmfind breast cancer
  $ pmfind < keyword_list.txt > results.tsv
  $ echo "term1 term2 term3" | pmfind

Author: Kevin Ernst
Date:   14 May 2020
"""
import sys
import click
from pmlib import pubmed_query

VERSION = 0.1

@click.command()
@click.argument('terms', metavar='TERM', nargs=-1, required=True)
@click.version_option(VERSION)
#@click.option('-i', '--infile', metavar='FILE'
#        help="Read search terms from an input file")
#@click.option('-s', '--separator', metavar='SEP'
#        help="Separator for output records (default: tab")
def main(terms):  # ,infile, separator)
    """
    Search PubMed for given TERM(s) and return a list of URLs and titles
    from the first page of search results.
    """
    # ^^^ this docstring will be used as the help for this click.command()

    results = pubmed_query(terms)

    if not results:
        print("No results. :-(", file=sys.stderr)
        sys.exit(1)

    for result in results:
        print('\t'.join(result))

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt):
        click.echo("\nTerminating on interrupt.", err=True)
