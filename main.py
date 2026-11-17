from app import app, iniciar_sistema

if __name__ == "__main__":
    iniciar_sistema()

    app.run(debug = True, use_reloader = False)