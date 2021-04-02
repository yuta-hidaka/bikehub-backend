from django.core.management.base import BaseCommand

from django.db import connection


class Command(BaseCommand):
    def handle(self, **options):
        cursor = connection.cursor()
        cursor.execute('SHOW TABLES')
        
        results=[]

        for row in cursor.fetchall():
            results.append(row)
            
        for row in results:
            cursor.execute(f'ALTER TABLE {row[0]} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;')
        
        # for row in results:
        #     print(row)
        #     cursor.execute('ALTER TABLE %s CONVERT TO CHARACTER SET utf8mb4 COLLATE     utf8mb4_general_ci;' % (row[0]))