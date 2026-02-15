from models import GameState


def build_system_prompt(state: GameState) -> str:
    sections = [
        _role(state),
        _club(state),
        _manager(state),
        _squad(state),
        _journalists(state),
        _conference(state),
        _rules(),
    ]
    return "\n\n".join(sections)


# --- Sections ---


def _role(state: GameState) -> str:
    return (
        "You are a panel of football journalists at a press conference.\n"
        f"The manager of {state.club.name} is sitting in front of you.\n"
        "You ask questions one at a time. After the manager replies, "
        "the next journalist asks their question.\n"
        "Each message you send is exactly ONE journalist asking ONE question."
    )


def _club(state: GameState) -> str:
    c = state.club
    ls = state.league_standing

    lines = [
        "# Club",
        f"{c.name} ({c.nickname}), est. {c.founded}",
        f"Stadium: {c.stadium} ({c.capacity:,} capacity)",
    ]

    if c.honours:
        lines.append(f"Honours: {'; '.join(c.honours)}")
    if c.recent_seasons:
        lines.append(f"Recent seasons: {'; '.join(c.recent_seasons)}")

    lines.append(
        f"\nLeague: {ls.position}th — P{ls.played} W{ls.won} D{ls.drawn} "
        f"L{ls.lost} GF{ls.goals_for} GA{ls.goals_against} Pts {ls.points}"
    )

    if state.recent_form:
        form = ", ".join(
            f"{m.result.value} {m.score} {'(H)' if m.home else '(A)'} vs {m.opponent}"
            for m in state.recent_form
        )
        lines.append(f"Recent form (latest first): {form}")

    if c.rivalries:
        for r in c.rivalries:
            lines.append(f"Rivalry: {r.opponent} ({r.rivalry_type}) — {r.description}")

    return "\n".join(lines)


def _manager(state: GameState) -> str:
    m = state.manager
    lines = [
        "# Manager",
        f"{m.name}, {m.age}, {m.nationality}",
        f"In charge {m.tenure_months} months, win rate {m.win_percentage}%",
        f"Board confidence: {m.board_confidence.value}",
        f"Media reputation: {m.media_reputation}",
    ]
    if m.previous_clubs:
        lines.append(f"Previous clubs: {', '.join(m.previous_clubs)}")
    return "\n".join(lines)


def _squad(state: GameState) -> str:
    lines = ["# Squad"]

    for p in state.squad:
        parts = [f"{p.name} ({p.position}, {p.age})"]
        if p.is_captain:
            parts.append("CAPTAIN")
        if p.is_star_player:
            parts.append("star player")
        if p.morale.value not in ("content", "happy"):
            parts.append(f"morale: {p.morale.value}")
        if p.goals or p.assists:
            parts.append(f"{p.goals}G {p.assists}A")
        if p.transfer_rumour:
            parts.append(f"RUMOUR: {p.transfer_rumour}")
        lines.append("- " + " | ".join(parts))

    if state.injuries:
        lines.append("\nInjuries:")
        for inj in state.injuries:
            key = " (KEY PLAYER)" if inj.is_key_player else ""
            lines.append(
                f"- {inj.player_name}: {inj.injury_type}, {inj.weeks_out} weeks out{key}"
            )

    return "\n".join(lines)


def _journalists(state: GameState) -> str:
    lines = ["# Journalists in the room"]
    for j in state.journalists:
        lines.append(
            f"- {j.name} ({j.outlet}) — {j.personality.value}. "
            f"Relationship: {j.relationship_with_manager}"
        )
    return "\n".join(lines)


def _conference(state: GameState) -> str:
    lines = [f"# Conference type: {state.conference_type.value}"]

    if state.upcoming_match:
        um = state.upcoming_match
        venue = "Home" if um.home else "Away"
        lines.append(
            f"Next match: {um.opponent} ({um.competition}, {venue}). {um.significance}"
        )

    if state.post_match:
        pm = state.post_match
        lines.append(f"Just played: {pm.result.value} {pm.score} vs {pm.opponent}")
        if pm.notable_events:
            lines.append(f"Events: {'; '.join(pm.notable_events)}")

    if state.transfer:
        t = state.transfer
        lines.append(f"Window: {t.window}")
        if t.new_signing:
            lines.append(f"New signing: {t.new_signing}")
        if t.incoming:
            lines.append(f"Incoming: {', '.join(t.incoming)}")
        if t.outgoing:
            lines.append(f"Outgoing: {', '.join(t.outgoing)}")
        if t.rumoured:
            lines.append(f"Rumoured: {', '.join(t.rumoured)}")
        if t.budget_remaining:
            lines.append(f"Budget remaining: {t.budget_remaining}")

    return "\n".join(lines)


def _rules() -> str:
    return (
        "# Rules\n"
        "- Ask 5-8 questions total, then end the conference.\n"
        "- Rotate between journalists. Don't let one dominate.\n"
        "- Match each journalist's personality and tone to their profile.\n"
        "- React to the manager's answers: follow up if they dodge, "
        "acknowledge good answers, escalate if provoked.\n"
        "- Build tension through the conference, don't front-load hard questions.\n"
        "- Only reference facts from the context above. Never invent results, "
        "players, or events.\n"
        "- Format: **Name (Outlet):** question\n"
        "- After the final question, write [END OF PRESS CONFERENCE].\n"
        "- Never break character. You are journalists, not an AI assistant."
    )
