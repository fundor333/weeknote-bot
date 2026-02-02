import logging
import os

import requests
from rich.logging import RichHandler

LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


FORMAT = "%(message)s"
logging.basicConfig(
    level=LOG_LEVEL, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


def hardcover_shelf(
    my_token: str, section_label: str = "Books I'm reading"
) -> str:
    return get_currently_reading(my_token, section_label=section_label)


def get_currently_reading(
    api_token, section_label: str = "Books I'm reading"
) -> str:
    # Endpoint ufficiale GraphQL di Hardcover
    url = "https://api.hardcover.app/v1/graphql"

    # Header richiesti per l'autenticazione
    headers = {"authorization": api_token, "Content-Type": "application/json"}

    # Query per i libri in lettura (status_id: 2) con URL copertina
    query = """
    query {
      me {
        user_books(where: {status_id: {_eq: 2}}) {
          book {
            title
            image {
              url
            }
          }
        }
      }
    }
    """
    output = "\n## " + section_label + "\n\n"

    # Invio della richiesta POST
    response = requests.post(url, json={"query": query}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        books = data.get("data", {}).get("me", [{}])[0].get("user_books", [])

        if not books:
            log.info("Nessun libro in fase di lettura trovato.")
            return ""

        log.info("--- Libri che sto leggendo ---")
        for entry in books:
            book = entry["book"]
            title = book.get("title")
            author = book.get("author_name")
            # Recupera l'URL della copertina se disponibile
            cover_url = (
                book.get("image", {}).get("url") if book.get("image") else None
            )

            log.debug(f"Titolo: {title}")
            log.debug(f"Autore: {author}")
            log.debug(f"Copertina: {cover_url}")
            log.debug("-" * 30)

            if cover_url:
                output += f"![{title}]({cover_url})  \n"
    else:
        log.info(f"Errore nella richiesta: {response.status_code}")
        log.info(response.text)

    return output
