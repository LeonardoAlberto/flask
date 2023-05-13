import mysql.connector
import random
from datetime import datetime

db_database = {
    'user': 'admin',
    'password': 'Ladas2015',
    'host': 'database-1.crpptqrdm74l.us-east-1.rds.amazonaws.com',
    'database': 'database'
}


def add_user(nome, vencimento, numero, valor, plano, user):
    banco = mysql.connector.connect(**db_database)
    mycursor = banco.cursor()

    id = random.randint(111111, 999999)
    id = str(id)

    agora = str(datetime.now())
    horario_atual = agora.replace('-', '/').replace(' ', '-')[0:16]

    try:
        sql = "INSERT INTO {} Values(%s,%s,%s,%s,%s,%s,%s) ".format(user)
        val = (nome, vencimento, numero, valor, plano, id, horario_atual)
        mycursor.execute(sql, val)
        banco.commit()

        mycursor.close()
        banco.close()
        return True
    except:
        mycursor.close()
        banco.close()
        return False
