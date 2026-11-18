from app import app, agencia
from dados import salvar_dados


if __name__ == "__main__":
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        salvar_dados(agencia)