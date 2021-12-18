![ezchord](https://user-images.githubusercontent.com/95546311/146630042-6b7d96a1-0f9a-4c98-97f4-ea400d0dc7d6.png)


# ezchord
Simply python script that can convert complex chord names to midi notes

## Prerequisites
MIDIUtil

    $ pip install midiutil


## Usage

    $ ./ezchord.py Dmin7 G7 C
    $ timidity Dmin7-G-C.mid

Supports roman numerals

    $ ./ezchord.py iimin7 V7 I --key Eb

Supports complex chord names

    $ ./ezchord.py C6/9 Cb(b9) Fminmaj13#11 Fbdim7add9/G Fbbaugmaj13b9#11/Cbb Gsus9#13

Use '-' to continue previous chord or 'nc' to have no chord

    $ ./ezchord.py Dmin7b5 nc G7 nc Cmin -
    
## Examples

Twelve Bar Blues

    $ ./ezchord.py I I I I IV IV I I V IV I I -d 4 12_bar_blues.mid

Family Guy Theme Song

    $ ./ezchord.py F - G7 - Gmin7 C7 F F7 Bb Bdim7 F/C D7 G9 - C B9 Bb Bmin7 F/C D7 Gmin7 C7 Fmaj7 Bbmaj7 Emin7b5 A7 Dmin - G9 C7 Db7 C7/E F6/9 --key F -t 140 --voice -o family_guy.midi

Giant Steps

    $ ./ezchord.py Bmaj7 D7 Gmaj7 Bb7 Ebmaj7 - A-7 D7 Gmaj7 Bb7 Ebmaj7 F#7 Bmaj7 - F-7 Bb7 Ebmaj7 - A-7 D7 Gmaj7 - C#-7 F#7 Bmaj7 - F-7 Bb7 Ebmaj7 - C#-7 F#7 -t 130 -d 1 --voice -o giantsteps.mid

Autumn Leaves
    
    $ ./ezchord.py Cmin7 F7 Bbmaj7 Ebmaj7 Amin7b5 D7 Gmin7 -d  4 --key G --voice -o autumn_leaves.mid 

Misty

    $ ./ezchord.py D/Eb Ebmaj7 Bb-7 Eb7 Abmaj7 - Ab-7 Db7 Ebmaj7 C-7 F-7 Bb7 G-7 C7 F-7 Bb7 Ebmaj7 --voice -o misty.mid
