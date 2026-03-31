import os
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from moonlight_sonata import MoonlightSonata
from midi_builder import MidiBuilder
from player import MidiPlayer


MIDI_FILE = "moonlight_sonata.mid"
console = Console()

BANNER = """
        *    .        *       .        *
   .        *    .        .       *
      .           *    .     .        .

    [bold white]M O O N L I G H T   S O N A T A[/]
    [dim]Ludwig van Beethoven[/]
    [dim]Adagio sostenuto in C# minor[/]
"""


def show_menu():
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column()
    table.add_row("[1]", "Play")
    table.add_row("[2]", "Change tempo")
    table.add_row("[3]", "Exit")
    console.print()
    console.print(Panel(table, title="[bold]Menu[/]", border_style="dim", width=32))


def build_and_play(sonata, builder, midi_player):
    with Progress(SpinnerColumn(), TextColumn("{task.description}"),
                  console=console, transient=True) as progress:
        progress.add_task(f"Generating MIDI (tempo: {sonata.tempo} BPM)...", total=None)
        builder.build(sonata, MIDI_FILE)

    console.print(f"  [cyan]Playing at {sonata.tempo} BPM...[/]")
    midi_player.play(MIDI_FILE)
    midi_player.wait()
    console.print("  [green]Done.[/]")


def change_tempo(sonata):
    console.print(f"\n  Current tempo: [bold]{sonata.tempo}[/] BPM")
    try:
        new_tempo = int(console.input("  [dim]New tempo (30-200):[/] "))
        if 30 <= new_tempo <= 200:
            sonata.tempo = new_tempo
            console.print(f"  Tempo set to [bold cyan]{new_tempo}[/] BPM.")
        else:
            console.print("  [red]Must be between 30 and 200.[/]")
    except ValueError:
        console.print("  [red]Enter a number.[/]")


def main():
    os.system("cls" if os.name == "nt" else "clear")
    console.print(BANNER)

    sonata = MoonlightSonata()
    builder = MidiBuilder()
    midi_player = MidiPlayer()

    try:
        while True:
            show_menu()
            choice = console.input("\n  [bold]>[/] ").strip()

            if choice == "1":
                build_and_play(sonata, builder, midi_player)
            elif choice == "2":
                change_tempo(sonata)
            elif choice == "3":
                console.print("\n  [dim]Goodbye.[/]\n")
                break
            else:
                console.print("  [red]Invalid choice.[/]")
    finally:
        midi_player.cleanup()
        if os.path.exists(MIDI_FILE):
            os.remove(MIDI_FILE)


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
