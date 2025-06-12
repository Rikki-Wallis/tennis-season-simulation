# Imports
from tournament import GrandSlam, Master1000, ATP500, ATP250


class Season:
    def __init__(self):
        self.init_tournaments()

    def init_tournaments(self):
        """
        Method:
            Creates the tournament schedule
        """
        # December
        brisbane_international = ATP250("Hard", "Brisbane International")
        hong_kong_open = ATP250("Hard", "Hong Kong Open")

        # January
        adelaide_international = ATP250("Hard", "Adelaide Internationale")
        auckland = ATP250("Hard", "ASB Classic")
        australian_open = GrandSlam("Hard", "AO")
        montpellier = ATP250("Hard", "Open Occitaine")

        # February
        dallas_open = ATP500("Hard", "Dallas Open")
        rotterdam = ATP500("Hard", "ABN AMRO Open")
        marseille = ATP250("Hard", "Open 13 Provence")
        delray_beach = ATP250("Hard", "Delray Beach Open")
        argentina = ATP250("Hard", "IEB+ Argentina Open")
        qatar = ATP500("Hard", "Qatar ExonnMobil Open")
        rio = ATP500("Hard", "Rio Open")
        dubai = ATP500("Hard", "Dubai Duty Free Tennis Chamionships")
        acapulco = ATP500("Hard", "Acapulco")
        santiago = ATP250("Hard", "Movistar Chile Open")

        # March
        indian_wells = Master1000("Hard", "BNP Paribas Open")
        miami = Master1000("Hard", "Miami Open")
        houston = ATP250("Clay", "Houston Open")
        morocco = ATP250("Clay", "Grand Prix Hassan II")
        romania = ATP250("Clay", "Bucharest Open")

        # April
        monte_carlo = Master1000("Clay", "Rolex Monte-Carlo Masters")
        barcelona = ATP500("Clay", "Barcelona Open")
        munich = ATP500("Clay", "BMW Open")
        madrid = Master1000("Clay", "Mutua Madrid Open")

        # May
        rome = Master1000("Clay", "Internazionali BNL d'Italia")
        hamburg = ATP500("Clay", "Hamburg Open")
        geneva = ATP250("Clay", "Gonet Geneva Open")
        roland_garros = GrandSlam("Clay", "Roland Garros")

        # June
        stuttgart = ATP250("Grass", "BOSS Open")
        libema = ATP250("Grass", "Libema Open")
        hsbc_champs = ATP500("Grass", "HSBC Championships")
        halle = ATP500("Grass", "Terra Wortmann Open")
        mallorca = ATP250("Grass", "Mallorca Championships")
        eastbourne = ATP250("Grass", "Lexus Eastbourne Open")
        wimbledon = GrandSlam("Grass", "Wimbledon")

        # July
        los_cabos = ATP250("Hard", "Mifel Tennis Open")
        gstaad = ATP250("Clay", "EFG Swiss Open Gstaad")
        nordea = ATP250("Clay", "Nordea Open")
        generali = ATP250("Clay", "Generali Open")
        umag = ATP250("Clay", "Croatia Open")
        washington = ATP500("Hard", "DC Open")
        toronto = Master1000("Hard", "Toronto Open")

        # August
        cincinatti = Master1000("Hard", "Cincinatti Open")
        winston_salem = ATP250("Hard", "Winston-Salem Open")
        us_open = GrandSlam("Hard", "US Open")

        # September
        chengdu = ATP250("Hard", "Chengdu Open")
        hangzhou = ATP250("Hard", "Hangzhou Open")
        tokyo = ATP500("Hard", "Tokyo Open")
        china = ATP500("Hard", "China Open")

        # October
        shangai = Master1000("Hard", "Shanghai Masters")
        almaty = ATP250("Hard", "Almaty Open")
        stockholm = ATP250("Hard", "BNP Paribas Nordic Open")
        brussels = ATP250("Hard", "European Open")
        vienna = ATP500("Hard", "Erste Bank Open")
        basel = ATP500("Hard", "Swiss Indoors Basel")
        paris_masters = Master1000("Hard", "Rolex Paris Masters")

        # November
        belgrade = ATP250("Hard", "Belgrade Open")
        moselle = ATP250("Hard", "Moselle Open")

        self.tournamentSchedule = [
            (brisbane_international, hong_kong_open),
            (adelaide_international, auckland),
            (australian_open),
            (montpellier),
            (dallas_open, rotterdam),
            (marseille, delray_beach, argentina),
            (qatar, rio),
            (dubai, acapulco, santiago),
            (indian_wells),
            (miami),
            (houston, morocco, romania),
            (monte_carlo),
            (barcelona, munich),
            (madrid),
            (rome),
            (hamburg, geneva),
            (roland_garros),
            (stuttgart, libema),
            (hsbc_champs, halle),
            (mallorca, eastbourne),
            (wimbledon),
            (los_cabos, gstaad, nordea),
            (generali, umag, washington),
            (toronto),
            (cincinatti),
            (winston_salem),
            (us_open),
            (chengdu, hangzhou),
            (tokyo, china),
            (shangai),
            (almaty, stockholm, brussels),
            (vienna, basel),
            (paris_masters),
            (belgrade, moselle),
        ]
