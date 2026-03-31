# Moonlight Sonata MIDI Player

A Python command line application that encodes the opening bars of Ludwig van Beethoven's **Piano Sonata No. 14 in C# minor, Op. 27, No. 2** (popularly known as the "Moonlight Sonata") into a MIDI file and plays it back through your speakers. The entire musical score is defined purely in Python code using object oriented programming, and the program generates the MIDI file on the fly every time you hit play.

No pre recorded audio files are included. The music is built from scratch, note by note, every single time.

<br>

## Table of Contents

1. [What This Project Is](#what-this-project-is)
2. [What Is MIDI and Why Use It](#what-is-midi-and-why-use-it)
3. [Technologies and Libraries Used](#technologies-and-libraries-used)
4. [How to Run the Program](#how-to-run-the-program)
5. [Project Structure](#project-structure)
6. [How Each File Works](#how-each-file-works)
7. [How It All Works Under the Hood](#how-it-all-works-under-the-hood)
8. [Object Oriented Programming Principles](#object-oriented-programming-principles)
9. [The Musical Theory Behind the Code](#the-musical-theory-behind-the-code)
10. [What Could Be Added Next](#what-could-be-added-next)

<br>

## What This Project Is

This is a CLI (Command Line Interface) application written in Python. When you run it, a clean terminal menu appears. You can press `1` to play the first eight bars of the Moonlight Sonata, press `2` to change the tempo (speed) of the playback, or press `3` to exit.

Behind the scenes, the program:

1. Holds the entire musical score as a collection of `Note` objects inside a `MoonlightSonata` class.
2. Converts those notes into a valid `.mid` (MIDI) file using the `MidiBuilder` class.
3. Plays that `.mid` file through your computer's speakers using the `MidiPlayer` class and `pygame`.
4. Cleans up after itself by deleting the temporary MIDI file on exit.

Everything is orchestrated from `main.py`, which presents a modern looking terminal interface powered by the `rich` library.

<br>

## What Is MIDI and Why Use It

MIDI stands for **Musical Instrument Digital Interface**. It is not audio. It does not contain any sound waves or recordings. Instead, it is a set of **instructions** that tell a synthesizer (or your computer's built in sound chip) which notes to play, how hard to press them, and for how long.

Think of it this way: a `.wav` or `.mp3` file is like a photograph of a painting. A `.mid` file is like a list of instructions that says "put red here, draw a line there, shade this corner." The computer reads those instructions and **generates** the sound in real time.

A single MIDI message might say something like: "Turn on note 61 (C#4) with velocity 50 at tick 0." Then later: "Turn off note 61 at tick 160." That is all it takes to produce one note.

### Why MIDI for this project?

| Reason | Explanation |
|--------|-------------|
| **Tiny file size** | The generated `.mid` file is about 1 KB for 8 bars of music. An equivalent `.wav` would be several megabytes. |
| **Programmable** | Since MIDI is just data (note numbers, durations, velocities), we can define an entire musical score in Python and generate the file programmatically. |
| **Educational** | Working with MIDI teaches you how digital music works at a fundamental level. You learn about timing, pitch representation, and event based systems. |
| **No recording needed** | We do not need a microphone, a piano, or any audio files. Everything is built from code. |

### Key MIDI Concepts Used in This Project

| Concept | What It Means |
|---------|---------------|
| **Note Number (pitch)** | An integer from 0 to 127 that represents a musical pitch. Middle C is 60. C#4 is 61. Each increment is one semitone. |
| **Velocity** | How hard a key is pressed, from 0 (silent) to 127 (maximum force). This controls the volume and intensity of each note. |
| **Ticks** | The unit of time inside a MIDI file. The number of ticks per beat is configurable (we use 480). At 480 ticks per beat, a quarter note lasts 480 ticks, an eighth note 240, and so on. |
| **Delta Time** | MIDI events do not store absolute timestamps. Each event stores the number of ticks **since the previous event**. This is called delta time. |
| **Tempo** | Defined in microseconds per quarter note. To convert from BPM: `tempo_microseconds = 60,000,000 / BPM`. At 54 BPM, that gives us roughly 1,111,111 microseconds per beat. |
| **note_on / note_off** | The two main MIDI message types. `note_on` starts a note, `note_off` stops it. Every `note_on` must have a matching `note_off`, or the note rings forever. |
| **Program Change** | A message that selects which instrument to use. Program 0 is Acoustic Grand Piano. |

<br>

## Technologies and Libraries Used

### Python 3.10+

The entire project is written in Python. It uses standard Python features like classes, properties, abstract base classes, and list comprehensions.

### mido

[mido](https://mido.readthedocs.io/) is a Python library for working with MIDI files and messages. It provides clean, Pythonic classes for creating MIDI files, tracks, and messages. In this project, `mido` is used exclusively in the `MidiBuilder` class to:

1. Create a `MidiFile` object
2. Append `Message` objects (note_on, note_off, program_change)
3. Append `MetaMessage` objects (tempo, track name, end of track)
4. Save the result to a `.mid` file

### pygame

[pygame](https://www.pygame.org/) is a multimedia library for Python. We only use its `pygame.mixer.music` module, which can load and play MIDI files through your operating system's audio subsystem. The `MidiPlayer` class wraps pygame to provide simple `play()`, `stop()`, `wait()`, and `cleanup()` methods.

### rich

[rich](https://rich.readthedocs.io/) is a library for building beautiful terminal output. It handles colored text, panels, tables, and animated spinners. The `main.py` file uses `rich` to display:

1. A styled ASCII art banner
2. A bordered menu panel with a table
3. A spinning progress indicator while the MIDI file is being generated
4. Colored status messages (cyan for playing, green for done, red for errors)

### abc (Standard Library)

The `abc` module from Python's standard library provides the `ABC` base class and the `@abstractmethod` decorator. These are used to define the `Score` abstract class, which enforces a contract that all musical scores must follow.

<br>

## How to Run the Program

### Prerequisites

You need Python 3.10 or newer installed on your machine.

### Setup

```bash
cd moonlight-sonata-midi-python

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt
```

### Run

```bash
./venv/bin/python3 main.py
```

You will see a styled terminal interface with three options:

```
        *    .        *       .        *
   .        *    .        .       *
      .           *    .     .        .

    M O O N L I G H T   S O N A T A
    Ludwig van Beethoven
    Adagio sostenuto in C# minor

  ┌──── Menu ────┐
  │ [1]  Play    │
  │ [2]  Change  │
  │      tempo   │
  │ [3]  Exit    │
  └──────────────┘

  >
```

Press `1` to hear the first eight bars of the Moonlight Sonata. Press `2` to change the playback speed. Press `3` to exit.

<br>

## Project Structure

```
moonlight-sonata-midi-python/
│
├── main.py               Entry point. CLI interface with rich.
├── note.py               The Note class. Represents a single musical note.
├── score.py              Abstract base class Score. Defines the contract.
├── moonlight_sonata.py   MoonlightSonata class. The actual musical data.
├── midi_builder.py       MidiBuilder class. Converts Score to a .mid file.
├── player.py             MidiPlayer class. Plays .mid files with pygame.
├── requirements.txt      Python dependencies (mido, pygame, rich).
└── venv/                 Virtual environment (not committed to git).
```

### Why Is It Structured This Way?

Each file has **one responsibility**. This follows the Single Responsibility Principle and makes the codebase easy to read, easy to test, and easy to extend.

| File | Responsibility |
|------|---------------|
| `note.py` | Knows what a musical note is. Nothing else. |
| `score.py` | Defines the **shape** of any musical score. Does not know about any specific piece. |
| `moonlight_sonata.py` | Holds the actual notes of the Moonlight Sonata. Inherits from `Score`. |
| `midi_builder.py` | Knows how to convert any `Score` into a MIDI file. Does not know about specific pieces. |
| `player.py` | Knows how to play a `.mid` file. Does not know how it was created. |
| `main.py` | Glues everything together and handles user interaction. |

This separation means that if you wanted to add a new piece of music (say, Fur Elise), you would only need to create one new file: `fur_elise.py`. You would not need to touch `midi_builder.py`, `player.py`, or `note.py` at all. The existing infrastructure works for any score.

<br>

## How Each File Works

### note.py

```python
class Note:

    def __init__(self, pitch, duration, velocity=64, start_tick=0):
        self._pitch = pitch
        self._duration = duration
        self._velocity = velocity
        self._start_tick = start_tick

    @property
    def pitch(self):
        return self._pitch

    @property
    def duration(self):
        return self._duration

    @property
    def velocity(self):
        return self._velocity

    @property
    def start_tick(self):
        return self._start_tick

    def __repr__(self):
        return f"Note(pitch={self._pitch}, dur={self._duration}, vel={self._velocity}, t={self._start_tick})"
```

This is the most basic building block. A `Note` has four attributes:

| Attribute | Type | Meaning |
|-----------|------|---------|
| `pitch` | int | MIDI note number (0 to 127). For example, 61 is C#4. |
| `duration` | int | How long the note lasts, measured in MIDI ticks. |
| `velocity` | int | How hard the key is pressed (0 to 127). Default is 64 (medium). |
| `start_tick` | int | The absolute position in time where this note begins. |

All attributes are stored as **private** (prefixed with `_`) and exposed through **read only properties**. This means once a note is created, it cannot be accidentally changed. A note is a fact: "play C#4 at tick 0 for 160 ticks with velocity 50." Facts do not change.

The `__repr__` method gives a readable string when you print a Note, which is useful during debugging.

### score.py

```python
from abc import ABC, abstractmethod


class Score(ABC):

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def tempo(self):
        pass

    @abstractmethod
    def get_notes(self):
        pass
```

This is an **abstract base class**. You can never create an instance of `Score` directly. If you try `Score()`, Python will raise a `TypeError`. Its only purpose is to say: "Any class that wants to be a musical score **must** provide these three things: a `title`, a `tempo`, and a `get_notes()` method."

This is the backbone of the whole architecture. Because `MidiBuilder` works with the `Score` type (and not with `MoonlightSonata` specifically), it can accept any score. The builder does not care whether it is processing Beethoven or Bach. It just calls `score.get_notes()` and gets a list of `Note` objects.

### moonlight_sonata.py

```python
class MoonlightSonata(Score):

    TICKS_PER_BEAT = 480
    TRIPLET = TICKS_PER_BEAT // 3

    CS2 = 37
    GS2 = 44
    CS3 = 49
    ...
```

This is where the actual music lives. The class stores MIDI note numbers as **class level constants** (like `CS2 = 37`, which is C#2) so the code that builds the bars is readable. Instead of writing the number 37 everywhere, you write `self.CS2`, which is immediately understandable.

The `_triplet_bar()` helper method creates one full bar of music. It takes:

1. `bar_start`: the absolute tick position where this bar begins
2. `bass_notes`: a list of pitches for the bass (left hand), played as whole notes
3. `arpeggio_notes`: a list of three pitches for the right hand triplet arpeggio

It returns a list of `Note` objects that together make up one bar.

The `get_notes()` method calls `_triplet_bar()` for each of the eight bars with the appropriate bass notes and arpeggio patterns, and collects all the notes into one big list.

The `tempo` property has both a getter and a setter, so the user can change the playback speed from the menu without creating a new `MoonlightSonata` object.

### midi_builder.py

```python
class MidiBuilder:

    TICKS_PER_BEAT = 480

    def build(self, score, filename="output.mid"):
        mid = MidiFile(type=0, ticks_per_beat=self.TICKS_PER_BEAT)
        track = MidiTrack()
        mid.tracks.append(track)
        ...
```

This class takes any `Score` object and converts it into a `.mid` file. The `build()` method:

1. **Creates a MIDI file** with Type 0 (single track) and 480 ticks per beat.
2. **Adds metadata**: track name, tempo (converted from BPM to microseconds), and instrument (Acoustic Grand Piano, program 0).
3. **Converts notes to events**: Each `Note` produces two events: a `note_on` at the note's `start_tick` and a `note_off` at `start_tick + duration`.
4. **Sorts events by time**: This is critical. Events from different notes (bass and arpeggio) must be interleaved in chronological order. The sort also places `note_off` before `note_on` at the same tick, which prevents hanging notes.
5. **Converts absolute time to delta time**: MIDI files store delta times (time since the last event), not absolute times. The code walks through the sorted events and computes `delta = abs_tick - prev_tick` for each one.
6. **Saves the file** to disk.

This is the most technically interesting class. It bridges the gap between our high level musical data model (`Note` objects with absolute start times) and the low level MIDI file format (sequential messages with delta times).

### player.py

```python
class MidiPlayer:

    def __init__(self):
        pygame.mixer.init()

    def play(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    @property
    def is_playing(self):
        return pygame.mixer.music.get_busy()

    def wait(self):
        while self.is_playing:
            pygame.time.delay(200)

    def cleanup(self):
        pygame.mixer.quit()
```

This is a thin wrapper around `pygame.mixer.music`. It exposes a clean interface: `play()`, `stop()`, `is_playing`, `wait()`, and `cleanup()`. The rest of the program never touches pygame directly; it only talks to `MidiPlayer`.

The `wait()` method blocks until the music finishes, checking every 200 milliseconds. The `cleanup()` method properly shuts down pygame's mixer subsystem to release audio resources.

### main.py

The entry point. It uses `rich` to create a modern terminal experience:

1. Clears the screen and prints an ASCII art starry sky banner with the title.
2. Creates instances of `MoonlightSonata`, `MidiBuilder`, and `MidiPlayer`.
3. Shows a `rich.Panel` menu in a loop.
4. On "Play": shows a `rich.Progress` spinner while generating the MIDI file, then plays it and waits.
5. On "Change tempo": prompts for a new BPM value (validated to be between 30 and 200).
6. On "Exit": says goodbye and breaks the loop.
7. In the `finally` block: always cleans up the player and deletes the temporary MIDI file, even if the program crashes.

<br>

## How It All Works Under the Hood

Here is the complete flow from the moment you press `1` to the moment you hear music:

### Step 1: Building the Note List

`MoonlightSonata.get_notes()` is called. It iterates through 8 bars. For each bar, `_triplet_bar()` creates:

Two bass notes (whole notes, 1920 ticks each, starting at the bar's first tick):
```
Note(pitch=37, dur=1920, vel=40, t=0)     # C#2 bass
Note(pitch=49, dur=1920, vel=40, t=0)     # C#3 bass
```

Twelve triplet notes (160 ticks each, starting sequentially):
```
Note(pitch=56, dur=160, vel=50, t=0)      # G#3
Note(pitch=61, dur=160, vel=50, t=160)    # C#4
Note(pitch=64, dur=160, vel=50, t=320)    # E4
Note(pitch=56, dur=160, vel=50, t=480)    # G#3
Note(pitch=61, dur=160, vel=50, t=640)    # C#4
...and so on for 12 triplet notes total
```

This produces 14 notes per bar and 112 notes total across 8 bars.

### Step 2: Converting to MIDI Events

`MidiBuilder.build()` takes the 112 notes and creates 224 events (one `note_on` and one `note_off` per note). These events are then sorted by absolute time. Events at the same tick are ordered so that `note_off` comes before `note_on`, which prevents overlapping issues.

### Step 3: Delta Time Conversion

The sorted events are converted from absolute time to delta time. For example:

| Absolute Tick | Event | Delta Time |
|---------------|-------|------------|
| 0 | note_on C#2 | 0 |
| 0 | note_on C#3 | 0 |
| 0 | note_on G#3 | 0 |
| 160 | note_off G#3 | 160 |
| 160 | note_on C#4 | 0 |
| 320 | note_off C#4 | 160 |

Notice how two events at the same tick both have correct deltas: the first one at tick 160 has delta=160 (from tick 0), and the note_on at the same tick 160 has delta=0 (no time has passed since the previous event).

### Step 4: Saving and Playing

The MIDI file is saved to `moonlight_sonata.mid` (about 1 KB). Then `pygame.mixer.music` loads it and sends it to your operating system's audio subsystem, which uses a software synthesizer to produce actual sound waves from the MIDI instructions.

### Step 5: Cleanup

When playback ends (or you exit), the program deletes the temporary `.mid` file and releases the audio resources.

<br>

## Object Oriented Programming Principles

This project demonstrates all four core principles of OOP. Below is an explanation of each one, how it is used, and why it matters.

### 1. Encapsulation

**What it is:** Encapsulation means bundling data (attributes) and the methods that operate on that data into a single unit (a class), and controlling access to the internal state.

**How it is used in this project:**

In `Note`, all attributes are private (prefixed with an underscore) and exposed through read only properties:

```python
class Note:

    def __init__(self, pitch, duration, velocity=64, start_tick=0):
        self._pitch = pitch
        self._duration = duration
        self._velocity = velocity
        self._start_tick = start_tick

    @property
    def pitch(self):
        return self._pitch
```

The outside world can **read** `note.pitch` but cannot **write** `note.pitch = 99`. This is intentional. A musical note, once placed in the score, should not silently change. If something in the code tried to modify a note's pitch, it would get an `AttributeError`, which is exactly what we want. Bugs surface immediately instead of hiding.

In `MidiPlayer`, the pygame state is fully encapsulated:

```python
class MidiPlayer:

    def __init__(self):
        pygame.mixer.init()

    def play(self, filename):
        pygame.mixer.music.load(filename)
        pygame.mixer.music.set_volume(0.8)
        pygame.mixer.music.play()
```

No other file in the project imports `pygame`. Only `MidiPlayer` knows that pygame exists. If we wanted to switch to a different audio library tomorrow, we would only need to change `player.py`. Everything else stays untouched.

**Why it matters:** Encapsulation protects data integrity and reduces coupling between components. Each class manages its own state, and changes to one class do not ripple through the rest of the codebase.

### 2. Abstraction

**What it is:** Abstraction means exposing only the essential features of a component and hiding the complex implementation details. The user of a class does not need to know how it works internally; they only need to know what methods to call.

**How it is used in this project:**

The `Score` abstract base class is pure abstraction:

```python
from abc import ABC, abstractmethod


class Score(ABC):

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    @abstractmethod
    def tempo(self):
        pass

    @abstractmethod
    def get_notes(self):
        pass
```

`Score` says: "A musical score has a title, a tempo, and a method to get its notes." That is the **abstract concept** of a score. It deliberately does not say anything about C# minor, triplets, or Beethoven. Those are implementation details that belong to specific subclasses.

Similarly, `MidiBuilder.build()` provides a simple interface:

```python
builder.build(sonata, "moonlight_sonata.mid")
```

One line. The caller does not need to understand delta time conversion, event sorting, MIDI message types, or the Type 0 file format. All of that complexity is **abstracted away** behind the `build()` method.

And `MidiPlayer` abstracts away the entire pygame ecosystem:

```python
midi_player.play("moonlight_sonata.mid")
midi_player.wait()
```

Two lines to play music. The caller does not know (or care) about `pygame.mixer.init()`, `pygame.mixer.music.load()`, `get_busy()`, or `pygame.time.delay()`.

**Why it matters:** Abstraction reduces cognitive load. When reading `main.py`, you do not need to understand MIDI file internals or pygame setup. You see `builder.build()` and `player.play()` and you understand the flow immediately.

### 3. Inheritance

**What it is:** Inheritance allows a new class (child) to reuse the structure and behavior of an existing class (parent). The child class inherits everything from the parent and can add or modify behavior.

**How it is used in this project:**

`MoonlightSonata` inherits from `Score`:

```python
class MoonlightSonata(Score):

    @property
    def title(self):
        return "Moonlight Sonata - Adagio sostenuto (Beethoven)"

    @property
    def tempo(self):
        return self._tempo

    def get_notes(self):
        notes = []
        bar_length = self.TICKS_PER_BEAT * 4
        bar = 0
        ...
        return notes
```

By inheriting from `Score`, `MoonlightSonata` **promises** that it will implement `title`, `tempo`, and `get_notes()`. If it forgot to implement one of these, Python would raise a `TypeError` at instantiation time, telling you exactly what is missing. This turns potential runtime bugs into immediate, obvious errors.

The inheritance relationship also communicates intent. When a developer reads `class MoonlightSonata(Score)`, they instantly know: "This is a type of Score. It has a title, a tempo, and notes." They do not need to read the whole class to understand its shape.

**Why it matters:** Inheritance establishes an "is a" relationship. A `MoonlightSonata` **is a** `Score`. This means it can be used anywhere a `Score` is expected, which leads directly to the next principle.

### 4. Polymorphism

**What it is:** Polymorphism means "many forms." It allows code to work with objects of different classes through a common interface. The same method call can produce different behavior depending on which class the object belongs to.

**How it is used in this project:**

The `MidiBuilder.build()` method accepts any `Score`:

```python
class MidiBuilder:

    def build(self, score, filename="output.mid"):
        ...
        track.append(MetaMessage("track_name", name=score.title, time=0))
        tempo_us = int(60_000_000 / score.tempo)
        ...
        for note in score.get_notes():
            events.append((note.start_tick, "on", note.pitch, note.velocity))
            events.append((note.start_tick + note.duration, "off", note.pitch, 0))
```

The builder calls `score.title`, `score.tempo`, and `score.get_notes()`. It does not know or care which specific class it is working with. Right now, we pass a `MoonlightSonata` object. But imagine we created two more classes:

```python
class FurElise(Score):
    @property
    def title(self):
        return "Fur Elise (Beethoven)"

    @property
    def tempo(self):
        return 72

    def get_notes(self):
        return [...]  # different notes entirely


class ClairDeLune(Score):
    @property
    def title(self):
        return "Clair de Lune (Debussy)"

    @property
    def tempo(self):
        return 66

    def get_notes(self):
        return [...]  # completely different notes
```

**Without changing a single line** in `MidiBuilder`, `MidiPlayer`, or `main.py`, we could do:

```python
builder.build(FurElise(), "fur_elise.mid")
builder.build(ClairDeLune(), "clair_de_lune.mid")
```

The same `build()` method, the same code, but it produces completely different MIDI files because each `Score` subclass returns different notes. That is polymorphism in action.

This is also visible in `main.py`:

```python
sonata = MoonlightSonata()
builder = MidiBuilder()
midi_player = MidiPlayer()

builder.build(sonata, MIDI_FILE)
midi_player.play(MIDI_FILE)
```

If you swapped `MoonlightSonata()` for `FurElise()`, the rest of the code would work identically. The variable `sonata` could hold any `Score`. The builder and player are oblivious to which piece they are processing.

**Why it matters:** Polymorphism makes code extensible without modification. You add new behavior (new pieces of music) by adding new classes, not by editing existing ones. This is the essence of the Open/Closed Principle: open for extension, closed for modification.

### Summary Table: OOP Principles at a Glance

| Principle | Where It Appears | What It Does |
|-----------|-----------------|--------------|
| **Encapsulation** | `Note` uses `_pitch` with `@property`; `MidiPlayer` hides pygame internally | Protects internal state, exposes clean interfaces |
| **Abstraction** | `Score` ABC defines the contract; `MidiBuilder.build()` hides MIDI complexity | Simplifies usage by hiding implementation details |
| **Inheritance** | `MoonlightSonata(Score)` inherits and implements the abstract contract | Establishes "is a" relationships, enforces structure |
| **Polymorphism** | `MidiBuilder.build(score)` works with **any** `Score` subclass | Enables extensibility without changing existing code |

<br>

## The Musical Theory Behind the Code

### About the Piece

The Moonlight Sonata (officially: Piano Sonata No. 14 in C# minor, Op. 27, No. 2) was composed by Ludwig van Beethoven in 1801. The first movement, marked **Adagio sostenuto**, is one of the most recognized pieces of classical music in the world.

The movement features a simple but hypnotic structure:

1. The **left hand** plays sustained bass notes (octaves) that ring out for an entire bar.
2. The **right hand** plays continuous triplet arpeggios: groups of three notes that cycle through the chord tones.

This creates a shimmering, almost ghostly texture. The bass provides harmonic foundation while the triplets create a flowing, dreamlike surface.

### How the Notes Are Encoded

Each note is identified by its MIDI number. Here is a reference table for the notes used in this project:

| Note Name | MIDI Number | Role in the Piece |
|-----------|-------------|-------------------|
| C#2 | 37 | Bass (left hand, lowest note) |
| G#2 | 44 | Bass in bars 7 and 8 |
| A2 | 45 | Bass in bar 6 |
| B2 | 47 | Bass in bar 5 |
| C#3 | 49 | Bass octave (left hand, upper) |
| G#3 | 56 | Arpeggio note (right hand) |
| A3 | 57 | Arpeggio note in bar 6 |
| B3 | 59 | Arpeggio note in bars 7 and 8 |
| C#4 | 61 | Arpeggio note (right hand) |
| E4 | 64 | Arpeggio note, highest in the triplet |

### The Triplet Pattern

At 480 ticks per beat, each triplet note is `480 / 3 = 160` ticks. There are 4 beats per bar, so each bar has `4 x 3 = 12` triplet notes plus the bass notes underneath.

The first four bars all use the same pattern:

```
Bass:      C#2 + C#3 (held for the entire bar = 1920 ticks)
Arpeggio:  G#3  C#4  E4 | G#3  C#4  E4 | G#3  C#4  E4 | G#3  C#4  E4
           ^^^beat 1^^^   ^^^beat 2^^^   ^^^beat 3^^^   ^^^beat 4^^^
```

### Tempo

The default tempo is 54 BPM (beats per minute), which is within the **Adagio** range. In MIDI, this is expressed as `60,000,000 / 54 = 1,111,111` microseconds per quarter note. The user can change this from the menu to hear the piece faster or slower.

<br>

## What Could Be Added Next

Here are some ideas for extending the project:

| Feature | How You Would Do It |
|---------|--------------------|
| **More bars** | Add more calls to `_triplet_bar()` in `get_notes()` with the correct bass and arpeggio notes for bars 9 through 69. |
| **Volume dynamics** | Change the `velocity` parameter across different bars. The real piece has crescendos and decrescendos. |
| **Sustain pedal** | MIDI Control Change 64 controls the sustain pedal. Add `Message("control_change", control=64, value=127)` for pedal down and `value=0` for pedal up. |
| **New pieces** | Create a new class like `FurElise(Score)` with its own `get_notes()`. The builder and player work automatically. |
| **Save MIDI to file** | Add a menu option that saves the generated `.mid` to a user specified path instead of deleting it on exit. |
| **Multiple instruments** | Use MIDI channels and program changes to add strings or other instruments alongside the piano. |
