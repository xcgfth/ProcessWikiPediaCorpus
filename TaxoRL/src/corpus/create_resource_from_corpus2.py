"""
    Usage:
    create_from_resource_corpus2.py <triplet_file> <resource_prefix>
"""

from bsddb3 import db
import codecs
def main():
    from docopt import docopt
    args = docopt(__doc__)
    triplet_file = args['<triplet_file>']
    resource_prefix = args['<resource_prefix>']
    # print("hello")
    print(triplet_file)
    # print(resource_prefix)
    term_to_id_db = db.DB()
    term_to_id_db.open(resource_prefix + '_term_to_id.db', None, db.DB_HASH, db.DB_DIRTY_READ)
    path_to_id_db = db.DB()
    path_to_id_db.open(resource_prefix + '_path_to_id.db', None, db.DB_HASH, db.DB_DIRTY_READ)

    with codecs.open(triplet_file) as f_in:
        with codecs.open(triplet_file + '_id', 'w') as f_out:
            for line in f_in:
                try:
                    x, y, path = line.strip().split('\t')
                except:
                    continue
                x_id, y_id, path_id = term_to_id_db[bytes(x, 'utf-8')], term_to_id_db[bytes(y, 'utf-8')], path_to_id_db.get(bytes(path, 'utf-8'), -1)
                print(path_id)
                if path_id != -1:
                    print('\t'.join(map(str, (x_id, y_id, path_id))), file=f_out)

if __name__ == '__main__':
    main()