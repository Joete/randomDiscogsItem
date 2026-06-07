#!/usr/bin/env python3
"""
pick_random.py
--------------
Ruft die Discogs-Collection des Users ab, wählt zufällig ein Release aus
und schreibt das Ergebnis als result.json ins Repo-Root.

Benötigt zwei Umgebungsvariablen (werden von der GitHub Action gesetzt):
  DISCOGS_CONSUMER_KEY
  DISCOGS_CONSUMER_SECRET
  DISCOGS_USERNAME

Lokaler Test:
  export DISCOGS_CONSUMER_KEY=xxx
  export DISCOGS_CONSUMER_SECRET=yyy
  export DISCOGS_USERNAME=Joete
  python scripts/pick_random.py
"""

import json
import os
import random
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT   = Path(__file__).parent.parent
RESULT_FILE = REPO_ROOT / "result.json"

DISCOGS_API = "https://api.discogs.com"
USER_AGENT  = "DiscogsRandomPick/1.0"


def auth_header() -> str:
    key    = os.environ["DISCOGS_CONSUMER_KEY"]
    secret = os.environ["DISCOGS_CONSUMER_SECRET"]
    return f'Discogs key="{key}", secret="{secret}"'


def get_json(url: str) -> dict:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent":    USER_AGENT,
            "Authorization": auth_header(),
        }
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode())


def fetch_collection(username: str) -> list[dict]:
    """Lädt alle Releases aus der Collection (paginiert)."""
    releases = []
    page = 1
    per_page = 100

    while True:
        url = (
            f"{DISCOGS_API}/users/{username}/collection/folders/0/releases"
            f"?page={page}&per_page={per_page}&sort=added&sort_order=desc"
        )
        data = get_json(url)
        releases.extend(data.get("releases", []))

        pagination = data.get("pagination", {})
        if page >= pagination.get("pages", 1):
            break
        page += 1

    return releases


def extract_info(release: dict) -> dict:
    """Extrahiert die relevanten Felder aus einem Discogs-Release-Objekt."""
    info       = release.get("basic_information", {})
    artists    = info.get("artists", [])
    artist_str = ", ".join(a.get("name", "").strip() for a in artists)

    # Bestes Cover-Bild wählen
    images     = info.get("cover_image", "")
    thumb      = info.get("thumb", "")

    return {
        "id":           release.get("id"),
        "discogs_id":   info.get("id"),
        "title":        info.get("title", ""),
        "artist":       artist_str,
        "year":         info.get("year"),
        "cover_image":  images or thumb,
        "thumb":        thumb,
        "genres":       info.get("genres", []),
        "styles":       info.get("styles", []),
        "label":        info.get("labels", [{}])[0].get("name", "") if info.get("labels") else "",
        "discogs_url":  f"https://www.discogs.com/release/{info.get('id')}",
    }


def main() -> None:
    username = os.environ.get("DISCOGS_USERNAME", "Joete")

    print(f"→ Lade Collection von @{username} …")
    releases = fetch_collection(username)

    if not releases:
        raise ValueError("Keine Releases in der Collection gefunden.")

    chosen  = random.choice(releases)
    info    = extract_info(chosen)

    result = {
        "generated_at":   datetime.now(timezone.utc).isoformat(),
        "total_in_collection": len(releases),
        "result": info,
    }

    with RESULT_FILE.open("w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"✓ result.json → \"{info['artist']} – {info['title']}\" ({info['year']})")


if __name__ == "__main__":
    main()
