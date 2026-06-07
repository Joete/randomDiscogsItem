# Discogs Random Pick · GitHub Pages

Wählt 3× täglich automatisch ein zufälliges Album aus der Discogs-Collection und stellt es als JSON-Endpunkt auf GitHub Pages bereit.

---

## Endpunkt

```
https://<username>.github.io/<repo>/result.json
```

```json
{
  "generated_at": "2026-06-03T04:00:00+00:00",
  "total_in_collection": 342,
  "result": {
    "id": 123456,
    "discogs_id": 789012,
    "title": "Kind of Blue",
    "artist": "Miles Davis",
    "year": 1959,
    "cover_image": "https://i.discogs.com/...",
    "thumb": "https://i.discogs.com/...",
    "genres": ["Jazz"],
    "styles": ["Modal", "Hard Bop"],
    "label": "Columbia",
    "discogs_url": "https://www.discogs.com/release/789012"
  }
}
```

---

## Setup

### 1. Repo anlegen & pushen

```bash
git init
git add .
git commit -m "init: discogs random pick"
git remote add origin https://github.com/DEIN-USERNAME/REPO.git
git branch -M main
git push -u origin main
```

### 2. GitHub Secrets anlegen ⚠️

Repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name               | Wert                          |
|---------------------------|-------------------------------|
| `DISCOGS_CONSUMER_KEY`    | dein Consumer Key von discogs.com/settings/developers |
| `DISCOGS_CONSUMER_SECRET` | dein Consumer Secret          |
| `DISCOGS_USERNAME`        | dein Discogs-Username         |

### 3. Workflow-Permissions setzen

Repo → **Settings → Actions → General → Workflow permissions → Read and write permissions** ✓

### 4. GitHub Pages aktivieren

Repo → **Settings → Pages → Source: Deploy from branch → main / (root)**

### 5. Ersten Run starten

Repo → **Actions → Discogs Random Pick → Run workflow**

---

## Neue Credentials generieren (empfohlen)

Falls du Consumer Key/Secret irgendwo geteilt hast:
[discogs.com/settings/developers](https://www.discogs.com/settings/developers) → Token/App widerrufen → neu generieren → Secrets in GitHub aktualisieren.

---

## Lokaler Test

```bash
export DISCOGS_CONSUMER_KEY=xxx
export DISCOGS_CONSUMER_SECRET=yyy
export DISCOGS_USERNAME=Joete
python scripts/pick_random.py
```
