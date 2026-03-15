import re
from dataclasses import dataclass

import log_setup
from transaction import Category, Transfer

log = log_setup.getLogger('matching')


@dataclass
class MatchCategory:
    match: str
    category: Category = Category.UNKNOWN
    priority: int = 100


def transfer_to_category(t: Transfer, o: str) -> Category:
    result = Category.UNKNOWN
    priority = 0

    for m in matches:
        if m.match.lower() in t.description.lower():

            # Custom rules
            if o == "fælles" and t.description.lower() == "overførsel":
                return Category.IGNORE


            # Default result
            if m.priority > priority:
                result = m.category
                priority = m.priority

    if result == Category.UNKNOWN:
        log.warning(f"Found no category for transfer '{t}'")

    return result

matches_income = [
    MatchCategory("LØNOVERFØRSEL", Category.SALARY),
    MatchCategory("Rente af indestående", Category.INCOME),
    MatchCategory("Børne- og Ungeydelse", Category.CHILD_MONEY),
    MatchCategory("Udbetaling tandskade", Category.INCOME),
    MatchCategory("BonusTryghedsGruppen", Category.INCOME),
    MatchCategory("Barselsdagpenge", Category.MATERNITY_ALLOWANCE),
    MatchCategory("danmark", Category.INCOME, 20),
    MatchCategory("SU", Category.SU, 10),
    MatchCategory("Vejdirektoratet", Category.SALARY),
    MatchCategory("OVERFØRSEL", Category.INCOME),
    MatchCategory("OVERSKYDENDE SKAT", Category.INCOME),
    MatchCategory("Lønover", Category.SALARY),
    MatchCategory("Advis", Category.INCOME),
    MatchCategory("Feriepenge", Category.SALARY),
    MatchCategory("placeholder", Category.INCOME),
    MatchCategory("placeholder", Category.INCOME),
]

matches_housing = [
    MatchCategory("IKEA", Category.FURNITURE),
    MatchCategory("Betalingsservice P/S MARSHALLS ALLE", Category.RENT_AND_LOAN),
    MatchCategory("Betalingsservice AALBORG FORSYNING", Category.EL_WATER_HEATING),
    MatchCategory("Betalingsservice NORLYS ENERGI", Category.EL_WATER_HEATING),
    MatchCategory("placeholder", Category.HOUSING),
]

