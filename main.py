from datetime import datetime, timedelta


class Szoba:
    def __init__(self, ar, szobaszam, type):
        self.ar = ar
        self.szobaszam = szobaszam
        self.type = type


class Egyagyasszoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=10, szobaszam=szobaszam, type="Egyágyas Szoba")


class Ketagyasszoba(Szoba):
    def __init__(self, szobaszam):
        super().__init__(ar=20, szobaszam=szobaszam, type="Kétágyas Szoba")


class Szalloda:
    def __init__(self, nev):
        self.nev = nev
        self.szobak = []
        self.foglalasok = []

    def szalloda_feltoltes(self, szoba):
        self.szobak.append(szoba)

    def foglalas_felvetel(self, szobaszam, datum):
        for szoba in self.szobak:
            if szoba.szobaszam == szobaszam:
                foglalas = Foglalas(szoba, datum)
                if datum > datetime.now():
                    if len(self.foglalasok) > 0:
                        for foofoglalas in self.foglalasok:
                            if (foofoglalas.datum != foglalas.datum):
                                self.foglalasok.append(foglalas)
                                return szoba.ar
                            else:
                                return "Erre az időpontra már van foglalás"
                    else:
                        self.foglalasok.append(foglalas)
                        return szoba.ar
                else:
                    return "Csak jövőbeli dátumot adhatsz meg"
        return None

    def foglalas_lemondas(self, foglalas):
        if foglalas in self.foglalasok:
            self.foglalasok.remove(foglalas)
            return True
        else:
            return False

    def return_foglalasok(self):
        for foglalas in self.foglalasok:
            print(
                f'Szobaszám: {foglalas.szoba.szobaszam}, Ár: {foglalas.szoba.ar}, Szoba Típusa: {foglalas.szoba.type}, Foglalás Dátuma: {foglalas.datum}')


class Foglalas:
    def __init__(self, szoba, datum):
        self.szoba = szoba
        self.datum = datum


def feltolt_szalloda(szalloda):
    szalloda.szalloda_feltoltes(Egyagyasszoba(101))
    szalloda.szalloda_feltoltes(Ketagyasszoba(102))
    szalloda.szalloda_feltoltes(Egyagyasszoba(103))

    szalloda.foglalas_felvetel(szobaszam=101, datum=datetime.now() + timedelta(days=1))
    szalloda.foglalas_felvetel(szobaszam=102, datum=datetime.now() + timedelta(days=2))
    szalloda.foglalas_felvetel(szobaszam=103, datum=datetime.now() + timedelta(days=3))
    szalloda.foglalas_felvetel(szobaszam=101, datum=datetime.now() + timedelta(days=4))
    szalloda.foglalas_felvetel(szobaszam=102, datum=datetime.now() + timedelta(days=5))


def main():
    szalloda = Szalloda("Szalloda")
    feltolt_szalloda(szalloda)

    while True:
        print("\nMit akarsz csinálni?")
        print("1. Szoba foglalás")
        print("2. Foglalás törlés")
        print("3. Foglalások listázája")
        print("4. Kilépés")

        valasztas = input("Választás: ")

        match valasztas:
            case "1":
                szobaszam = int(input("Add meg a szobaszámot: "))
                datum_str = input("Add meg a foglalás dátumát (YYYY-MM-DD formátumban): ")
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
                ar = szalloda.foglalas_felvetel(szobaszam, datum)
                if ar:
                    print(f"A foglalás sikeres, ára: {ar}")
                else:
                    print("Nincs ilyen szoba vagy foglalás már erre a dátumra")

            case "2":
                print("Kérem, adja meg a foglalás adatait:")
                szobaszam = int(input("Szobaszám: "))
                datum_str = input("Dátum (YYYY-MM-DD formátumban): ")
                datum = datetime.strptime(datum_str, "%Y-%m-%d")
                foglalas = None
                for f in szalloda.foglalasok:
                    if f.szoba.szobaszam == szobaszam and f.datum == datum:
                        foglalas = f
                        break
                if foglalas:
                    szalloda.foglalas_lemondas(foglalas)
                    print("A foglalás törölve.")
                else:
                    print("Nem található ilyen foglalás.")

            case "3":
                szalloda.return_foglalasok()

            case "4":
                print("Kilépés...")
                break

            case _:
                print("Érvénytelen választás.")


if __name__ == "__main__":
    main()
