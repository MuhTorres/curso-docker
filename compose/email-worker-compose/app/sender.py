import psycopg2 as dbCon
import redis
import json
import os
from bottle import Bottle, request

class Sender(Bottle):
    def __init__(self):
        super().__init__()
        self.route('/', method='POST', callback=self.send)

        redis_host = os.getenv('REDIS_HOST', 'queue')
        self.fila = redis.StrictRedis(host=redis_host, port=6379, db=0)
        
        db_host = os.getenv('DB_HOST', 'db')
        db_user = os.getenv('DB_USER', 'postgres')
        db_pass = os.getenv('DB_PASS', '')
        db_name = os.getenv('DB_NAME', 'sender')

        # data source name
        DSN = f'dbname={db_name} user={db_user} password={db_pass} host={db_host}'
        self.connection = dbCon.connect(DSN)

    def register_message(self, assunto, mensagem):        
        SQL = 'INSERT INTO emails (assunto, mensagem) values (%s, %s)'
        cursor = self.connection.cursor()
        cursor.execute(SQL, (assunto, mensagem))
        self.connection.commit()
        cursor.close()

        msg = { 'assunto': assunto, 'mensagem': mensagem }
        self.fila.rpush('sender', json.dumps(msg))

        print('Mensagem registrada!')
    
    def send(self):
        assunto = request.forms.get('assunto')
        mensagem = request.forms.get('mensagem')

        self.register_message(assunto, mensagem)

        return 'Mensagem enfileirada! Assunto: {} Mensagem: {}'.format(
            assunto, mensagem
        )


if __name__ == '__main__':
    sender = Sender()
    sender.run(host='0.0.0.0', port=8080, debug=True)