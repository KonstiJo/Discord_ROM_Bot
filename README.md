# Discord_ROM_Bot

Discord-Bot auf Basis von [discord.py](https://github.com/Rapptz/discord.py) mit Slash-Commands,
Nutzungs-Logging und einem einfachen Keep-Alive-Webserver, damit der Bot auf Free-Hosting-Plattformen
nicht einschläft.

## Tech-Stack

- **Python 3** + `discord.py` (Slash-Commands über `app_commands.CommandTree`)
- **python-dotenv** für Secrets (`.env`, nicht eingecheckt)
- **Flask** (`keep_alive.py`) – minimaler HTTP-Server auf Port `8080`, der auf `GET /` antwortet,
  damit ein externer Uptime-Monitor den Prozess am Leben halten kann

## Befehle (Slash-Commands)

| Befehl | Beschreibung |
|---|---|
| `/dm` | Schickt dem aufrufenden Nutzer eine Test-DM, um zu prüfen, ob private Nachrichten erreichbar sind |
| `/rom-list` | Zeigt einen Zustimmungs-Dialog (Buttons „I agree" / „I disagree") und sendet bei Zustimmung eine Datei per DM |
| `/time` | Gibt zurück, wann der aufrufende Nutzer dem Server beigetreten ist |
| `/info` | Embed mit Server-Historie, Bot-Uptime, Version und Entwickler-Info |

Slash-Commands werden beim Start nur für die konfigurierte Guild (`GUILD_ID`) synchronisiert
(`setup_hook` → `tree.copy_global_to` + `tree.sync`), nicht global.

## Logging & Statistik

- `log_command()` schreibt jede Befehlsnutzung mit Zeitstempel und Nutzername nach `logs/command_log.txt`
- `count_command()` führt einen persistenten Zähler pro Befehl in `counters/usage_count.json`
- Beide Verzeichnisse werden beim Start automatisch angelegt (`os.makedirs(..., exist_ok=True)`)

## Konfiguration

Secrets liegen in einer lokalen `.env`-Datei (per `python-dotenv` geladen) und werden **nicht**
committet:

```env
DISCORD_TOKEN=
```

Die Ziel-Guild ist aktuell als Konstante (`GUILD_ID`) direkt in `bot.py` hinterlegt.

## Struktur

| Datei | Zweck |
|---|---|
| `bot.py` | Bot-Setup, alle Slash-Commands, Logging/Counter-Logik |
| `keep_alive.py` | Flask-Server im eigenen Thread für Uptime-Monitoring |
| `requirements.txt` | Abhängigkeiten |
| `usage_count.json` | Persistenter Zähler pro Befehl (wird zur Laufzeit geschrieben) |

## Starten

```bash
pip install -r requirements.txt
python bot.py
```

Voraussetzung: gültiger Bot-Token in `.env` sowie passende Intents/Berechtigungen in der Guild.