matches_food_and_household = [
    MatchCategory("Coop App", Category.GROCERIES, 200),
    MatchCategory("MENY", Category.GROCERIES, 50),
    MatchCategory("BILKA", Category.GROCERIES),
    MatchCategory("SPAR", Category.GROCERIES),
    MatchCategory("Fakta", Category.GROCERIES),
    MatchCategory("F Notanr", Category.GROCERIES),
    MatchCategory("REMA 1000", Category.GROCERIES),
    MatchCategory("LIDL", Category.GROCERIES),
    MatchCategory("NETTO", Category.GROCERIES),
    MatchCategory("Kvickly", Category.GROCERIES),
    MatchCategory("COOP365", Category.GROCERIES),
    MatchCategory("MIN K", Category.GROCERIES, 50),
    MatchCategory("SuperB", Category.GROCERIES, 50),
    MatchCategory("249AALBORGGRONLANDSTOR", Category.GROCERIES),
    MatchCategory("AALBORG STORCENTER", Category.GROCERIES),
    MatchCategory("Batteribyen", Category.GROCERIES),
    MatchCategory("berrybean", Category.GROCERIES),
    MatchCategory("HELLOFRESH", Category.GROCERIES),
    MatchCategory("ÅLBORG STORCENT", Category.GROCERIES),
    MatchCategory("ALLSWEETS", Category.GROCERIES),
    MatchCategory("BERRY&BEAN", Category.GROCERIES),
    MatchCategory("NORMAL", Category.GROCERIES),
    MatchCategory("MOTATOS", Category.GROCERIES),
    MatchCategory("KANPLA", Category.GROCERIES),
    MatchCategory("basicclean.dk", Category.GROCERIES),
    MatchCategory("bager", Category.BAKERY_AND_SPECIALS, priority=70),
    MatchCategory("GISTRUP BAGERI", Category.BAKERY_AND_SPECIALS),
    MatchCategory("lagkagehuset", Category.BAKERY_AND_SPECIALS),
    MatchCategory("PENNY LANE", Category.BAKERY_AND_SPECIALS),
    MatchCategory("ISVAERFTET", Category.BAKERY_AND_SPECIALS),
    MatchCategory("VEJGAARD BAGERI", Category.BAKERY_AND_SPECIALS),
    MatchCategory("OTHELLOBAGERIET", Category.BAKERY_AND_SPECIALS),
    MatchCategory("PARADIS AALBORG", Category.BAKERY_AND_SPECIALS),
    MatchCategory("TGTG", Category.BAKERY_AND_SPECIALS),
    MatchCategory("ISMEJERI", Category.BAKERY_AND_SPECIALS),
    MatchCategory("JUMBO MINDET", Category.BAKERY_AND_SPECIALS),
    MatchCategory("Okkels", Category.BAKERY_AND_SPECIALS),
    MatchCategory("Guf", Category.BAKERY_AND_SPECIALS),
    MatchCategory("Blokhus forretning", Category.BAKERY_AND_SPECIALS),
    MatchCategory("VESTERPORTS BAG", Category.BAKERY_AND_SPECIALS),
    MatchCategory("Ostebutik", Category.BAKERY_AND_SPECIALS),
    MatchCategory("KILDEGÅRD LAND", Category.BAKERY_AND_SPECIALS),
    MatchCategory("Zettle_*BALLAST BAR", Category.BAKERY_AND_SPECIALS),
    MatchCategory("GELATO", Category.BAKERY_AND_SPECIALS),
    MatchCategory("KLINGENBERG OST", Category.BAKERY_AND_SPECIALS),
    MatchCategory("DELICIOUS FACTORY", Category.BAKERY_AND_SPECIALS),
    MatchCategory("LABC DEL GUSTO", Category.BAKERY_AND_SPECIALS),  # Fudge
    MatchCategory("SURDEJSBAGEREN", Category.BAKERY_AND_SPECIALS),
    MatchCategory("MCD", Category.RESTAURANT_AND_CAFE, 40),
    MatchCategory("Burger King", Category.RESTAURANT_AND_CAFE),
    MatchCategory("STUDENTERHUS AA", Category.RESTAURANT_AND_CAFE),
    MatchCategory("SOGAARD'S BRYGH", Category.RESTAURANT_AND_CAFE),
    MatchCategory("Bone's Skalborg", Category.RESTAURANT_AND_CAFE),
    MatchCategory("eRestaurant Notanr", Category.RESTAURANT_AND_CAFE),
    MatchCategory("THE BUDDHA BOWL", Category.RESTAURANT_AND_CAFE),
    MatchCategory("NADIAS SANDWICH", Category.RESTAURANT_AND_CAFE),
    MatchCategory("CAFE", Category.RESTAURANT_AND_CAFE),
    MatchCategory("PastaLab1", Category.RESTAURANT_AND_CAFE),
    MatchCategory("PINGVIN TAPAS", Category.RESTAURANT_AND_CAFE),
    MatchCategory("MealoTakeaway", Category.RESTAURANT_AND_CAFE),
    MatchCategory("JULIETTE APS", Category.RESTAURANT_AND_CAFE),
    MatchCategory("AZZURRA", Category.RESTAURANT_AND_CAFE),
    MatchCategory("placeholder", Category.FOOD_AND_HOUSEHOLD),
]

matches_ignore = [
    MatchCategory("Penge til fælles", Category.IGNORE),
    MatchCategory("FÆLLES", Category.IGNORE),
    MatchCategory("Til Fælles", Category.IGNORE),
    MatchCategory("Til LSBprivat Budget", Category.IGNORE),
    MatchCategory("Til Budgetkonto", Category.IGNORE),
    MatchCategory("Fast penge Kristian", Category.IGNORE),
    MatchCategory("placeholder", Category.IGNORE),
]

matches_opsparing = [
    MatchCategory("Overført 0101152310", Category.SAVINGS),  # Aktier
    MatchCategory("Overført 0101352030", Category.SAVINGS),  # Aktier
]

