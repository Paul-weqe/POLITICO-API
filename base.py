from politico_api.v2.models.DBConnections.BaseConnectionDb import BaseConnection

base = BaseConnection(DB_NAME="politico_test", DB_PASSWORD='4ndel4', DB_USER='weqe', DB_HOST='localhost')
base.reset_database()