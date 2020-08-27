# -*- coding: utf-8 -*-
# ! /usr/bin/python
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib
import os.path
import nlp_tasks

from sklearn.neural_network import MLPClassifier  # アルゴリズムとしてmlpを使用


def train():
    classifier = MyMLPClassifier()
    classifier.train('corpus.csv')


def predict():
    classifier = MyMLPClassifier()
    classifier.load_model()
    result = classifier.predict(u"Home\
                                新車・インプレ, 新車ニュース, 編集部おすすめ【新車】カワサキ、オフロード競技専用「KLX230R」のカラー＆グラフィックを変更し8/1に発売\
                                【新車】カワサキ、オフロード競技専用「KLX230R」のカラー＆グラフィックを変更し8/1に発売\
                                2020/7/10 17: 40新車・インプレ, 新車ニュース, 編集部おすすめKLX230R, カワサキ, バイク\
                                カワサキモータースジャパンは、2021年モデルとなるオフロード競技専用モデル「KLX230R」を8月1日（土）に発売することを発表した。主な変更点はカラー＆グラフィックの変更。\
\
                                KLX230Rは、誰もが本格的なオフロードライディングを楽しめるように開発。新設計のエンジンとフレームは、オフロードでの楽しさを追求している。空冷4ストローク232cm3単気筒エンジンは低中回転域からの力強いトルクを生み出し、シンプルな構造でオフロード走破に理想的な設計。そして、コンパクトなペリメターフレームは、オフロードライディングでの操縦安定性を実現している。\
                                さらに、余裕あるロードクリアランスとロングストロークサスペンションも、高いオフロード性能に貢献。また、エンジンとフレームのバランスは、幅広いライダーが楽しめるように設定されている。\
                                外観は、KXシリーズを踏襲し、人間工学に基づきマシンコントロール性が高いスリムさとアグレッシブなデザインを採用。加えて、軽量な樹脂製タンク、アルミニウム製スイングアームなど、兄弟モデルのKLX230から各所がアップグレードされ、より軽量な車体（115kg）、より大きなサスペンションストローク（フロント：250mm／リヤ：251mm）、より余裕あるロードクリアランス（300mm）をもっている。\
                                フロント21インチ、リヤ18インチのホイールを装備したこの新しいオフロード専用モデルは、軽量、パワフル、扱いやすさを兼ね備え、オフロードアドベンチャーに最適な1台だ。")
    print(result)


class MyMLPClassifier():
    model = None
    model_name = "mlp"

    def load_model(self):
        if os.path.exists(self.get_model_path()) == False:
            raise Exception('no model file found!')
        self.model = joblib.load(self.get_model_path())
        self.classes = joblib.load(self.get_model_path('class')).tolist()
        self.vectorizer = joblib.load(self.get_model_path('vect'))
        self.le = joblib.load(self.get_model_path('le'))

    def get_model_path(self, type='model'):
        return 'models/'+self.model_name+"_"+type+'.pkl'

    def get_vector(self, text):
        return self.vectorizer.transform([text])

    def train(self, csvfile):
        df = pd.read_csv(csvfile, names=('text', 'category'))
        X, vectorizer = nlp_tasks.get_vector_by_text_list(df["text"])

        # loading labels
        le = LabelEncoder()
        le.fit(df['category'])
        Y = le.transform(df['category'])

        model = MLPClassifier(
            max_iter=300, hidden_layer_sizes=(100,), verbose=10,)
        model.fit(X, Y)

        # save models
        joblib.dump(model, self.get_model_path())
        joblib.dump(le.classes_, self.get_model_path("class"))
        joblib.dump(vectorizer, self.get_model_path("vect"))
        joblib.dump(le, self.get_model_path("le"))

        self.model = model
        self.classes = le.classes_.tolist()
        self.vectorizer = vectorizer

    def predict(self, query):
        X = self.vectorizer.transform([query])
        key = self.model.predict(X)
        return self.classes[key[0]]


if __name__ == '__main__':
    # train()
    predict()