matches_fixed = [
    MatchCategory("Mobil, Netflix mm.", Category.PHONE),
    MatchCategory("Betalingsservice THIELE", Category.GLASSES_AND_LENSES),
    MatchCategory("Podimo", Category.TV_STREAMING),
    MatchCategory("Mofibo", Category.TV_STREAMING),
    MatchCategory("Mobil", Category.PHONE, 10),
    MatchCategory("Betalingsservice TRYG", Category.INSURANCE),
    MatchCategory("tryg", Category.INSURANCE, priority=50),
    MatchCategory("Betalingsservice IDA", Category.UNION),
    MatchCategory("Betalingsservice AKADEMIKERNES A-KASSE", Category.UNION),
    MatchCategory("AKADEMIKERNES A-K", Category.UNION),
    MatchCategory("Betalingsservice AALBORG KOMMUNE", Category.INSTITUTION),
    MatchCategory("Betalingsservice AP PENSION", Category.INSURANCE),
    MatchCategory("Til A-kasse", Category.UNION),
]

matches_transport = [
    MatchCategory("Delebil", Category.VEHICLE_LOAN),
    MatchCategory("DMR period. afgift", Category.GREEN_TAX),
    MatchCategory("AUTOMOBILER", Category.REPAIR_AND_WHEELS),
    MatchCategory("S. ERIKSEN", Category.REPAIR_AND_WHEELS),
    MatchCategory("Shell", Category.FUEL_AND_PARKING),
    MatchCategory("OK Svenstrup", Category.FUEL_AND_PARKING),
    MatchCategory("CIRCLE K", Category.FUEL_AND_PARKING),
    MatchCategory("Uno-X", Category.FUEL_AND_PARKING),
    MatchCategory("1-2-3 ST. BINDERUP", Category.FUEL_AND_PARKING),
    MatchCategory("OIL tank", Category.FUEL_AND_PARKING),
    MatchCategory("EasyPark", Category.FUEL_AND_PARKING),
    MatchCategory("DSB APP", Category.PUBLIC_TRANSPORTATION),
    MatchCategory("Rejsekort", Category.PUBLIC_TRANSPORTATION),
    MatchCategory("Molslinjen", Category.PUBLIC_TRANSPORTATION),
    MatchCategory("aeroeferrydk", Category.PUBLIC_TRANSPORTATION),
    MatchCategory("aeroe-ferry", Category.PUBLIC_TRANSPORTATION),
    MatchCategory("aeroexpres", Category.PUBLIC_TRANSPORTATION),
    MatchCategory("AEROXPRESSEN", Category.PUBLIC_TRANSPORTATION),
    MatchCategory("cykelgear.dk", Category.BICYCLE),
    MatchCategory("FRI BIKESHOP", Category.BICYCLE),
    MatchCategory("cykelpartner.d", Category.BICYCLE),
    MatchCategory("cykelpartner", Category.BICYCLE),
    MatchCategory("Buckaroo", Category.BICYCLE),
    MatchCategory("placeholder", Category.TRANSPORT),
]

