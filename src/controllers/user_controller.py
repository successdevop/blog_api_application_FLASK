from src import create_app

app = create_app()

@app.route("/")
def homepage():
    return "Welcome to Nkata Blog Application"

@app.route("/register", methods=["POST"])
def register_user():
    pass