import os
import conll
import sys

ud_version_uri = {
    'v2.5': 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3105/ud-treebanks-v2.5.tgz',
    'v2.4': 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2988/ud-treebanks-v2.4.tgz',
    'v2.3': 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2895/ud-treebanks-v2.3.tgz',
    'v2.2': 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2837/ud-treebanks-v2.2.tgz',
    'v2.1': 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-2515/ud-treebanks-v2.1.tgz',
    'v2.0': 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-1983/ud-treebanks-v2.0.tgz'
}

if __name__ == "__main__":
    if len(sys.argv) == 1:
        pass
    elif len(sys.argv) == 3:
        ud_version_uri = { sys.argv[1]: sys.argv[2] }
    else:
        print('Wrong number of arguments. Usage:\n$ python run.py [ud_version ud_url]')
        exit(-1)

    if not os.path.exists(conll.process.TMP_DIR):
        os.mkdir(conll.process.TMP_DIR)

    print ('Working directory: %s' % conll.process.TMP_DIR)
    os.chdir(conll.process.TMP_DIR)

    for version, uri in ud_version_uri.items():
        print('Processing %s.' % version)

        print('Downloading %s...' % uri)
        archive_path = conll.process.download(uri)

        print('Extracting %s...' % archive_path)
        input_conllu_directory = conll.process.extract(archive_path)

        print('Flattening %s...' % input_conllu_directory)
        output_csv_file = conll.process.flatten(input_conllu_directory)