matches_misc = [
    MatchCategory("MobilePay", Category.MISC, priority=30),
    MatchCategory("Mob.Pay", Category.MISC, priority=30),
    MatchCategory("Blizzard Entertainment", Category.MISC),
    MatchCategory("Google Play Apps", Category.MISC),
    MatchCategory("POWER Aalborg", Category.MISC),
    MatchCategory("GUG ANLAG OG PL", Category.MISC),
    MatchCategory("TANDLGENDK", Category.MISC),
    MatchCategory("TANDLAEGEN", Category.MISC),
    MatchCategory("revolutionrac", Category.MISC),
    MatchCategory("BAHNE", Category.MISC),
    MatchCategory("AMZN", Category.MISC),
    MatchCategory("NIELSENS", Category.MISC),
    MatchCategory("Elgiganten", Category.MISC),
    MatchCategory("BAUHAUS", Category.MISC),
    MatchCategory("On AG, Zurich", Category.MISC),
    MatchCategory("WWW.BOG-IDE.DK", Category.MISC),
    MatchCategory("STEAMGAMES.COM", Category.MISC),
    MatchCategory("eyda.dk", Category.MISC),
    MatchCategory("thimms.yogo", Category.MISC),
    MatchCategory("camillakroeyer", Category.MISC),
    MatchCategory("OnReg.com", Category.MISC),
    MatchCategory("IMERCO", Category.MISC),
    MatchCategory("ICIW.COM", Category.MISC),
    MatchCategory("Transfer", Category.MISC, 40),
    MatchCategory("sokind.com", Category.MISC),
    MatchCategory("Bestseller AS", Category.MISC),
    MatchCategory("IDA INGENI Notanr", Category.MISC),
    MatchCategory("Nordisk Film Biografer", Category.MISC),
    MatchCategory("micare.dk", Category.MISC),
    MatchCategory("anewsleep.dk", Category.MISC),
    MatchCategory("HM", Category.MISC, 40),
    MatchCategory("APPLE.COM", Category.MISC),
    MatchCategory("MED24", Category.MISC),
    MatchCategory("Vinduespudser", Category.MISC),
    MatchCategory("proshop.dk", Category.MISC),
    MatchCategory("APOTEK", Category.MISC),
    MatchCategory("SILVAN", Category.MISC),
    MatchCategory("Peach Fuzz", Category.MISC),
    MatchCategory("Zalando", Category.MISC),
    MatchCategory("MH", Category.MISC, 40),
    MatchCategory("SP HYPE", Category.MISC),
    MatchCategory("Hermans Hule", Category.MISC),
    MatchCategory("AALBORG LOVE AP", Category.MISC), # Apotek
    MatchCategory("SALLING", Category.MISC),
    MatchCategory("BILTEMA", Category.MISC),
    MatchCategory("BOG & ID", Category.MISC),
    MatchCategory("BR", Category.MISC, 40),
    MatchCategory("puzzle YOU", Category.MISC),
    MatchCategory("GIGANTIUM", Category.MISC),
    MatchCategory("AALBORG O FYRKILDEN", Category.MISC),
    MatchCategory("NORDISK FILM", Category.MISC),
    MatchCategory("apopro.dk", Category.MISC),
    MatchCategory("UNIVERSITETS AP", Category.MISC),  # Apotek
    MatchCategory("DILLING A/S", Category.MISC),
    MatchCategory("petiteknit", Category.MISC),
    MatchCategory("HJEM-IS DANMARK", Category.MISC),
    MatchCategory("harald nyborg", Category.MISC),
    MatchCategory("prikogstreg", Category.MISC),
    MatchCategory("nintendo", Category.MISC),
    MatchCategory("placeholder", Category.MISC),
]

matches_sport = [
    MatchCategory("BOOKLI", Category.PADEL),
    MatchCategory("Padel", Category.PADEL, 50),
    MatchCategory("DPF SPILLERLICENS", Category.PADEL),
    MatchCategory("LEDAP* PP AALBORG", Category.PADEL),
    MatchCategory("padelspecialist", Category.PADEL),
    MatchCategory("ROCKET PADEL RANDERS", Category.PADEL),
    MatchCategory("ZERV ApS", Category.PADEL),
    MatchCategory("Q*ongoal.se", Category.PADEL),
    MatchCategory("Tennis", Category.PADEL),
    MatchCategory("NemTilmeld.dk", Category.PADEL),
    MatchCategory("Crossfit", Category.CROSSFIT, 50),
    MatchCategory("apuls.dk", Category.CROSSFIT),
    MatchCategory("aroxfitness", Category.CROSSFIT),
    MatchCategory("UFILTRERET PROGRAM", Category.CROSSFIT),
    MatchCategory("Fitness Engros", Category.CROSSFIT),
    MatchCategory("Fusion Sportswear", Category.RUNNING),
    MatchCategory("sportstiming", Category.SPORT),
    MatchCategory("Watery.dk", Category.SPORT),
    MatchCategory("Garmin, Southampton", Category.SPORT),
    MatchCategory("Strava", Category.SPORT),
    MatchCategory("placeholder", Category.SPORT),
]

