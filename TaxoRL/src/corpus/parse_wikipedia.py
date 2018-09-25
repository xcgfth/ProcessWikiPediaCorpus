"""
    Usage:
    parse_wikipedia.py <wiki_file> <vocabulary_file> <out_file>
"""
import codecs
import spacy
from collections import defaultdict




def main():
    from docopt import docopt
    args = docopt(__doc__)
    nlp = spacy.load('en')
    wiki_file = args['<wiki_file>']
    vocabulary_file = args['<vocabulary_file>']
    out_file = args['<out_file>']
    with codecs.open(vocabulary_file, 'r', 'utf-8') as f_in:
        vocabulary = set([line.strip() for line in f_in])
    with codecs.open(wiki_file, 'r', 'utf-8') as f_in:
        with codecs.open(out_file, 'w', 'utf_8') as f_out:
            for paragraph in f_in:
                paragraph = paragraph.strip()
                if len(paragraph) == 0:
                    continue
                parsed_par = nlp(paragraph)
                for sent in parsed_par.sents:
                    dependency_paths = parse_sentence(sent, vocabulary)
                    for (x, y), paths in dependency_paths.items():
                        for path in paths:
                            print('\t'.join([x, y, path]), file=f_out)


def parse_sentence(sent, vocabulary):
    # from nltk import Tree
    # def to_nltk_tree(node):
    #     if node.n_lefts + node.n_rights > 0:
    #         return Tree(node.orth_, [to_nltk_tree(child) for child in node.children])
    #     else:
    #         return node.orth_
    #
    # to_nltk_tree(sent.root).pretty_print()
    indices = [(token.lemma_, sent[i:i+1], i, i) for i, token in enumerate(sent) if len(token.orth_) > 2
               and token.lemma_ in vocabulary and token.pos_ in ['NOUN', 'VERB', 'ADJ']]
    indices.extend([(np.orth_, np, np.start, np.end) for np in sent.doc.noun_chunks
                   if sent.start <= np.start < np.end - 1 < sent.end and np.orth_ in vocabulary])
    tokens = [(x[0], x[1], y[0], y[1]) for x in indices for y in indices if x[3] < y[2]]
    paths = defaultdict(list)
    [paths[(x, y)].append(shortest_path((x_tokens, y_tokens))) for (x, x_tokens, y, y_tokens) in tokens]
    satellites = defaultdict(list)
    [satellites[(x, y)].extend([sat_path for path in paths[(x, y)] for sat_path in get_satellite_links(path)
                           if sat_path is not None]) for (x, y) in paths.keys()]
    filtered_paths = defaultdict(list)
    [filtered_paths[(x, y)].extend(filter(None, [pretty_print(set_x_l, x, set_x_r, hx, lch, hy, set_y_l, y, set_y_r)
                                                for (set_x_l, x, set_x_r, hx, lch, hy, set_y_l, y, set_y_r)
                                                in satellites[(x, y)]])) for x, y in satellites.keys()]
    return filtered_paths


def shortest_path(path):
    if path is None:
        return None
    x_tokens, y_tokens = path
    x_token = x_tokens.root
    y_token = y_tokens.root
    hx = heads(x_token)
    hy = heads(y_token)
    if hx == [] and x_token in hy:
        hy = hy[:hy.index(x_token)]
        hx = []
        lch = x_token
    elif hy == [] and y_token in hx:
        hx = hx[:hx.index(y_token)]
        hy = []
        lch = y_token
    elif len(hx) == 0 or len(hy) == 0:
        return None
    elif hy[0] != hx[0]:
        return None
    elif hx == hy:
        lch = hx[-1]
        hx = hy = []
    else:
        for i in range(min(len(hx), len(hy))):
            if hx[i] is not hy[i]:
                break
        if len(hx) > i:
            lch = hx[i - 1]
        elif len(hy) > i:
            lch = hy[i - 1]
        else:
            return None
        hx = hx[i + 1:]
        hy = hy[i + 1:]
    if lch and check_direction(lch, hx, lambda h: h.lefts):
        return None
    hx = hx[::-1]
    if lch and check_direction(lch, hy, lambda h: h.rights):
        return None
    return (x_token, hx, lch, hy, y_token)

