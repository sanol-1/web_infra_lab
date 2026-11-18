import getpass
from fabric import Connection, Config

KEY_FILE = '/home/sanol-1/.ssh/id_ed25519'
DB_NAME = 'lab_db'

passphrase = getpass.getpass('SSH key passphrase: ')

config = Config(overrides={'sudo': {'password': 'pass123'},
                           'run': {'in_stream': False},
})
connection = Connection(
    host='127.0.0.1',
    port=2211,                      # web-01
    user='ubuntu',
    config=config,
    connect_kwargs={'key_filename': KEY_FILE, 'passphrase': passphrase},
)


def install_mysql():
    connection.sudo('apt-get update -qq')
    connection.sudo('env DEBIAN_FRONTEND=noninteractive apt-get install -y mysql-server')
    connection.sudo('service mysql start')


def create_database():
    connection.sudo(f'mysql -e "CREATE DATABASE IF NOT EXISTS {DB_NAME};"')


def load_dump():
    connection.put('dump.sql', '/tmp/dump.sql')
    connection.sudo(f'mysql {DB_NAME} -e "source /tmp/dump.sql"')


def verify():
    connection.sudo(f'mysql {DB_NAME} -e "SHOW TABLES;"')


if __name__ == '__main__':
    install_mysql()
    create_database()
    load_dump()
    verify()
