"""Create and get summary"""
import re

from news.models import News
from pysummarization.abstractabledoc.top_n_rank_abstractor import \
    TopNRankAbstractor
from pysummarization.nlp_base import NlpBase
from pysummarization.nlpbase.auto_abstractor import AutoAbstractor
from pysummarization.similarityfilter.tfidf_cosine import TfIdfCosine

from .find_content import FindContents
# from .find_tag import FindTag
from .mecab_tokenizer import MeCabTokenizer

"""追加"""


class Summary():

    def __init__(self):
        pass

    def create(self, document: str) -> str:
        processed_document = ''.join(document.split())

        nlp_base = NlpBase()
        nlp_base.tokenizable_doc = MeCabTokenizer()
        similarity_filter = TfIdfCosine()
        similarity_filter.nlp_base = nlp_base
        similarity_filter.similarity_limit = 0.25
        auto_abstractor = AutoAbstractor()
        meCab_tokenizer = MeCabTokenizer()
        auto_abstractor.tokenizable_doc = meCab_tokenizer
        abstractable_doc = TopNRankAbstractor()
        result_dict = auto_abstractor.summarize(
            processed_document, abstractable_doc, similarity_filter
        )

        summaries = []
        summaries.extend(
            re.sub('\n.|\u3000．', '', data) for data in result_dict["summarize_result"]
        )
        return '\n'.join(summaries)

    def create_summary_from_all_news(self):
        fc = FindContents()
        # ft = FindTag()

        news_list = News.objects.all()
        for news in news_list:
            content_text = ''
            if news.site.is_there_another_source:
                content_text = fc.find_contents_by_tags(news.url)
            else:
                content_text = fc.find_contents(
                    news.url,
                    news.site.content_tag.tag_type,
                    news.site.content_tag.tag_class_name,
                    news.site.content_tag.tag_id_name
                )
            summary = self.create(content_text)
            news.summary = summary
            news.save()
