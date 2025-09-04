from dashboard import app

# Exponha o servidor para o Gunicorn
server = app.server

if __name__ == "__main__":
    app.run(debug=False)