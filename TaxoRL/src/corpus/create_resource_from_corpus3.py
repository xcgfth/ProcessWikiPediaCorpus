"""
Usage:
    create_resource_from_corpus3.py <id_triplet_file> <resource_prefix>
"""
from bsddb3 import db
import codecs
from collections import defaultdict

from tqdm import  tqdm

def main():
    from docopt import  docopt
    args = docopt(__doc__)
    id_triplet_file = args['<id_triplet_file>']
    resource_prefix = args['<resource_prefix>']
    l2r_db = db.DB()
    l2r_db.open(resource_prefix + '_l2r.db', None, db.DB_HASH, db.DB_CREATE)
    l2r_dict = defaultdict(str)
    with codecs.open(id_triplet_file) as f_in:
        for ct, line in tqdm(enumerate(f_in)):
            try:
                x, y, path, count = line.strip().split('\t')
            except:
                # print(line)
                continue
            key = '%s###%s' % (x, y)
            current = '%s:%s' % (path, count)
            l2r_dict[key] += current + ','
    for k, v in l2r_dict.items():
        l2r_db[bytes(k, 'utf-8')] = v.rstrip(',')
    l2r_db.close()

if __name__ == '__main__':
    main()