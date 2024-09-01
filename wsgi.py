from main import app
from flask_cors import CORS

cors = CORS(app, origins=['http://localhost:3000'])

if __name__ == "__main__":
    app.run(host = "0.0.0.0" , port = 5000)
