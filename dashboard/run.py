import os
import conll

ud_version_uri = {
    'v2.5': 'https://lindat.mff.cuni.cz/repository/xmlui/bitstream/handle/11234/1-3105/ud-treebanks-v2.5.tgz'
}

if __name__ == "__main__":
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