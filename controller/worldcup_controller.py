import sqlite3
from abc import ABC, abstractmethod
from datetime import date

from models import Player, Match, Team
from repository import IWorldCupRepository

from .errors import AppError


class IWorldCupController(ABC):
    @abstractmethod
    def save_player(
        self, player_id: str, name: str, position: str, team_id: str
    ) -> Player:
        pass

    @abstractmethod
    def delete_player(self, player_id: str) -> None:
        pass

    @abstractmethod
    def save_team(self, team_id: str, name: str, coach: str) -> Team:
        pass

    @abstractmethod
    def delete_team(self, team_id: str) -> None:
        pass

    @abstractmethod
    def save_match(
        self,
        match_id: str,
        home_team_id: str,
        away_team_id: str,
        match_date: str,
        venue: str,
        home_score: str,
        away_score: str,
    ) -> Match:
        pass

    @abstractmethod
    def delete_match(self, match_id: str) -> None:
        pass

    @abstractmethod
    def list_players(self) -> list[Player]:
        pass

    @abstractmethod
    def list_teams(self) -> list[Team]:
        pass

    @abstractmethod
    def list_matches(self) -> list[Match]:
        pass

    @abstractmethod
    def matches_for_team(self, team_id: str) -> list[Match]:
        pass

    @abstractmethod
    def matches_for_player(self, player_id: str) -> list[Match]:
        pass


def _text(value: str) -> str | None:
    """Strip an entry's text, treating blank as None."""
    return value.strip() or None


def _int(value: str, field: str) -> int | None:
    """Parse an optional integer field; blank means None."""
    text = _text(value)
    if text is None:
        return None
    try:
        return int(text)
    except ValueError:
        raise AppError(f"{field} must be a whole number.") from None


def _required_int(value: str, field: str) -> int:
    number = _int(value, field)
    if number is None:
        raise AppError(f"{field} is required.")
    return number


def _required_text(value: str, field: str) -> str:
    text = _text(value)
    if text is None:
        raise AppError(f"{field} is required.")
    return text


class WorldCupController(IWorldCupController):
    def __init__(self, repo: IWorldCupRepository) -> None:
        self._repo = repo

    def save_player(
        self, player_id: str, name: str, position: str, team_id: str
    ) -> Player:
        player = Player(
            name=_required_text(name, "Player name"),
            team_id=self._existing_team_id(team_id),
            position=_text(position),
            # Blank ID means a new player; SQLite assigns one.
            player_id=_int(player_id, "Player ID"),
        )
        self._repo.upsert_player(player)
        return player

    def delete_player(self, player_id: str) -> None:
        self._repo.delete_player(self._existing_player_id(player_id))

    def save_team(self, team_id: str, name: str, coach: str) -> Team:
        team = Team(
            name=_required_text(name, "Team name"),
            coach=_text(coach),
            team_id=_required_int(team_id, "Team ID"),
        )
        try:
            self._repo.upsert_team(team)
        except sqlite3.IntegrityError:
            raise AppError(f"A team named '{team.name}' already exists.") from None
        return team

    def delete_team(self, team_id: str) -> None:
        self._repo.delete_team(self._existing_team_id(team_id))

    def save_match(
        self,
        match_id: str,
        home_team_id: str,
        away_team_id: str,
        match_date: str,
        venue: str,
        home_score: str,
        away_score: str,
    ) -> Match:
        match = Match(
            match_date=_text(match_date),
            venue=_text(venue),
            match_id=_required_int(match_id, "Match ID"),
            home_team_id=self._existing_team_id(home_team_id, "Home team ID"),
            away_team_id=self._existing_team_id(away_team_id, "Away team ID"),
            home_score=_int(home_score, "Home score"),
            away_score=_int(away_score, "Away score"),
        )
        if match.home_team_id == match.away_team_id:
            raise AppError("A team can't play against itself.")
        if match.match_date is not None:
            try:
                date.fromisoformat(match.match_date)
            except ValueError:
                raise AppError("Match date must be YYYY-MM-DD.") from None
        self._repo.upsert_match(match)
        return match

    def delete_match(self, match_id: str) -> None:
        self._repo.delete_match(self._existing_match_id(match_id))

    def list_players(self) -> list[Player]:
        return self._repo.list_players()

    def list_teams(self) -> list[Team]:
        return self._repo.list_teams()

    def list_matches(self) -> list[Match]:
        return self._repo.list_matches()

    def matches_for_team(self, team_id: str) -> list[Match]:
        return self._repo.get_match_for_given_team(self._existing_team_id(team_id))

    def matches_for_player(self, player_id: str) -> list[Match]:
        return self._repo.get_match_for_given_player(
            self._existing_player_id(player_id)
        )

    def _existing_player_id(self, value: str) -> int:
        player_id = _required_int(value, "Player ID")
        if self._repo.get_player(player_id) is None:
            raise AppError(f"No player with ID {player_id}.")
        return player_id

    def _existing_team_id(self, value: str, field: str = "Team ID") -> int:
        team_id = _required_int(value, field)
        if self._repo.get_team(team_id) is None:
            raise AppError(f"No team with ID {team_id}.")
        return team_id

    def _existing_match_id(self, value: str) -> int:
        match_id = _required_int(value, "Match ID")
        if self._repo.get_match(match_id) is None:
            raise AppError(f"No match with ID {match_id}.")
        return match_id
