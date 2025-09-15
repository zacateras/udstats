import os   
import csv
import re
import urllib.request
import tarfile
import ssl
from . import conll18_ud_eval_proxy as conll

def iterate_recursive(directory, pattern):
    cmpl = re.compile(pattern)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if cmpl.match(file):
                yield os.path.join(root, file)

def download(url, download_path='.'):
    file_name = url.split('/')[-1]
    file_path = os.path.join(download_path, file_name)

    context = ssl._create_unverified_context()
    with urllib.request.urlopen(url, context=context) as response, open(file_path, 'wb') as out_file:
        data = response.read()
        out_file.write(data)

    return file_path

def extract(archive_path, extract_path='.'):
    if archive_path.endswith("tar.gz") or archive_path.endswith("tgz"):
        tar = tarfile.open(archive_path, "r:gz")
        tar.extractall(extract_path)
        tar.close()
    elif archive_path.endswith("tar"):
        tar = tarfile.open(archive_path, "r:")
        tar.extractall(extract_path)
        tar.close()

    return os.path.join(extract_path, os.path.splitext(os.path.basename(archive_path))[0])

def flatten(input_conllu_directory, output_csv_file=None):
    if output_csv_file is None:
        output_csv_file = input_conllu_directory + '.csv'

    treebanks = list(iterate_recursive(input_conllu_directory, r'.+\.conllu$'))

    with open(output_csv_file, 'w+', newline='\n', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow([
            'lang',
            'tag',
            'ds_type',
            
            'sent',
            'token',
            
            'id', 
            'form', 
            'lemma',
            'upos',
            'xpos',
            'feats',
            'head',
            'deprel',
            'deps',
            'misc',

            # statistics
            'len_form',
            'len_lemma',
            'vdist_to_head',
            'hdist_to_root'
        ])

        treebank_i = 0
        sent_i = 0
        token_i = 0
        
        for treebank_file in treebanks:
            treebank = conll.load_conllu(treebank_file)

            print('Processing {}/{}, {}...'.format(treebank_i + 1, len(treebanks), treebank))

            for sent in treebank.sents:
                for token in sent.words:

                    vdist_to_head = abs(token.id - token.head)
                    hdist_to_root = 0

                    h = token.head
                    while h != 0:
                        h = sent[h - 1].head
                        hdist_to_root += 1

                    writer.writerow([
                        treebank.lang,
                        treebank.tag,
                        treebank.dataset_type,

                        sent_i,
                        token_i

                    ] + token.columns + [len(token.form), len(token.lemma), vdist_to_head, hdist_to_root])

                    token_i += 1

                sent_i += 1
                
            treebank_i += 1

    return output_csv_file
