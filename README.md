![ezchord](https://user-images.githubusercontent.com/95546311/146630042-6b7d96a1-0f9a-4c98-97f4-ea400d0dc7d6.png)


# ezchord
Simple python script that can convert complex chord names to midi notes

## Prerequisites
Python 3, midiutil

To install midiutil:

    pip3 install midiutil


## Usage

    python3 ezchord.py [OPTIONS] chords [chords...]

The following produces a midi file with the chords Dmin7, G7, and C:

    python3 ezchord.py Dmin7 G7 C

output: `ezchord: created Dmin7-G7-Cmaj7.mid`

Supports roman numerals

    python3 ezchord.py iimin7 V7 I --key Eb

output: `ezchord: created iimin7-V7-I.mid`

Supports complex chord names

    python3 ezchord.py C6/9 Csus2maj7 Gsus9b13 "C7(b9#5)" "Cb(b9)" Fminmaj13#11 Fbdim7add9/G Fbbaugmaj13b9#11/Cbb

output: `ezchord: created C6slash9-Csus2maj7-Gsus9b13-C7(b9#5)-Cb(b9)-Fminmaj13#11-Fbdim7add9slashG-Fbbaugmaj13b9#11slashCbb.mid`

Use '-' to continue previous chord or 'nc' to have no chord

    python3 ezchord.py Dmin7b5 nc G7 nc Cmin -

output: `ezchord: created Dmin7b5-nc-G7-nc-Cmin--.mid`

## Options
```
  -h, --help            show this help message and exit
  -k KEY, --key KEY     Key (default C)
  -t TEMPO, --tempo TEMPO
                        Tempo in beats per minute (default 120)
  -d DURATION, --duration DURATION
                        Duration of each chord (default 2)
  -s SUBDIVIDE, --subdivide SUBDIVIDE
                        Subdivide chord's duration (default 1)
  -v VELOCITY, --velocity VELOCITY
                        Velocity (default 100)
  -O OCTAVE, --octave OCTAVE
                        Octave (default 4)
  -o OUTPUT, --output OUTPUT
                        Output file path
  --voice               Attempts to give chords a better voicing
```

## Examples

**Twelve Bar Blues**

    python3 ezchord.py I - - - IV - I - V IV I - -d 4 -o 12_bar_blues.mid

output: `ezchord: created 12_bar_blues.mid`

**Family Guy Theme Song**

    python3 ezchord.py F - G7 - Gmin7 C7 F F7 Bb Bdim7 F/C D7 G9 - C B9 Bb Bmin7 F/C D7 Gmin7 C7 Fmaj7 Bbmaj7 Emin7b5 A7 Dmin - G9 C7 Db7 C7/E F6/9 -t 140 --voice -o family_guy.mid

output: `ezchord: created family_guy.mid`

**Giant Steps**

    python3 ezchord.py Bmaj7 D7 Gmaj7 Bb7 Ebmaj7 - A-7 D7 Gmaj7 Bb7 Ebmaj7 F#7 Bmaj7 - F-7 Bb7 Ebmaj7 - A-7 D7 Gmaj7 - C#-7 F#7 Bmaj7 - F-7 Bb7 Ebmaj7 - C#-7 F#7 -t 130 -d 1 --voice -o giant_steps.mid

output: `ezchord: created giant_steps.mid`

**Autumn Leaves**

    python3 ezchord.py Cmin7 F7 Bbmaj7 Ebmaj7 Amin7b5 D7 Gmin7 -d 4 --voice -o autumn_leaves.mid

output: `ezchord: created autumn_leaves.mid`

**Misty**

    python3 ezchord.py D/Eb Ebmaj7 Bb-7 Eb7 Abmaj7 - Ab-7 Db7 Ebmaj7 C-7 F-7 Bb7 G-7 C7 F-7 Bb7 Ebmaj7 --voice -o misty.mid

output: `ezchord: created misty.mid`
