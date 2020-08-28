from django.core.management.base import BaseCommand
import json
from users.models import CustomUser
from fuel_consumption.models import Maker, Country, Eda, Bike, FuelType, Fc, FcComment
from allauth.account.models import EmailAddress


class Command(BaseCommand):
    def __init__(self):
        self.bike = None
        self.maker = None
        self.country = None
        self.user = None
        self.eda = None
        self.fc = None

    def handle(self, **options):
        with open('/code/bike_nenpi.json') as json_file:
            # print(json_file)
            data = json.load(json_file)
            # print(type(data))
            # print(data.keys())

            for d in data:
                # print(d)

                keys = d.keys()
                if 'name' in keys:
                    n = d['name']
                    if n == '':
                        print("empty")
                    elif n == 'maker_table':
                        self.maker = d['data']
                    elif n == 'user_table':
                        self.user = d['data']
                    elif n == 'country_table':
                        self.country = d['data']
                    elif n == 'eda_table':
                        self.eda = d['data']
                    elif n == 'bike_table':
                        self.bike = d['data']
                    elif n == 'fc_table':
                        self.fc = d['data']

            self.create_country()
            self.create_eda()
            self.create_maker()
            self.create_user()
            self.create_bike()
            self.create_fc()
            self.add_email_allauth_email()

    def create_user(self):
        for u in self.user:

            if u['regist_date']:
                u['regist_date'] = u['regist_date'].replace('/', '-', 2)
                u['regist_date'] = u['regist_date'].replace('/', ' ')

            if u['update_time']:
                u['update_time'] = u['update_time'].replace('/', '-', 2)
                u['update_time'] = u['update_time'].replace('/', ' ')

            if u['login_date']:
                u['login_date'] = u['login_date'].replace('/', '-', 2)
                u['login_date'] = u['login_date'].replace('/', ' ')

            print('create user')

            try:
                i = CustomUser.objects.create_user(
                    email=u['mail_add'],
                    username=u['mail_add'],
                    password=u['password'],
                    disp_name=u['user_name'],
                    birthday=u['birthday'],
                    gender=u['gender'],
                    # 自由入力で自分のバイクを保存
                    ubike1=u['ubike1'] if u['ubike1'] else '',
                    ubike2=u['ubike2'] if u['ubike2'] else '',
                    # 外部参照から自分のバイクを取得
                    accept=True,
                    login_date=u['login_date'],
                    # login_cnt=u[''],
                    created_at=u['regist_date'],
                    updated_at=u['update_time'],
                )
            except Exception as e:
                # print(e)
                i = CustomUser.objects.get(email=u['mail_add'])
                pass
            id = u['user_id']
            name = u['user_name']

            for num in range(len(self.bike)):
                if self.bike[num]['fc_max_user_name'] == '退会ユーザー':
                    self.bike[num]['fc_max_user_name'] = None

                elif self.bike[num]['fc_max_user_name'] == name:
                    # print(self.bike[num]['fc_max_user_name'] + 'を以下に変更')
                    self.bike[num]['fc_max_user_name'] = i
                    # print(self.bike[num]['fc_max_user_name'])

                else:
                    # print(str(self.bike[num]['fc_max_user_name']) + 'をNoneに変更')
                    self.bike[num]['fc_max_user_name'] = None

            for num in range(len(self.fc)):
                if self.fc[num]['user_id'] == id:
                    # print(self.fc[num]['user_id'] + 'を以下に変更')
                    self.fc[num]['user_id'] = i
                    # print(self.fc[num]['user_id'])

            # print(type(i))

        d = self.user

    def create_fc(self):
        print("create fc")
        ft = ['ガソリン', 'ハイオク']
        g = []
        for f in ft:
            n, k = FuelType.objects.get_or_create(
                fuel=f
            )
            g.append(n)
        d = self.fc
        for l in d:
            if l['fuel'] == 'ガソリン':
                l['fuel'] = g[0]
            else:
                l['fuel'] = g[1]

            if l['fc_regist_time']:
                l['fc_regist_time'] = l['fc_regist_time'].replace('/', '-')

            if l['update_time'] == '17:50.0':
                l['update_time'] = '2020-03-22 17:17:50.0'
            if l['update_time']:
                l['update_time'] = l['update_time'].replace('/', '-')

            o, r = Fc.objects.get_or_create(
                fc=l['fc'],
                model_year=l['model_year'],
                city_ride=l['city_ride'],
                high_way_ride=l['high_way_ride'],
                fc_comment=l['fc_comment'],
                fc_good=l['fc_good'],
                fc_user_official=l['fc_user_official'],
                fuel_type=l['fuel'],
                bike=l['bike_id'],
                user=l['user_id'],
                created_at=l['fc_regist_time'],
                updated_at=l['update_time']
            )

    def create_bike(self):
        print("create bike")
        d = self.bike
        for l in d:
            # print(l)
            o, r = Bike.objects.get_or_create(
                bike_name=l['bike_name'],
                engine_displacement=l['engine_displacement'],
                engine_displacement_area=l['engine_displacement_area_id'],
                maker=l['maker_id'],
                fc_max=l['fc_max'],
                fc_ave=l['fc_ave'],
                fc_max_user_name=l['fc_max_user_name'],
                tag=l['tag']
            )

            id = l['bike_id']

            for vvv in range(len(self.fc)):
                if self.fc[vvv]['bike_id'] == id:
                    self.fc[vvv]['bike_id'] = o

    def create_maker(self):
        print("create maker")
        d = self.maker

        for l in d:
            o, r = Maker.objects.get_or_create(
                country=l['country_id'],
                maker_name_en=l['maker_name_en'],
                maker_name_jp=l['maker_name_jp']
            )

            id = l['maker_id']

            for num in range(len(self.bike)):
                if self.bike[num]['maker_id'] == id:
                    # print(self.bike[num]['maker_id'])
                    self.bike[num]['maker_id'] = o
                    # print(self.bike[num]['maker_id'])

    def create_eda(self):
        print("create eda")
        d = self.eda

        for l in d:
            o, r = Eda.objects.get_or_create(
                engine_displacement_area=l['engine_displacement_area']
            )

            id = l['engine_displacement_area_id']

            for num in range(len(self.bike)):
                if self.bike[num]['engine_displacement_area_id'] == id:
                    self.bike[num]['engine_displacement_area_id'] = o

    def create_country(self):
        print("create country")
        d = self.country

        for l in d:
            # print("c作成")
            o, r = Country.objects.get_or_create(
                country=l['country']
            )
            # print("c週施用")

            id = l['country_id']

            for num in range(len(self.maker)):
                if self.maker[num]['country_id'] == id:
                    # print('置き換えた')
                    self.maker[num]['country_id'] = o
                    # print(self.maker[num]['country_id'])

    def create_fuel_type(self):
        d = self.bike


    def add_email_allauth_email(self):
        print("adding Email")
        users = CustomUser.objects.all()

        for user in users:
            EmailAddress.objects.get_or_create(
                user= user,
                email= user.email,
                verified = True,
                primary = True
            )
