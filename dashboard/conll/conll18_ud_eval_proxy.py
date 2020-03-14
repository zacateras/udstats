import os
from . import conll18_ud_eval as conll
from . import vocab 
from typing import List, Mapping
from enum import Enum

class UDWord:
    def __init__(self, columns):
        """
        10 columns of CoNLL-U file: ID, FORM, LEMMA,...
        """
        self.columns = columns

    def __str__(self):
        return self.form

    def __repr__(self):
        return self.__str__()

    @property
    def id(self):
        return int(self.columns[conll.ID])

    @id.setter
    def id(self, value):
        self.columns[conll.ID] = str(value)

    @property
    def form(self):
        return self.columns[conll.FORM]

    @form.setter
    def form(self, value):
        self.columns[conll.FORM] = value

    @property
    def lemma(self):
        return self.columns[conll.LEMMA]

    @lemma.setter
    def lemma(self, value):
        self.columns[conll.LEMMA] = value

    @property
    def upos(self):
        return self.columns[conll.UPOS]

    @upos.setter
    def upos(self, value):
        self.columns[conll.UPOS] = value

    @property
    def xpos(self):
        return self.columns[conll.XPOS]

    @xpos.setter
    def xpos(self, value):
        self.columns[conll.XPOS] = value

    @property
    def feats(self):
        return self.columns[conll.FEATS].split('|')

    @feats.setter
    def feats(self, value):
        self.columns[conll.FEATS] = '|'.join(value)

    @property
    def head(self):
        return int(self.columns[conll.HEAD])

    @head.setter
    def head(self, value):
        self.columns[conll.HEAD] = str(value)

    @property
    def deprel(self):
        return self.columns[conll.DEPREL]

    @deprel.setter
    def deprel(self, value):
        self.columns[conll.DEPREL] = value

    @property
    def deps(self):
        return self.columns[conll.DEPS]

    @deps.setter
    def deps(self, value):
        self.columns[conll.DEPS] = value

    @property
    def misc(self):
        return self.columns[conll.MISC]

    @misc.setter
    def misc(self, value):
        self.columns[conll.MISC] = value

    @property
    def is_multiword(self):
        return False

class UDRoot(UDWord):
    def __init__(self):
        super(UDRoot, self).__init__(None)

    @property
    def id(self):
        return 0

    @property
    def form(self):
        return vocab.ROOT

    @property
    def lemma(self):
        return vocab.ROOT

    @property
    def upos(self):
        return vocab.ROOT

    @property
    def xpos(self):
        return vocab.ROOT

    @property
    def feats(self):
        return []

    @property
    def head(self):
        # CoNLL file words point to ROOT at 0 position
        return 0

    @property
    def deprel(self):
        return vocab.ROOT

    @property
    def deps(self):
        return vocab.ROOT

    @property
    def misc(self):
        return vocab.ROOT

    @property
    def is_multiword(self):
        return False

class CoNLLWord(UDWord):
    def __init__(self, word):
        super(CoNLLWord, self).__init__(word.columns)
        
        self._word = word

class UDSentence:
    def __init__(self, words: List[UDWord]):
        self._words = words

    def __str__(self):
        return ' '.join(map(lambda x: x.form, self._words))

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self._words)

    def __getitem__(self, key):
        return self._words[key]

    @property
    def words(self):
        return self._words

    def with_root(self):
        return UDSentence([UDRoot()] + self._words)

    @staticmethod  
    def from_UDRepresentation(tb):
        sents = []
        last: int = 0
        words: List[UDWord] = []

        for word in tb.words:
            word = CoNLLWord(word)

            if word.id <= last:
                sents.append(UDSentence(words))
                words = []
            
            last = word.id
            words.append(word)

        return sents
            
class CoNLLFile:
    def __init__(self, name, sents, vocabs, lang=None, tag=None, dataset_type=None):
        self._name = name
        self._sents = sents
        self._vocabs = vocabs
        self._lang = lang
        self._tag = tag
        self._dataset_type = dataset_type

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'ud_treebank, {}, {}, {}'.format(self._lang, self._tag, self._dataset_type)

    @property
    def name(self):
        return self._name
    
    @property
    def sents(self):
        return self._sents

    @property
    def vocabs(self):
        return self._vocabs

    @property
    def lang(self):
        return self._lang

    @property
    def tag(self):
        return self._tag

    @property
    def dataset_type(self):
        return self._dataset_type

def write_conllu(file, sents: List[UDSentence]):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with open(file, 'w+', encoding='utf-8') as f:
        for sent in sents:
            # foreach word except root
            for word in sent.words[1:]:
                f.write('\t'.join(str(column) for column in word.columns) + '\n')

            f.write('\n')

def load_conllu(file, is_path=True, name=None, lang=None, tag=None, dataset_type=None):
    UDR = _just_load_conllu(file, is_path)

    if is_path:
        if name is None:
            name = os.path.basename(file)

            lang, tag = name.split('-')[0].split('_')
            dataset_type = name.split('-')[2].split('.')[0]

    vocabs = vocab.from_UDRepresentation(UDR)
    sents = UDSentence.from_UDRepresentation(UDR)

    return CoNLLFile(name, sents, vocabs, lang=lang, tag=tag, dataset_type=dataset_type)

def _just_load_conllu(file, is_path=True):
    file = str(file)

    if  is_path:
        assert os.path.exists(file)
        assert file.endswith('.conllu')

        return conll.load_conllu_file(file)

    else:
        return conll.load_conllu(file)
