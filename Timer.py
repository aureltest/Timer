from datetime import datetime, timedelta
import time


class Timer:
    def __init__(self, secondes, minutes, heure, jour, jour_semaine, mois, annee):
        self.secondes = secondes
        self.minutes = minutes
        self.heure = heure
        self.jour = jour
        self.jour_semaine_actuel = jour_semaine
        self.mois = mois
        self.annee = annee
        self.is_bissextile = False
        self.stop_count = False

        self.noms_jours = {
            0: "Lundi",
            1: "Mardi",
            2: "Mercredi",
            3: "Jeudi",
            4: "Vendredi",
            5: "Samedi",
            6: "Dimanche",
        }

        self.noms_mois = [
            "janvier",
            "février",
            "mars",
            "avril",
            "mai",
            "juin",
            "juillet",
            "août",
            "septembre",
            "octobre",
            "novembre",
            "decembre",
        ]

        self.jours_par_mois = {
            "janvier": 31,
            "février": 28,
            "mars": 31,
            "avril": 30,
            "mai": 31,
            "juin": 30,
            "juillet": 31,
            "août": 31,
            "septembre": 30,
            "octobre": 31,
            "novembre": 30,
            "decembre": 31,
        }

    def is_bissextile(self):
        if self.annee % 400 == 0:
            bissextile = True
        elif self.annee % 100 == 0:
            bissextile = False
        elif self.annee % 4 == 0:
            bissextile = True
        return bissextile

    def increment_time(self):
        self.secondes += 1
        if self.secondes == 60:
            self.secondes = 0
            self.minutes += 1
            if self.minutes == 60:
                self.minutes = 0
                self.heure += 1
                if self.heure > 23:
                    self.heure = 0
                    self.jour += 1
                    self.jour_semaine_actuel += 1
                    self.jour_semaine_actuel = self.jour_semaine_actuel % 7
                    mois_actuel = self.noms_mois[self.mois - 1]
                    nb_jour_par_mois = self.jours_par_mois.get(mois_actuel)
                    if self.jour > nb_jour_par_mois:
                        self.jour = 1
                        self.mois += 1
                        if self.mois > 12:
                            self.mois = 1
                            self.annee += 1
                            self.jours_par_mois["février"] = (
                                29 if self.is_bissextile() else 28
                            )

    def format_display(self):
        mois_actuel = self.noms_mois[self.mois - 1]
        jour_actuel = self.noms_jours[self.jour_semaine_actuel]
        return f"Il est {self.heure:02d}:{self.minutes:02d}:{self.secondes:02d} le {jour_actuel} {self.jour} {mois_actuel} {self.annee}"

    def get_target_date(self):
        date_str = input("Entrez une date (format:JJ/MM/AAAA)")
        choix = input("Voulez vous préciser l'heure ? (o/n):")
        if choix.lower() == "o":
            time_str = input("Entrez l'heure (format: HH:MM) : ")
            date_complete = f"{date_str} {time_str}"
        else:
            date_complete = f"{date_str} 00:00"
        format_date = "%d/%m/%Y %H:%M"
        return datetime.strptime(date_complete, format_date)

    def count_until_date(self):
        target_date = self.get_target_date()
        while not self.stop_count:
            current_date = datetime(
                self.annee,
                self.mois,
                self.jour,
                self.heure,
                self.minutes,
                self.secondes,
            )
            delta = target_date - current_date
            if delta.total_seconds() <= 0:
                print("Date atteinte !")
                break

            delta_days = delta.days
            delta_hour = delta.seconds // 3600
            reste_seconds = delta.seconds % 3600
            delta_minutes = reste_seconds // 60
            delta_sec = reste_seconds % 60
            print(
                f"Il reste {delta_days} jours, {delta_hour} heures, {delta_minutes} minutes, {delta_sec} secondes"
            )
            self.increment_time()
            time.sleep(1)


now = datetime.now()
compteur_temps = Timer(
    now.second, now.minute, now.hour, now.day, now.weekday(), now.month, now.year
)
compteur_temps.count_until_date()
