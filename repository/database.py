import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "worldcup.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS teams (
    team_id  INTEGER PRIMARY KEY,
    name     TEXT NOT NULL UNIQUE,
    coach    TEXT
);
CREATE TABLE IF NOT EXISTS players (
    player_id  INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    position   TEXT,
    team_id    INTEGER NOT NULL REFERENCES teams(team_id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS matches (
    match_id      INTEGER PRIMARY KEY,
    home_team_id  INTEGER NOT NULL REFERENCES teams(team_id) ON DELETE CASCADE,
    away_team_id  INTEGER NOT NULL REFERENCES teams(team_id) ON DELETE CASCADE,
    match_date    TEXT,
    venue         TEXT,
    home_score    INTEGER,
    away_score    INTEGER,
    CHECK (home_team_id <> away_team_id)
);
"""


def get_connection(path: Path = DB_PATH) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def init_db(con: sqlite3.Connection) -> None:
    con.executescript(SCHEMA)
