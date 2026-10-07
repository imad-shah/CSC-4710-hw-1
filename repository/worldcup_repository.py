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
    def get_team(self, t: Team) -> Team:
        pass

    @abstractmethod
    def upsert_team(self, t: Team) -> None:
        pass

    @abstractmethod
    def delete_team(self, t: Team) -> None:
        pass

    @abstractmethod
    def get_match(self, m: Match) -> Match:
        pass

    @abstractmethod
    def upsert_match(self, m: Match) -> None:
        pass

    @abstractmethod
    def delete_match(self, m: Match) -> None:
        pass

    @abstractmethod
    def get_match_for_given_team(self, t: Team) -> Match:
        pass

    @abstractmethod
    def get_match_for_given_player(self, p: Player) -> Match:
        pass


class WorldCupRepository(IWorldCupRepository):
    def __init__(self, sqldb) -> None:
        self._sqldb = sqldb

    def get_player(self, p: Player) -> Player | None:
        cursor = self._sqldb.cursor()
        cursor.execute("""SELECT player from Players WHERE player.name == p.name""")
        row = cursor.fetchone()
        if not row:
            return None
        return Player(*row)

    def upsert_player(self, p: Player) -> None:
        cursor = self._sqldb.cursor()
        cursor.execute(""""
    INSERT INTO users (id, name, email)
    VALUES (?, ?, ?)
    ON CONFLICT(id) 
    DO UPDATE SET 
        name = excluded.name,
        email = excluded.email;
        """)
        row = cursor.fetchone()
        if not row:
            return None
        return Player(*row)

    def delete_player(self, p: Player) -> None:
        pass

    def get_team(self, t: Team) -> Team:
        pass

    def upsert_team(self, t: Team) -> None:
        pass

    def delete_team(self, t: Team) -> None:
        pass

    def get_match(self, m: Match) -> Match:
        pass

    def upsert_match(self, m: Match) -> None:
        pass

    def delete_match(self, m: Match) -> None:
        pass

    def get_match_for_given_team(self, t: Team) -> Match:
        pass

    def get_match_for_given_player(self, p: Player) -> Match:
        pass


"""
upsert_query = '''
    INSERT INTO users (id, name, email)
    VALUES (?, ?, ?)
    ON CONFLICT(id) 
    DO UPDATE SET 
        name = excluded.name,
        email = excluded.email;
"""
