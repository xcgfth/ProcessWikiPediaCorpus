"""
    Usage:
    python3 create_resource_from_corpus1.py <frequent_paths_file> <terms_file> <resource_prefix>
"""
import codecs
from bsddb3 import db



def main():
    from docopt import docopt
    args = docopt(__doc__)
    frequent_paths_file = args['<frequent_paths_file>']
    terms_file = args['<terms_file>']
    resource_file = args['<resource_prefix>']
    print(frequent_paths_file, '\t\n', terms_file, '\t\n', resource_file)
    print('saving the paths...')
    with codecs.open(frequent_paths_file, 'r', 'utf-8') as f_in:
        frequent_paths = set([line.strip() for line in f_in])
    path_to_id = {path: i for i, path in enumerate(list(frequent_paths))}

    path_to_id_db = db.DB()
    path_to_id_db.open(resource_file + '_path_to_id.db', None, db.DB_HASH, db.DB_CREATE)
    id_to_path_db = db.DB()
    id_to_path_db.open(resource_file + '_id_to_path.db', None, db.DB_HASH, db.DB_CREATE)
    for path, id_ in path_to_id.items():
        id_, path = bytes(str(id_), 'utf-8'), bytes(path, 'utf-8')
        path_to_id_db.put(path, id_)
        id_to_path_db.put(id_, path)
    path_to_id_db.close()
    id_to_path_db.close()



    print('Saving the terms')
    with codecs.open(terms_file, 'r', 'utf-8') as f_in:
        terms = [line.strip() for line in f_in]
    term_to_id = {term: i for i, term in enumerate(terms)}
    term_to_id_db = db.DB()
    term_to_id_db.open(resource_file + '_term_to_id.db', None, db.DB_HASH, db.DB_CREATE)
    id_to_term_db = db.DB()
    id_to_term_db.open(resource_file + '_id_to_term.db', None, db.DB_HASH, db.DB_CREATE)
    for term, id_ in term_to_id.items():
        id_, term = str(id_) .encode('utf-8'), term.encode('utf-8')
        term_to_id_db.put(term, id_)
        id_to_term_db.put(id_, term)
    term_to_id_db.close()
    id_to_term_db.close()

if __name__ == '__main__':
    main()