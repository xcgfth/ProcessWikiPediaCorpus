"""
Usage:
parse_wikipedia.py <wiki_file> <vocabulary_file> <out_file>
"""
from docopt import docopt
args = docopt(__doc__)
print("hello word")
wiki_file=args['<wiki_file>']
print(wiki_file, args['<vocabulary_file>'], args['<out_file>'])



# """
# Usage: test.py <file> [--verbose]
# """
# from docopt import docopt
# args=docopt(__doc__)
# print(args['<file>'])