import requests

def sync_cats_from_api(url: str):
    """Ejemplo de sincronización con API externa."""
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        data = response.json()
        # procesar y guardar en BD si se desea
        return data
    return None
