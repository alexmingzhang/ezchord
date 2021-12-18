![ezchord](https://user-images.githubusercontent.com/95546311/146628942-ce778235-0b25-4c8f-babb-e2c781d21c29.png)

# ezchord
Convert complex chord names to midi notes

## Usage
    $ ./ezchord.py Dmin7 G7 C
    $ timidity Dmin7-G-C.mid

Supports roman numerals:
    $ ./ezchord.py iimin7 V7 I --key Eb

Supports complex chord names
    $ ./ezchord.py C6/9 Fminmaj13#11 Fbdim7add9/G Fbbaugmaj13b9#11/Cbb Gsus9#13

Use '-' to continue previous chord or 'nc' to have no chord
    $ ./ezchord.py Dmin7b5 nc G7 nc Cmin -
