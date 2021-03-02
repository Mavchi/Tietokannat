
"""
Yhteensä on tarkoitus suorittaa 3 tehokkuustestissä
1 Tauluun ei lisätä kyselyitä tehostavaa indeksiä.
2 Tauluun lisätään kyselyitä tehostava indeksi ennen rivien lisäämistä.
3 Tauluun lisätään kyselyitä tehostava indeksi ennen kyselyiden suoritusta.

Itse testeissä on tarkoitus:
- Ohjelma luo taulun Elokuvat, jossa on sarakkeet id, nimi ja vuosi.
- Ohjelma lisää tauluun miljoona riviä. Jokaisen rivin kohdalla nimeksi valitaan 
  satunnainen merkkijono ja vuodeksi valitaan satunnainen kokonaisluku väliltä 1900–2000.
- Ohjelma suorittaa tuhat kertaa kyselyn, jossa haetaan elokuvien määrä vuonna x. 
  Jokaisessa kyselyssä x valitaan satunnaisesti väliltä 1900–2000.
"""
import sqlite3
import os
import time
import random
import string

# tyhjennetään tietokanta ja luodaan uusi Elokuvat-taulukko
def empty_db(db):
    try:
        db.execute('DROP TABLE Elokuvat;')
    except:
        print('Ei Elokuvat tietokantaa vielä lisättynä')

    db.execute(
        f'CREATE TABLE Elokuvat ('
        f'id INTEGER PRIMARY KEY,'
        f'nimi TEXT,'
        f'vuosi INTEGER'
        f');'
    )
    print(f'Tietokanta avattu ja alussa {db.execute("SELECT COUNT(nimi) from Elokuvat;").fetchone()[0]} elokuvaa tietokannassa')

# Ohjelma lisää tauluun miljoona riviä. Jokaisen rivin kohdalla nimeksi valitaan satunnainen merkkijono ja vuodeksi valitaan 
# satunnainen kokonaisluku väliltä 1900–2000.
def insert_rows(db):
    n = 1000000
    db.execute('BEGIN;')
    for i in range(n):
        name = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        year = random.randint(1900,2000)
        db.execute('INSERT INTO Elokuvat (nimi,vuosi) VALUES (?,?);', [name, year])
    db.execute('COMMIT;')
    db.commit()

# Ohjelma suorittaa tuhat kertaa kyselyn, jossa haetaan elokuvien määrä vuonna x. 
# Jokaisessa kyselyssä x valitaan satunnaisesti väliltä 1900–2000.
def make_queries(db):
    n = 1000
    for __ in range(n):
        db.execute('SELECT COUNT(*) FROM Elokuvat WHERE vuosi = ?;', [random.randint(1900,2000)])


# Testi 1
# Tauluun ei lisätä kyselyitä tehostavaa indeksiä.
# Ohjelma suorittaa tuhat kertaa kyselyn, jossa haetaan elokuvien määrä vuonna x. 
# Jokaisessa kyselyssä x valitaan satunnaisesti väliltä 1900–2000.
def test1(db,file):
    times = []
    # alustetaan tietokanta
    empty_db(db)

    # luodaan rivit ilman indeksiä
    start_time = time.time()
    insert_rows(db)
    times.append(time.time()-start_time)

    # suoritetaan kyselyt
    start_time = time.time()
    make_queries(db)
    times.append(time.time()-start_time)

    print('*** Testi 1 ***')
    print(f'Rivien lisäämiseen meni aikaa {times[0]} sekuntia')
    print(f'Kyselyiden suoritukseen meni aikaa {times[1]} sekuntia')
    print(
        f'Tietokannan koko päätteeksi: {os.path.getsize("/home/alex/tietokannat/IndeksinTehokkuus/"+file)*0.000001}')

# Tauluun lisätään kyselyitä tehostava indeksi ennen rivien lisäämistä.
def test2(db, file):
    times = []
    # alustetaan tietokanta
    empty_db(db)

    db.execute('CREATE INDEX idx_vuosi On Elokuvat (vuosi);')
    # luodaan rivit
    start_time = time.time()
    insert_rows(db)
    times.append(time.time()-start_time)

    # suoritetaan kyselyt
    start_time = time.time()
    make_queries(db)
    times.append(time.time()-start_time)

    print('*** Testi 2 ***')
    print(f'Rivien lisäämiseen meni aikaa {times[0]} sekuntia')
    print(f'Kyselyiden suoritukseen meni aikaa {times[1]} sekuntia')
    print(
        f'Tietokannan koko päätteeksi: {os.path.getsize("/home/alex/tietokannat/IndeksinTehokkuus/"+file)*0.000001}')

# Tauluun lisätään kyselyitä tehostava indeksi ennen kyselyiden suoritusta.
def test3(db, file):
    times = []
    # alustetaan tietokanta
    empty_db(db)

    # luodaan rivit
    start_time = time.time()
    insert_rows(db)
    times.append(time.time()-start_time)

    # suoritetaan kyselyt
    db.execute('CREATE INDEX idx_vuosi On Elokuvat (vuosi);')
    start_time = time.time()
    make_queries(db)
    times.append(time.time()-start_time)

    print('*** Testi 3 ***')
    print(f'Rivien lisäämiseen meni aikaa {times[0]} sekuntia')
    print(f'Kyselyiden suoritukseen meni aikaa {times[1]} sekuntia')
    print(f'Tietokannan koko päätteeksi: {os.path.getsize("/home/alex/tietokannat/IndeksinTehokkuus/"+file)*0.000001}')

if __name__ == '__main__':
    db = sqlite3.connect('data1.db')
    db.isolation_level = None
    test1(db, 'data1.db')
    db.close()
    db = sqlite3.connect('data2.db')
    db.isolation_level = None
    test2(db, 'data2.db')
    db.close()
    db = sqlite3.connect('data3.db')
    db.isolation_level = None
    test3(db, 'data3.db')
    db.close()

