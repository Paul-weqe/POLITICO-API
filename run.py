from politico_api.v1 import create_app
from config import Config

app = create_app(Config)
app.run()

