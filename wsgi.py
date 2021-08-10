from app import app
from art import *

if __name__ == "__main__":
    tprint("ZJUN PCD")
    init(loadLocal=True)
    app.run(host='0.0.0.0')