import json
import os
import sys

import httpx
from rich.console import Console
from rich.panel import Panel

from prompts import build_system_prompt
from scenarios import SCENARIOS

GEMINI_MODEL = "gemini-2.0-flash"
GEMINI_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:streamGenerateContent"
)

console = Console()


def pick_scenario():
    console.print("\n[bold]Choose a scenario:[/bold]\n")
    for key, (description, _) in SCENARIOS.items():
        console.print(f"  [cyan]{key}[/cyan] — {description}")
    console.print()

    while True:
        choice = console.input("[bold]Pick a number:[/bold] ").strip()
        if choice in SCENARIOS:
            _, factory = SCENARIOS[choice]
            return factory()
        console.print("[red]Invalid choice, try again.[/red]")


def stream_response(api_key: str, system_prompt: str, contents: list[dict]) -> str:
    """Send a request to Gemini and stream the response. Returns full text."""
    body = {
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "contents": contents,
    }

    full_text = ""

    with httpx.Client(timeout=60) as client:
        with client.stream(
            "POST",
            GEMINI_URL,
            params={"alt": "sse", "key": api_key},
            json=body,
        ) as resp:
            if resp.status_code != 200:
                resp.read()
                console.print(f"[red]API error {resp.status_code}:[/red] {resp.text}")
                sys.exit(1)

            for line in resp.iter_lines():
                if not line.startswith("data: "):
                    continue
                chunk = json.loads(line[6:])
                candidates = chunk.get("candidates", [])
                if not candidates:
                    continue
                parts = candidates[0].get("content", {}).get("parts", [])
                for part in parts:
                    text = part.get("text", "")
                    if text:
                        console.print(text, end="", highlight=False)
                        full_text += text

    console.print()  # newline after streamed response
    return full_text


def run_conference(api_key: str, system_prompt: str):
    contents = [{"role": "user", "parts": [{"text": "Begin the press conference."}]}]

    while True:
        # Get journalist question
        console.print()
        response = stream_response(api_key, system_prompt, contents)
        contents.append({"role": "model", "parts": [{"text": response}]})

        if "[END OF PRESS CONFERENCE]" in response:
            break

        # Get manager's answer
        console.print()
        try:
            answer = console.input("[bold green]Your response:[/bold green] ")
        except (KeyboardInterrupt, EOFError):
            break

        if answer.strip().lower() == "/quit":
            console.print("\n[dim]Press conference abandoned.[/dim]")
            break

        contents.append({"role": "user", "parts": [{"text": answer}]})


def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        console.print(
            "[red]Set GEMINI_API_KEY environment variable first.[/red]\n"
            "  export GEMINI_API_KEY=your-key-here"
        )
        sys.exit(1)

    state = pick_scenario()
    system_prompt = build_system_prompt(state)

    console.print(
        Panel(
            f"[bold]{state.conference_type.value} Press Conference[/bold]\n"
            f"{state.club.name} — Manager: {state.manager.name}\n"
            f"[dim]Type /quit to leave early[/dim]",
            title="FM Press Conference Simulator",
            border_style="blue",
        )
    )

    run_conference(api_key, system_prompt)
    console.print("\n[bold]Thanks for playing![/bold]\n")


if __name__ == "__main__":
    main()
