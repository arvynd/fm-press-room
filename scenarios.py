from models import (
    BoardConfidence,
    Club,
    ConferenceType,
    GameState,
    Injury,
    Journalist,
    JournalistPersonality,
    LeagueStanding,
    Manager,
    MatchRecord,
    MatchResult,
    Player,
    PlayerMorale,
    Rivalry,
    UpcomingMatch,
)


def losing_streak_crisis() -> GameState:
    """Everton in freefall. Five straight losses, board wavering, captain
    dropped after a dressing-room bust-up, tabloids circling. Merseyside
    derby up next."""

    club = Club(
        name="Everton",
        nickname="The Toffees",
        founded=1878,
        stadium="Goodison Park",
        capacity=39_414,
        honours=[
            "9x First Division Champions",
            "5x FA Cup Winners",
            "1x European Cup Winners' Cup",
        ],
        recent_seasons=[
            "2023-24: 15th (points deduction, narrowly survived relegation)",
            "2022-23: 17th (survived on final day)",
            "2021-22: 16th (survived on final day)",
        ],
        rivalries=[
            Rivalry(
                opponent="Liverpool",
                rivalry_type="local derby",
                description="The Merseyside derby. Everton haven't beaten Liverpool "
                "at Anfield since 1999. The rivalry has become increasingly "
                "one-sided, which makes it even more painful for Everton fans.",
            ),
        ],
    )

    manager = Manager(
        name="Sean Dyche",
        age=53,
        nationality="English",
        tenure_months=22,
        board_confidence=BoardConfidence.WAVERING,
        media_reputation="combative and no-nonsense, known for blunt press conferences",
        previous_clubs=["Burnley (7 years)", "Watford"],
        win_percentage=31.2,
    )

    squad = [
        Player(
            "Jordan Pickford",
            "GK",
            30,
            is_captain=False,
            is_star_player=True,
            morale=PlayerMorale.UNHAPPY,
        ),
        Player(
            "Séamus Coleman",
            "RB",
            35,
            is_captain=True,
            morale=PlayerMorale.FURIOUS,
            transfer_rumour="wants to leave after bust-up with manager",
        ),
        Player("James Tarkowski", "CB", 31, morale=PlayerMorale.CONTENT),
        Player(
            "Jarrad Branthwaite",
            "CB",
            21,
            is_star_player=True,
            morale=PlayerMorale.CONTENT,
            transfer_rumour="Manchester United bid rejected in summer, expected to return in January",
        ),
        Player("Vitalii Mykolenko", "LB", 25, morale=PlayerMorale.CONTENT),
        Player(
            "Amadou Onana",
            "CM",
            23,
            morale=PlayerMorale.UNHAPPY,
            transfer_rumour="linked with Arsenal and Bayern Munich",
        ),
        Player("Abdoulaye Doucouré", "CM", 31, morale=PlayerMorale.CONTENT),
        Player(
            "Dwight McNeil", "LW", 24, morale=PlayerMorale.HAPPY, goals=3, assists=4
        ),
        Player(
            "Dominic Calvert-Lewin",
            "ST",
            27,
            is_star_player=True,
            morale=PlayerMorale.UNHAPPY,
            goals=2,
        ),
        Player("Beto", "ST", 26, morale=PlayerMorale.CONTENT, goals=1),
    ]

    injuries = [
        Injury("Dominic Calvert-Lewin", "hamstring", weeks_out=3, is_key_player=True),
        Injury("Youssef Chermiti", "ankle", weeks_out=6, is_key_player=False),
    ]

    journalists = [
        Journalist(
            "Dave Hughes",
            "The Sun",
            JournalistPersonality.TABLOID_HOSTILE,
            "openly hostile — published leaked dressing room details last week",
        ),
        Journalist(
            "Sarah Mitchell",
            "The Guardian",
            JournalistPersonality.BROADSHEET_NEUTRAL,
            "fair but probing — will ask difficult tactical questions",
        ),
        Journalist(
            "Tom Richards",
            "Liverpool Echo",
            JournalistPersonality.LOCAL_PRESS_FRIENDLY,
            "sympathetic to the club but under pressure from editors to get headlines",
        ),
    ]

    league_standing = LeagueStanding(
        position=18,
        played=12,
        won=2,
        drawn=3,
        lost=7,
        goals_for=10,
        goals_against=22,
        points=9,
    )

    recent_form = [
        MatchRecord(
            "Chelsea",
            home=True,
            score="0-2",
            result=MatchResult.LOSS,
            competition="Premier League",
        ),
        MatchRecord(
            "Fulham",
            home=False,
            score="1-3",
            result=MatchResult.LOSS,
            competition="Premier League",
        ),
        MatchRecord(
            "Nottm Forest",
            home=True,
            score="0-1",
            result=MatchResult.LOSS,
            competition="Premier League",
        ),
        MatchRecord(
            "Man City",
            home=False,
            score="1-3",
            result=MatchResult.LOSS,
            competition="League Cup",
        ),
        MatchRecord(
            "Brentford",
            home=False,
            score="0-1",
            result=MatchResult.LOSS,
            competition="Premier League",
        ),
    ]

    upcoming_match = UpcomingMatch(
        opponent="Liverpool",
        competition="Premier League",
        home=False,
        significance="Merseyside derby at Anfield. Everton haven't won there since 1999. "
        "A loss could leave them bottom of the table.",
    )

    return GameState(
        club=club,
        manager=manager,
        squad=squad,
        injuries=injuries,
        journalists=journalists,
        league_standing=league_standing,
        recent_form=recent_form,
        conference_type=ConferenceType.CRISIS,
        upcoming_match=upcoming_match,
    )


# --- ADD YOUR SCENARIOS BELOW ---
# Use the losing_streak_crisis() above as a template.
# Some ideas:
#
# def rivalry_preview_derby() -> GameState:
#     """Tottenham before the North London derby. Arsenal top, you're 4th.
#     Star striker injured, backup untested."""
#
# def post_match_giant_killing() -> GameState:
#     """Wrexham beat Man Utd 2-1 in the FA Cup. Your goalscorer now
#     transfer-linked to Premier League clubs."""
#
# def big_summer_signing() -> GameState:
#     """Newcastle just signed a world-class striker for £80M.
#     Questions about FFP, who he displaces, dressing room dynamics."""


# Registry of all available scenarios — add yours here too
SCENARIOS: dict[str, tuple[str, callable]] = {
    "1": (
        "Everton in crisis — 5 straight losses, derby next, captain bust-up",
        losing_streak_crisis,
    ),
    # "2": ("Description here", your_function_here),
    # "3": ("Description here", your_function_here),
}
