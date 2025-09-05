from dashboard import app

# Exponha o servidor para o Gunicorn
server = app.server

if __name__ == "__main__":
    app.run_server(debug=False, host="0.0.0.0", port=8050)