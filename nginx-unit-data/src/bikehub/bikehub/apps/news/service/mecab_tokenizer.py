# -*- coding: utf-8 -*-
import MeCab
from pysummarization.tokenizable_doc import TokenizableDoc


class MeCabTokenizer(TokenizableDoc):
    """
    Tokenize string.
    copy from from pysummarization.tokenizabledoc.mecab_tokenizer import MeCabTokenizer


    Japanese morphological analysis with MeCab.
    """

    # Path ot mecab dictionary.
    # For instance, '-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd'.
    # If empty(''), this class will see default settings.
    __mecab_system_dic = ''

    def get_mecab_system_dic(self):
        """ getter """
        return self.__mecab_system_dic

    def set_mecab_system_dic(self, value):
        """ setter """
        self.__mecab_system_dic = value

    mecab_system_dic = property(get_mecab_system_dic, set_mecab_system_dic)

    __part_of_speech = ['名詞', '形容詞', '動詞']

    def get_part_of_speech(self):
        """ getter """
        return self.__part_of_speech

    def set_part_of_speech(self, value):
        """ setter """
        self.__part_of_speech = value

    part_of_speech = property(get_part_of_speech, set_part_of_speech)

    def tokenize(self, sentence_str):
        """
        Tokenize str.

        Args:
            sentence_str:   tokenized string.

        Returns:
            [token, token, token, ...]
        """
        if len(self.part_of_speech) == 0:
            mt = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
            wordlist = mt.parse(sentence_str)
            token_list = wordlist.rstrip(' \n').split(' ')
            return token_list
        else:
            tagger = MeCab.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
            node = tagger.parseToNode(sentence_str)

            token_list = []
            while node:
                feature_list = node.feature.split(',')
                if feature_list[0] != 'BOS/EOS':
                    if feature_list[0] in self.part_of_speech:
                        token = feature_list[6]
                        token_list.append(token)
                node = node.next
            return token_list
