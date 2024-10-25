from flask import Flask

app = Flask(__name__)

@app.route("/")
def root_welcomeapi():
    return "welcome to Flask"

if __name__ == '__main__':
   app.run(port=5000)

# pip install Flask