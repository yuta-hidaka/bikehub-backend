import MeCab
from news.models import *


class FindTag:
    # 形態素解析で名詞のみを検索してタグとして返す
    @staticmethod
    def find_tag(text):
        tagger = MeCab.Tagger(
            '-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd'
        )
        response = []
        try:
            node = tagger.parseToNode(text)
            while node:
                if node.feature.split(',')[0] == '名詞':
                    response.append(node.surface.lower())
                node = node.next
        except Exception as e:
            print(e)
            return

        return response

    @staticmethod
    def create_tag(subTags):
        print('create tag')
        print(subTags)
        update_data = []
        insert_data = []
        response = []

        for subTag in subTags.itertuples(index=True, name='Pandas'):
            result = SubCategoryTag.objects.filter(
                name=subTag.tags
            ).first()

            print(subTag.counts)

            if result:
                result.tag_counter += subTag.counts
                update_data.append(result)
            else:
                tmp = SubCategoryTag(
                    name=subTag.tags,
                    tag_counter=subTag.counts,
                    main_category_tag_id=None
                )
                insert_data.append(tmp)

        if len(insert_data):
            r = SubCategoryTag.objects.bulk_create(
                insert_data
            )
            response.extend(r)

        if len(update_data):
            SubCategoryTag.objects.bulk_update(
                update_data, ['name', 'tag_counter']
            )
            response.extend(update_data)
        return response