mp_truncate_length = 10
padel_mp_modify_names = [
    "Ali Al Ali",
    "Allan Amstrup",
    "Anders Ulrich",
    "Bo Lynge",
    "Bo Ravn",
    "Casper Mahnecke",
    "Christian Frimor",
    "Danni Vinther-Jensen",
    "Dennis Harbøll Nielsen",
    "Emil Hovalt Byrresen",
    "Henrik Grønbek Palm",
    "Henrik Kristensen",
    "Jacob Sejer Chris",
    "Jes Nørgaard Nielsen",
    "Jesper Düring",
    "Jesper Frø",
    "Jesper Ger",
    "Jesper Lolk Søltoft",
    "Joakim Ishøi Hjorth",
    "Joakim Sloth Hjorth",
    "Jonas Pedersen",
    "Jørn Østergaard",
    "Kasper Hjørringga",
    "Kasper Pou",
    "Kim Nørgaard Nielsen",
    "Kristian Nikolai",
    "Lars Kiær",
    "Lars Rasmussen",
    "Lars Tølbøl Frøli",
    "Lasse Todberg",
    "Lasse Nørgaard Fr",
    "Lucas Baand Busk",
    "Mads Frost",
    "Magnus Koldkjær",
    "Malte Ahrenfeldt",
    "Martin Winther",
    "Matej Vinko Primorac",
    "Michael Hasselager",
    "Michael Sk",
    "Mike Nikke",
    "Michel Jos",
    "Morten Henriksen",
    "Morten Skole",
    "Nichlas Middelhede",
    "Nicolai Astor Molsen",
    "Nicolaj Juhl",
    "Nicolai Ta",
    "Peter Baagøe",
    "Rasmus Færch Bros",
    "Rasmus Nygaard",
    "Rasmus Nøhr",
    "René Sørensen",
    "Simon Anker Hansen",
    "Simon Astrup Chri",
    "Thomas Casper Olesen",
    "Thomas Olesen",
    "Claes Rydahl Stahlhut",
    "Allan Busk-Matthiasen",
    "Dino Krupic ",
    "Emil Hovalt Byrresen",
    "Emil Sander Abildgaard",
    "Lars Lund Rafn",
    "Mads Nygaard Madsen",
    "Michael Jensen",
    "Mikkel Svejstrup Højsleth",
    "Nicklas Brandt Holm",
    "Nicklas Madsgaard",
    "Sune Köhne Lind",
    "Simon Helge",
    "Thim Munkholm Christensen",
    "Thomas Møller Bendsen",
    "Tobias Skov Frederiksen",
    "Peter Borup Christensen",
    "Thomas Kærsgaard",
    "Rasmus Nørlem",
    "Michael Aagaard",
    "simon lyngsø jensen",
    "morten anneberg j",
    "kenneth dalsgaard anderse",
    "mads donbæk møller",
    "placeholder",
    "placeholder",
    "placeholder",
    "placeholder",
    "placeholder",
]
matches_sport_new_mp = [MatchCategory(f"MobilePay {name[0:mp_truncate_length]}", Category.PADEL) for name in padel_mp_modify_names]
# for m in matches_sport_new_mp:
#     print(m)

matches_sport += matches_sport_new_mp

matches_vacation = [
    MatchCategory("Hotel Aurora", Category.VACATION),
    MatchCategory("DIKTN A", Category.VACATION),
    MatchCategory("Achenrain Huette", Category.VACATION),
    MatchCategory("SKIWORLD PASSHOEHE", Category.VACATION),
    MatchCategory("Apollo", Category.VACATION),
    MatchCategory("HURGHADA", Category.VACATION),
    MatchCategory("MADPOINT RENT A CAR", Category.VACATION),
    MatchCategory("Obertauern", Category.VACATION),
    MatchCategory("Feucht", Category.VACATION),
    MatchCategory("FUNCHAL", Category.VACATION),
    MatchCategory("Restaurante Calamar", Category.VACATION),
    MatchCategory("NORWEGIAN", Category.VACATION),
    MatchCategory("Inflight Services", Category.VACATION),
    MatchCategory("CASA DO FAROL", Category.VACATION),
    MatchCategory("MADEIRA", Category.VACATION),
    MatchCategory("AIRBNB", Category.VACATION),
    MatchCategory("RED SEA", Category.VACATION),
    MatchCategory("Soltau", Category.VACATION),
    MatchCategory("Burghaun", Category.VACATION),
    MatchCategory("Hepberg", Category.VACATION),
    MatchCategory("AALBORG LUFTHAV", Category.VACATION),
    MatchCategory("VETERANBANEN-FAABORG", Category.VACATION),
    MatchCategory("placeholder", Category.VACATION),
]

matches_debt = [
    MatchCategory("Til Frivillig ind skat", Category.DEBT),
]

matches_other = [
    MatchCategory("Anton investering", Category.OTHER),
    MatchCategory("Skatteforvaltningen", Category.OTHER),
    MatchCategory("Anton investering", Category.OTHER),
    MatchCategory("Anton investering", Category.OTHER),
    MatchCategory("Anton investering", Category.OTHER),
]

matches = [
    *matches_income,
    *matches_housing,
    *matches_food_and_household,
    *matches_fixed,
    *matches_transport,
    *matches_misc,
    *matches_sport,
    *matches_vacation,
    *matches_opsparing,
    *matches_ignore,
    *matches_other,
    *matches_debt,
]