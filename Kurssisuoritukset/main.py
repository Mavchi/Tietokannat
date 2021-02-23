import sqlite3
con = sqlite3.connect('kurssit.db')

c = con.cursor()


def menu_items():
    print('______________________________________________________________')
    print('1. Laske annettuna vuonna saatujen opintopisteiden yhteismäärä.')
    print('2. Tulosta annetun opiskelijan kaikki suoritukset aikajärjestyksessä.')
    print('3. Tulosta annetun kurssin suoritusten arvosanojen jakauma.')
    print('4. Tulosta top x eniten opintopisteitä antaneet opettajat.')
    print('5. Sulje ohjelma.')
    print()


def credit_sum_by_year(c):
    year = input('Anna vuosi: ')
    query = (
        f'SELECT SUM(K.laajuus) '
        f'FROM Kurssit as K, Suoritukset as S '
        f'WHERE S.kurssi_id=K.id and SUBSTRING(S.paivays,1,4)="{year}";'
    ) 
    c.execute(query)
    print('Opintopisteiden määrä:', c.fetchone()[0])

def student_credits(c):
    student_name = input('Anna opiskelijan nimi: ')
    query = (
        f'SELECT K.nimi, K.laajuus, S.paivays, S.arvosana '
        f'FROM Opiskelijat as O, Kurssit as K, Suoritukset as S '
        f'WHERE S.opiskelija_id=O.id and S.kurssi_id=K.id and O.nimi="{student_name}" '
        f'GROUP BY K.id '
        f'ORDER BY S.paivays;'
    )
    c.execute(query)
    result = c.fetchall()
    print('{:10} {:10} {:15} {}'.format('kurssi', 'op', 'päiväys', 'arvosana'))
    #print(f"'kurssi':10 'op':10 'päiväys': 15 'arvosana'")
    for course in result:
        print(f'{course[0]:10} {course[1]:10} {course[2]:15} {course[3]}')

def grade_distribution(c):
    course_name = input('Anna kurssin nimi: ')
    for grade in range(1,6):
        query = (
            f'SELECT COUNT(S.arvosana) '
            f'FROM Kurssit as K, Suoritukset as S '
            f'WHERE S.kurssi_id=K.id and K.nimi="{course_name}" AND S.arvosana="{grade}";'
        )
        c.execute(query)
        print(f'Arvosana {grade}: {c.fetchone()[0]} kpl')

def top_teachers(c):
    n = int(input('Anna opettajien määrä: '))
    query = (
        f'SELECT O.nimi, SUM(K.laajuus) '
        f'FROM Opettajat as O, Kurssit as K, Suoritukset as S '
        f'WHERE S.kurssi_id=K.id AND K.opettaja_id=O.id '
        f'GROUP BY O.id '
        f'ORDER BY SUM(K.laajuus) DESC;'
    )
    c.execute(query)
    result = c.fetchall()
    print('{:20} {:15}'.format('opettaja', 'op'))
    for i in range(n):
        print('{:20} {:15}'.format(result[i][0], result[i][1]))

if __name__=='__main__':
    while True:
        menu_items()

        choise = input('Valitse toiminto: ')
        # Laske annettuna vuonna saatujen opintopisteiden yhteismäärä.
        if choise == '1':
            credit_sum_by_year(c)
        # Tulosta annetun opiskelijan kaikki suoritukset aikajärjestyksessä.
        elif choise == '2':
            student_credits(c)
        # Tulosta annetun kurssin suoritusten arvosanojen jakauma.
        elif choise == '3':
            grade_distribution(c)
        # Tulosta top x eniten opintopisteitä antaneet opettajat.
        elif choise == '4':
            top_teachers(c)
        elif choise == '5':
            con.close()
            break;
        else:
            print('Väärä valinta (1-5)')
