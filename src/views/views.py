"""Consola simple para consumir la API de aprendices."""

import os

import requests

API_URL = os.getenv("API_BASE_URL", "https://fast-api-97xd.onrender.com").rstrip("/")

# campo de la API -> texto que se muestra al usuario
FIELDS = {
    "document": "Documento",
    "firstname": "Nombre",
    "lastname": "Apellido",
    "email": "Correo",
    "age": "Edad",
    "program": "Programa",
    "record_number": "Numero de ficha",
}


# ---------- pedir datos ----------


def ask_field(key, label, required=True):
    """Pide un dato hasta que sea valido. Si no es obligatorio, Enter lo omite."""
    while True:
        value = input(f"{label}: ").strip()

        if not value and not required:
            return None
        if not value:
            print("Este campo es obligatorio.")
            continue
        if key == "age" and not value.isdigit():
            print("La edad debe ser un numero.")
            continue

        return int(value) if key == "age" else value


def ask_create_data():
    return {key: ask_field(key, label) for key, label in FIELDS.items()}


def ask_update_data():
    print("Enter para dejar un campo sin cambios.")
    data = {key: ask_field(key, label, required=False) for key, label in FIELDS.items()}
    return {key: value for key, value in data.items() if value is not None}


def ask_id():
    while True:
        trainee_id = input("ID del aprendiz: ").strip()
        if trainee_id:
            return trainee_id
        print("El ID del aprendiz es obligatorio.")


# ---------- hablar con la API ----------


def send_request(method, path="", data=None):
    """Envia la peticion. Devuelve la respuesta o None si no hay conexion."""
    try:
        return requests.request(method, f"{API_URL}{path}", json=data, timeout=10)
    except requests.RequestException as exc:
        print(f"No se pudo conectar con la API: {exc}")
        return None


# ---------- mostrar resultados ----------


def print_trainee(trainee):
    print("-" * 30)
    print(f"ID: {trainee.get('id') or trainee.get('_id')}")
    for key, label in FIELDS.items():
        print(f"{label}: {trainee.get(key)}")


def show_result(response):
    if response is None:
        return

    if response.status_code >= 400:
        print(f"Error {response.status_code}: {response.text}")
        return

    try:
        data = response.json()
    except ValueError:
        print(response.text)
        return

    if isinstance(data, list):
        for trainee in data:
            print_trainee(trainee)
        print(f"\nTotal: {len(data)}")
    elif isinstance(data, dict) and "firstname" in data:
        print_trainee(data)
    else:
        print(data)


# ---------- opciones del menu ----------


def create_trainee():
    show_result(send_request("POST", "/trainees", ask_create_data()))


def list_trainees():
    show_result(send_request("GET", "/trainees"))


def get_trainee():
    show_result(send_request("GET", f"/trainees/{ask_id()}"))


def update_trainee():
    trainee_id = ask_id()
    data = ask_update_data()

    if not data:
        print("No escribiste ningun cambio.")
        return

    show_result(send_request("PUT", f"/trainees/{trainee_id}", data))


def delete_trainee():
    trainee_id = ask_id()

    if input("Seguro que quieres eliminarlo? (s/n): ").strip().lower() != "s":
        print("Cancelado.")
        return

    show_result(send_request("DELETE", f"/trainees/{trainee_id}"))


def show_home():
    show_result(send_request("GET", "/"))


# ---------- menu ----------

OPTIONS = {
    "1": ("Inicio de la API", show_home),
    "2": ("Crear aprendiz", create_trainee),
    "3": ("Listar aprendices", list_trainees),
    "4": ("Buscar por ID", get_trainee),
    "5": ("Actualizar aprendiz", update_trainee),
    "6": ("Eliminar aprendiz", delete_trainee),
}


def print_menu():
    print("\n=== GESTION DE APRENDICES ===")
    for key, (label, _) in OPTIONS.items():
        print(f"{key}. {label}")
    print("0. Salir")


def main():
    print(f"API: {API_URL}")
    while True:
        print_menu()
        choice = input("Elige una opcion: ").strip()

        if choice == "0":
            print("Hasta luego!")
            break

        if choice in OPTIONS:
            OPTIONS[choice][1]()
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()
