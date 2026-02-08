from dataclasses import dataclass, field
from enum import Enum

# --- Enums ---


class MatchResult(Enum):
    WIN = "W"
    DRAW = "D"
    LOSS = "L"


class ConferenceType(Enum):
    PRE_MATCH = "Pre-Match"
    POST_MATCH = "Post-Match"
    TRANSFER_WINDOW = "Transfer Window"
    CRISIS = "Crisis"
    BIG_SIGNING = "Big Signing"
    RIVALRY_PREVIEW = "Rivalry Preview"


class JournalistPersonality(Enum):
    TABLOID_HOSTILE = "tabloid_hostile"
    TABLOID_SENSATIONALIST = "tabloid_sensationalist"
    BROADSHEET_NEUTRAL = "broadsheet_neutral"
    BROADSHEET_SUPPORTIVE = "broadsheet_supportive"
    LOCAL_PRESS_FRIENDLY = "local_press_friendly"


class BoardConfidence(Enum):
    FULL = "full confidence"
    SATISFIED = "satisfied"
    WAVERING = "wavering"
    UNDER_PRESSURE = "under pressure"
    ON_THE_BRINK = "on the brink of sacking"


class PlayerMorale(Enum):
    SUPERB = "superb"
    HAPPY = "happy"
    CONTENT = "content"
    UNHAPPY = "unhappy"
    FURIOUS = "furious"


# --- Core Dataclasses ---


@dataclass
class MatchRecord:
    opponent: str
    home: bool
    score: str  # e.g. "2-1"
    result: MatchResult
    competition: str


@dataclass
class Injury:
    player_name: str
    injury_type: str
    weeks_out: int
    is_key_player: bool


@dataclass
class Player:
    name: str
    position: str
    age: int
    is_captain: bool = False
    is_star_player: bool = False
    morale: PlayerMorale = PlayerMorale.CONTENT
    transfer_rumour: str | None = None  # e.g. "linked with Chelsea"
    goals: int = 0
    assists: int = 0


@dataclass
class Rivalry:
    opponent: str
    rivalry_type: str  # e.g. "local derby", "historical grudge", "title race"
    description: str


@dataclass
class Club:
    name: str
    nickname: str
    founded: int
    stadium: str
    capacity: int
    honours: list[str] = field(default_factory=list)
    recent_seasons: list[str] = field(
        default_factory=list
    )  # e.g. ["2023-24: 15th", "2022-23: 17th"]
    rivalries: list[Rivalry] = field(default_factory=list)


@dataclass
class Manager:
    name: str
    age: int
    nationality: str
    tenure_months: int
    board_confidence: BoardConfidence
    media_reputation: str  # e.g. "combative", "media-savvy", "reserved"
    previous_clubs: list[str] = field(default_factory=list)
    win_percentage: float = 0.0


@dataclass
class Journalist:
    name: str
    outlet: str
    personality: JournalistPersonality
    relationship_with_manager: (
        str  # e.g. "hostile after leaked story", "respects the manager"
    )


@dataclass
class LeagueStanding:
    position: int
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int
    points: int


@dataclass
class UpcomingMatch:
    opponent: str
    competition: str
    home: bool
    significance: str  # e.g. "local derby", "must-win relegation battle"


@dataclass
class PostMatchContext:
    opponent: str
    score: str
    result: MatchResult
    notable_events: list[str] = field(
        default_factory=list
    )  # e.g. ["Red card for Onana 65'"]


@dataclass
class TransferContext:
    window: str  # "summer" or "january"
    incoming: list[str] = field(default_factory=list)
    outgoing: list[str] = field(default_factory=list)
    rumoured: list[str] = field(default_factory=list)
    budget_remaining: str = ""
    new_signing: str | None = None  # for BIG_SIGNING type


@dataclass
class GameState:
    """Root container for all game-world data needed by the press conference."""

    club: Club
    manager: Manager
    squad: list[Player]
    injuries: list[Injury]
    journalists: list[Journalist]
    league_standing: LeagueStanding
    recent_form: list[MatchRecord]
    conference_type: ConferenceType

    # Situational — only one of these is populated depending on conference_type
    upcoming_match: UpcomingMatch | None = None
    post_match: PostMatchContext | None = None
    transfer: TransferContext | None = None
