#!/usr/bin/env python3

# ezchord - convert complex chord names to midi notes

# todo:
#   - remove duplicate note in sus chords
#   - de-spaghettify code
#   - add ability to get individual note names in chord
#   - add proper support for roman numeral slash chords (e.g. V/V in the key of C refers to D major)
#   - better chord voicing
#   - add comments to this mess

import sys
import math
import argparse
from enum import Enum, auto
from midiutil import MIDIFile

################################################################################
# ENUMS AND CONSTANTS                                                          #
################################################################################
class Mode(Enum):
    DIM = auto()
    MIN = auto()
    MAJ = auto()
    DOM = auto()
    AUG = auto()
    SUS2 = auto()
    SUS = auto()
    FIVE = auto()

TEXT_TO_MODE = {
    "maj":  Mode.MAJ,
    "dim":  Mode.DIM,
    "o":    Mode.DIM,
    "min":  Mode.MIN,
    "m":    Mode.MIN,
    "-":    Mode.MIN,
    "aug":  Mode.AUG,
    "+":    Mode.AUG,
    "sus2":  Mode.SUS2,
    "sus":  Mode.SUS,
    "5":    Mode.FIVE,
    "five": Mode.FIVE
}

MODE_TO_SHIFT = {
    Mode.MAJ:   {3:0, 5:0},
    Mode.DOM:   {3:0, 5:0},
    Mode.DIM:   {3:-1, 5:-1},
    Mode.MIN:   {3:-1, 5:0},
    Mode.AUG:   {3:0, 5:1},
    Mode.SUS2:  {3:-2, 5:0},
    Mode.SUS:   {3:1, 5:0},
    Mode.FIVE:  {3:3, 5:0},
}

NOTE_TO_PITCH = {
    "a": 9,
    "b": 11,
    "c": 12,
    "d": 14,
    "e": 16,
    "f": 17,
    "g": 19
}

PITCH_TO_NOTE = {}

for note, pitch in NOTE_TO_PITCH.items():
    PITCH_TO_NOTE[pitch] = note

RM_TO_PITCH = {
    "vii":  11,
    "iii":  4,
    "vi":   9,
    "iv":   5,
    "ii":   2,
    "i":    0,
    "v":    7
}

ACC_TO_SHIFT = {
    "b": -1,
    "#": 1
}

SCALE_DEGREE_SHIFT = {
    1: 0,
    2: 2,
    3: 4,
    4: 5,
    5: 7,
    6: 9,
    7: 11
}


################################################################################
# HELPER FUNCTIONS                                                             #
################################################################################
def get_number(text):
    num_str = ""

    for char in text:
        if char.isdigit():
            num_str += char

    if len(num_str) > 0:
        return int(num_str)

    return

def text_to_pitch(text, key = "c"):
    text = text.lower()
    is_letter = text[0] in NOTE_TO_PITCH.keys()

    if is_letter:
        pitch = NOTE_TO_PITCH[text[0]]
    else:
        for rm in RM_TO_PITCH.keys():
            if rm in text:
                pitch = RM_TO_PITCH[rm] + text_to_pitch(key)
                is_roman_numeral = True
                break

    for i in range(1 if is_letter else 0, len(text)):
        if text[i] in ACC_TO_SHIFT.keys():
            pitch += ACC_TO_SHIFT[text[i]]

    return pitch

def pitch_to_text(pitch):
    octave = math.floor(pitch / 12)
    pitch = pitch % 12
    pitch = pitch + (12 if pitch < 9 else 0)
    accidental = ""

    if not (pitch in PITCH_TO_NOTE.keys()):
        pitch = (pitch + 1) % 12
        pitch = pitch + (12 if pitch < 9 else 0)
        accidental = "b"

    return PITCH_TO_NOTE[pitch].upper() + accidental + str(octave)

def degree_to_shift(deg):
    return SCALE_DEGREE_SHIFT[(deg - 1) % 7 + 1] + math.floor(deg / 8) * 12

