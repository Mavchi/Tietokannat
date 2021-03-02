"""
Tietokantaan on luotu seuraava taulu, joka on aluksi tyhjä:
    CREATE TABLE Testi(x INTEGER)
Tee ohjelma, joka toistaa 5000 kertaa seuraavan operaation:
    1 Hae SELECT-kyselyllä taulun Testi suurin arvo x
    2 Lisää tauluun Testi uusi rivi, jonka arvona on x+1
    3 Tulosta lisätyn rivin arvo x
Testaa ensin, että ohjelma toimii: kun ohjelma suoritetaan ja taulu Testi on aluksi 
tyhjä, tauluun ilmestyy 5000 riviä, joilla on arvot 1, 2, 3, ..., 5000.

Tee sitten testi, jossa taulu on taas alussa tyhjä ja käynnistät samaan aikaan 
kaksi ohjelmaa, jotka molemmat lisäävät rinnakkain 5000 riviä tauluun.
"""
import sqlite3
import os
import sys

file_name = 'data'

# poistetaan vanha ja luodaan uusi tietokanta tilalle
def init_db():
    for i in range(1,4):
        if os.path.exists(file_name + str(i) + '.db'):
            os.remove(file_name + str(i) + '.db')
    # db1
    db = sqlite3.connect('data1.db')
    #db.execute('CREATE TABLE Testi (x INTEGER);')
    db.execute('CREATE TABLE Testi (x INTEGER UNIQUE);')
    db.commit()
    db.close()

def test1():
    db = sqlite3.connect('data1.db')
    db.isolation_level = None

    for __ in range(5000):
        x = db.execute('SELECT MAX(x) FROM Testi;').fetchone()[0]
        if not x:
            x = 0
        db.execute('INSERT INTO Testi (x) values (?);', [x+1])
        print(f'Lisättiin x={x+1}')

    print(db.execute('SELECT COUNT(*) FROM Testi;').fetchone()[0], 'alkiota')
    print(db.execute('SELECT MAX(x) FROM Testi;').fetchone()[0], ' suurin arvo')
    #db.commit()
    db.close()


def test3():
    db = sqlite3.connect('data1.db')
    db.isolation_level = None

    i = 0
    db.execute('BEGIN;')
    while i < 5000:
        try:
            x = db.execute('SELECT MAX(x) FROM Testi;').fetchone()[0]
            if not x:
                x = 0
        
            db.execute('INSERT INTO Testi (x) values (?);', [x+1])
            print(f'Lisättiin x={x+1}')
            i += 1
        except:
            #db.execute('ROLLBACK;')
            continue
    db.execute('COMMIT;')

    print(db.execute('SELECT COUNT(*) FROM Testi;').fetchone()[0], 'alkiota')
    print(db.execute('SELECT MAX(x) FROM Testi;').fetchone()
          [0], ' suurin arvo')
    #db.commit()
    db.close()


if __name__ == '__main__':
    if sys.argv[1] == 'init':
        init_db()
    elif sys.argv[1] == '3':
        test3()