def heads(token):
    t = token
    hs = []
    while t != t.head:
        t = t.head
        hs.append(t)
    return hs[::-1]

def check_direction(lch, hs, f_dir):
    return any(modifier not in f_dir(head) for head, modifier in zip([lch] + hs[:-1], hs))




def get_satellite_links(path):
    if path is None:
        return []
    x_tokens, hx, lch, hy, y_tokens = path
    paths = [(None, x_tokens, None, hx, lch, hy, None, y_tokens, None)]
    tokens_on_path = set([x_tokens] + hx + [lch] + hy + [y_tokens])
    set_xs = [(child, child.idx) for child in x_tokens.children if child not in tokens_on_path]
    set_ys = [(child, child.idx) for child in y_tokens.children if child not in tokens_on_path]
    x_index = x_tokens.idx
    y_index = y_tokens.idx

    for child, idx in set_xs:
        if child.tag_ != 'PUNCT' and len(child.string.strip()) > 1:
            if idx < x_index:
                paths.append((child, x_tokens, None, hx, lch, hy, None, y_tokens, None))
            else:
                paths.append((None, x_tokens, child, hx, lch, hy, None, y_tokens, None))

    for child, idx in set_ys:
        if child.tag_ != 'PUNCT' and len(child.string.strip()) > 1:
            if idx < y_index:
                paths.append((None, x_tokens, None, hx, lch, hy, child, y_tokens, None))
            else:
                paths.append((None, x_tokens, None, hx, lch, hy, None, y_tokens, child))

    return paths


def pretty_print(set_x_l, x, set_x_r, hx, lch, hy, set_y_l, y, set_y_r):
    set_path_x_l = []
    set_path_x_r = []
    set_path_y_l = []
    set_path_y_r = []
    lch_lst = []

    if set_x_l:
        set_path_x_l = [edge_to_string(set_x_l) + '/' + direction(SAT)]
    if set_x_r:
        set_path_x_r = [edge_to_string(set_x_r) + '/' + direction(SAT)]
    if set_y_l:
        set_path_y_l = [edge_to_string(set_y_l) + '/' + direction(SAT)]
    if set_y_r:
        set_path_y_r = [edge_to_string(set_y_r) + '/' + direction(SAT)]
    if lch == x:
        dir_x = direction(ROOT)
        dir_y = direction(DOWN)
    elif lch == y:
        dir_x = direction(UP)
        dir_y = direction(ROOT)
    else:
        lch_lst = [edge_to_string(lch, is_head=True) + '/' + direction(ROOT)] if lch else []
        dir_x = direction(UP)
        dir_y = direction(DOWN)
    len_path = len(hx) + len(hy) + len(set_path_x_r) + len(set_path_x_l) + len(set_path_y_r)+len(set_path_y_l) + len(lch_lst)
    if len_path <= MAX_PATH_LEN:
        cleaned_path = '_'.join(set_path_x_l + [argument_to_string(x, 'X') + '/' +dir_x] + set_path_x_r +
                                [edge_to_string(token)+ '/' + direction(UP) for token in hx ] + lch_lst +
                                [edge_to_string(token) + '/' + direction(DOWN) for token in hy] + set_path_y_l +
                                [argument_to_string(y, 'Y') + '/' +dir_y] + set_path_y_r
                                )
        return cleaned_path
    else:
        return None

def edge_to_string(t, is_head=False):
    return '/'.join([t.lemma_.strip().lower(), t.pos_, t.dep_ if t.dep_ != '' and not is_head else 'ROOT'])

def direction(dir):
    if dir == UP:
        return '>'
    elif dir == DOWN:
        return '<'
    elif dir == 'SAT':
        return 'V'
    else:
        return '^'

def argument_to_string(token, edge_name):
    return '/'.join([edge_name, token.pos_, token.dep_ if token.dep_ != '' else 'ROOT'])


MAX_PATH_LEN = 4
ROOT = 0
UP = 1
DOWN = 2
SAT = 3


if __name__=='__main__':
    main()