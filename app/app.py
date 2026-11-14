"""Aplicación web Flask de la calculadora."""

import os

from flask import Flask, render_template, request
from .calculadora import dividir, modulo, multiplicar, potencia, restar, sumar

app = Flask(__name__)

# Relaciona el valor del <select> con la función que realiza la operación
OPERACIONES = {
    "sumar": sumar,
    "restar": restar,
    "multiplicar": multiplicar,
    "dividir": dividir,
    "potencia": potencia,
    "modulo": modulo,
}


@app.route("/", methods=["GET", "POST"])
def index():
    """Muestra el formulario y, si es POST, calcula y muestra el resultado."""
    resultado = None
    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            funcion = OPERACIONES.get(request.form["operacion"])

            if funcion is None:
                resultado = "Operación no válida"
            else:
                resultado = funcion(num1, num2)
        except ValueError:
            resultado = "Error: Introduce números válidos"
        except ZeroDivisionError:
            resultado = "Error: No se puede dividir por cero"
        except OverflowError:
            resultado = "Error: El resultado es demasiado grande"

    return render_template("index.html", resultado=resultado)


@app.route("/health")
def health():
    """Health check usado por el Load Balancer. Incluye la versión desplegada."""
    return {"status": "ok", "version": os.environ.get("APP_VERSION", "local")}


if __name__ == "__main__":  # pragma: no cover
    app.run(port=5000)