def voice(chords):
    center = 0
    voiced_chords = [chords[0]]

    # Bring the fifth an octave down
    # voiced_chords[0][3] -= 12

    center = chords[0][1] + 3

    for i, curr_chord in enumerate(chords):
        # Skip first chord
        if i == 0:
            continue

        prev_chord = voiced_chords[i - 1]
        voiced_chord = []

        for i_, curr_note in enumerate(curr_chord):
            # Skip bass note
            if i_ == 0:
                prev_note = prev_chord[0]

                #print("================================")
                #print("{: >4} {: >4} {: >4}    {: >4} {: >4} {: >4}".format("CN", "BN", "BV", "CN", "BN", "BV"))

                if abs(curr_note - prev_note) > 7:
                    if curr_note < prev_note and abs(curr_note + 12 - prev_note) < abs(curr_note - prev_note):
                        best_voicing = curr_note + 12
                    elif curr_note > prev_note and abs(curr_note - 12 - prev_note) < abs(curr_note - prev_note):
                        best_voicing = curr_note - 12
                else:
                    best_voicing = curr_note

                voiced_chord.append(best_voicing)
                continue

            best_neighbor = None
            allowance = -1

            while best_neighbor == None:
                allowance += 1

                for i__, prev_note in enumerate(prev_chord):
                    if i__ == 0:
                        continue

                    if (
                        abs(curr_note - prev_note) % 12 == allowance
                        or abs(curr_note - prev_note) % 12 == 12 - allowance
                    ):
                        best_neighbor = prev_note
                        break

            if curr_note <= best_neighbor:
                best_voicing = curr_note + math.floor((best_neighbor - curr_note + 6) / 12) * 12
            else:
                best_voicing = curr_note + math.ceil((best_neighbor - curr_note - 6) / 12) * 12

            best_voicing = best_voicing if (abs(best_voicing - center) <= 8 or allowance > 2) else curr_note
            voiced_chord.append(best_voicing)

            #print("{: >4} {: >4} {: >4}    {: >4} {: >4} {: >4}".format(pitch_to_text(curr_note), pitch_to_text(best_neighbor), pitch_to_text(best_voicing), curr_note, best_neighbor, best_voicing))

        voiced_chord.sort()
        voiced_chords.append(voiced_chord)

    return voiced_chords

