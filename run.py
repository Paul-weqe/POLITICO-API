from politico_api.v2 import create_app
from config import Config

app = create_app(Config)

if __name__ == "__main__":
    app.run()
