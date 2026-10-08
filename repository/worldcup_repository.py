import sqlite3
from abc import ABC, abstractmethod

from models import Player, Match, Team


class IWorldCupRepository(ABC):
    @abstractmethod
    def get_player(self, p: Player) -> Player | None:
        pass

    @abstractmethod
    def upsert_player(self, p: Player) -> None:
        pass

    @abstractmethod
    def delete_player(self, p: Player) -> None:
        pass

    @abstractmethod
    def get_team(self, t: Team) -> Team | None:
        pass

    @abstractmethod
    def upsert_team(self, t: Team) -> None:
        pass

    @abstractmethod
    def delete_team(self, t: Team) -> None:
        pass

    @abstractmethod
    def get_match(self, m: Match) -> Match | None:
        pass

    @abstractmethod
    def upsert_match(self, m: Match) -> None:
        pass

    @abstractmethod
    def delete_match(self, m: Match) -> None:
        pass

    @abstractmethod
    def get_match_for_given_team(self, t: Team) -> list[Match]:
        pass

    @abstractmethod
    def get_match_for_given_player(self, p: Player) -> list[Match]:
        pass


class WorldCupRepository(IWorldCupRepository):
    def __init__(self, sqldb: sqlite3.Connection) -> None:
        self._sqldb = sqldb

    def get_player(self, p: Player) -> Player | None:
        row = self._sqldb.execute(
            "SELECT * FROM players WHERE player_id = ?", (p.player_id,)
        ).fetchone()
        return Player.from_row(row) if row else None

    def upsert_player(self, p: Player) -> None:
        with self._sqldb:
            self._sqldb.execute(
                """
                INSERT INTO players (player_id, name, position, team_id)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(player_id) DO UPDATE SET
                    name = excluded.name,
                    position = excluded.position,
                    team_id = excluded.team_id
                """,
                (p.player_id, p.name, p.position, p.team_id),
            )

    def delete_player(self, p: Player) -> None:
        with self._sqldb:
            self._sqldb.execute(
                "DELETE FROM players WHERE player_id = ?", (p.player_id,)
            )

    def get_team(self, t: Team) -> Team | None:
        row = self._sqldb.execute(
            "SELECT * FROM teams WHERE team_id = ?", (t.team_id,)
        ).fetchone()
        return Team.from_row(row) if row else None

    def upsert_team(self, t: Team) -> None:
        with self._sqldb:
            self._sqldb.execute(
                """
                INSERT INTO teams (team_id, name, coach)
                VALUES (?, ?, ?)
                ON CONFLICT(team_id) DO UPDATE SET
                    name = excluded.name,
                    coach = excluded.coach
                """,
                (t.team_id, t.name, t.coach),
            )

    def delete_team(self, t: Team) -> None:
        with self._sqldb:
            self._sqldb.execute("DELETE FROM teams WHERE team_id = ?", (t.team_id,))

    def get_match(self, m: Match) -> Match | None:
        row = self._sqldb.execute(
            "SELECT * FROM matches WHERE match_id = ?", (m.match_id,)
        ).fetchone()
        return Match.from_row(row) if row else None

    def upsert_match(self, m: Match) -> None:
        with self._sqldb:
            self._sqldb.execute(
                """
                INSERT INTO matches (match_id, home_team_id, away_team_id,
                                     match_date, venue, home_score, away_score)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(match_id) DO UPDATE SET
                    home_team_id = excluded.home_team_id,
                    away_team_id = excluded.away_team_id,
                    match_date = excluded.match_date,
                    venue = excluded.venue,
                    home_score = excluded.home_score,
                    away_score = excluded.away_score
                """,
                (
                    m.match_id,
                    m.home_team_id,
                    m.away_team_id,
                    m.match_date,
                    m.venue,
                    m.home_score,
                    m.away_score,
                ),
            )

    def delete_match(self, m: Match) -> None:
        with self._sqldb:
            self._sqldb.execute("DELETE FROM matches WHERE match_id = ?", (m.match_id,))

    def get_match_for_given_team(self, t: Team) -> list[Match]:
        rows = self._sqldb.execute(
            """
            SELECT * FROM matches
            WHERE home_team_id = :team_id OR away_team_id = :team_id
            ORDER BY match_date
            """,
            {"team_id": t.team_id},
        ).fetchall()
        return [Match.from_row(r) for r in rows]

    def get_match_for_given_player(self, p: Player) -> list[Match]:
        rows = self._sqldb.execute(
            """
            SELECT m.* FROM matches m
            JOIN players p ON p.team_id IN (m.home_team_id, m.away_team_id)
            WHERE p.player_id = ?
            ORDER BY m.match_date
            """,
            (p.player_id,),
        ).fetchall()
        return [Match.from_row(r) for r in rows]