################################################################################
# Chord class                                                                  #
################################################################################
class Chord:
    def __init__(self, string):
        self.string = string
        self.degrees = {}

        string += " "
        self.split = []
        sect = ""

        notes = list(NOTE_TO_PITCH.keys())
        rms = list(RM_TO_PITCH.keys())
        accs = list(ACC_TO_SHIFT.keys())
        modes = list(TEXT_TO_MODE.keys())

        root_added = False
        mode_added = False

        is_roman_numeral = False
        is_slash_chord = False
        is_maj7 = False

        for i in range(0, len(string) - 1):
            sect += string[i]
            curr_char = string[i].lower()
            next_char = string[i+1].lower()

            root_found = not root_added and (curr_char in notes+rms+accs and not next_char in rms+accs)
            mode_found = False
            num_found = (curr_char.isdigit() and not next_char.isdigit())

            if (
                (i == len(string) - 2)
                or root_found
                or num_found
                or next_char == "/"
                or curr_char == ")"
            ):
                if root_found:
                    self.root = sect
                    root_added = True

                    is_roman_numeral = self.root in rms
                elif sect[0] == "/":
                    # case for 6/9 chords
                    if sect[1] == "9":
                        self.degrees[9] = 0
                    else:
                        is_slash_chord = True
                        self.bassnote = sect[1:len(sect)]
                else:
                    if not mode_added:
                        for mode in modes:
                            mode_found = mode in sect[0:len(mode)]
                            if mode_found:
                                self.mode = TEXT_TO_MODE[mode]
                                mode_added = True
                                break

                    if not mode_added:
                        if not is_roman_numeral and str(get_number(sect)) == sect:
                            self.mode = Mode.DOM
                            mode_found = True
                            mode_added = True

                    deg = get_number(sect)
                    if deg != None:
                        shift = 0

                        for char in sect:
                            if char == "#":
                                shift += 1
                            elif char == "b":
                                shift -= 1

                        if (not mode_found) or deg % 2 == 0:
                            self.degrees[deg] = shift
                        elif deg >= 7:
                            for i in range(7, deg+1):
                                if i % 2 != 0:
                                    self.degrees[i] = shift

                self.split.append(sect)
                sect = ""

        if not mode_added:
            # Case for minor roman numeral chords
            if self.root in rms and self.root == self.root.lower():
                self.mode = Mode.MIN
            else:
                self.mode = Mode.DOM

        if not is_slash_chord:
            self.bassnote = self.root

        for sect in self.split:
            is_maj7 = ("maj" in sect) or is_maj7

        if (7 in self.degrees.keys()) and not is_maj7:
            self.degrees[7] = -1

    def get_midi(self, key="c", octave=4):
        notes = {}

        notes[0] = text_to_pitch(self.bassnote, key) - 12

        root = text_to_pitch(self.root, key)
        notes[1] = root
        notes[3] = root + degree_to_shift(3) + MODE_TO_SHIFT[self.mode][3]
        notes[5] = root + degree_to_shift(5) + MODE_TO_SHIFT[self.mode][5]

        for deg in self.degrees.keys():
            notes[deg] = root + degree_to_shift(deg) + self.degrees[deg]

        for deg in notes.keys():
            notes[deg] += 12 * octave

        return list(notes.values())

################################################################################
# MAIN                                                                         #
################################################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ezchord - convert complex chord names to midi notes")
    parser.add_argument("chords", type=str, nargs="+", help="Sequence of chord names (e.g. C C7 F Fmin6 C/G G7 C)\n'-' continues the previous chord\n'nc' inserts a rest")
    parser.add_argument("-k", "--key", type=str, default="c", help="Key (default C)")
    parser.add_argument("-t", "--tempo", type=int, default=120, help="Tempo in beats per minute (default 120)")
    parser.add_argument("-d", "--duration", type=int, default=2, help="Duration of each chord (default 2)")
    parser.add_argument("-s", "--subdivide", type=int, default=1, help="Subdivide chord's duration (default 1)")
    parser.add_argument("-v", "--velocity", type=int, default=100, help="Velocity (default 100)")
    parser.add_argument("-O", "--octave", type=int, default=4, help="Octave (default 4)")
    parser.add_argument("-o", "--output", type=str, help="Output file path")
    parser.add_argument('--voice', action="store_true", help="Attempts to give chords a better voicing")

    args = parser.parse_args()

    MIDI = MIDIFile(1)
    MIDI.addTempo(0, 0, args.tempo)

    midi_chords = []

    output_file_name = "" if args.output == None else args.output
    need_file_name = args.output == None

    for i, arg in enumerate(args.chords):
        if arg == "-":
            midi_chords.append(midi_chords[i - 1])
        elif arg.lower() in ["nc", "n.c", "n.c."]:
            midi_chords.append([])
        else:
            midi_chords.append(Chord(arg).get_midi(args.key, args.octave))

    if args.voice:
        midi_chords = voice(midi_chords)

    for i, chord in enumerate(midi_chords):
        for pitch in chord:
            for d in range(0, args.subdivide):
                MIDI.addNote(0, 0, pitch, i * args.duration + d * (args.duration / args.subdivide), args.duration / args.subdivide, args.velocity)

        if need_file_name:
            if i > 0:
                output_file_name += "-"

            output_file_name += args.chords[i].replace("/", "slash")

            if i == len(midi_chords) - 1:
                output_file_name += ".mid"

    with open(output_file_name, "wb") as output_file:
        MIDI.writeFile(output_file)
        print("ezchord: created", output_file_name)
