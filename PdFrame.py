import pandas as pd
import CarScrapper as cs
import pickle


def load_cars():
    print("Load cars")
    cars = cs.car_dicts(1, 3)
    pickle.dump(cars, open("loaded_cars.pickle", "wb"))

def reorer_df(df):
    neworder = [
        'vehid',
        'titel',
        'Leistung in PS',
        'Preis(chf)',
        'Anhangelast(kg)',
        'Antriebsart',
        'Aussenfarbe',
        'Energieeffizienz',
        'Euro Norm',
        'Fahrzeugart',
        'Getriebeart',
        'Hubraum(ccm2)',
        'Inverkehrsetzung',
        'Kilometer',
        'Leergewicht(kg)',
        'Neupreis(chf)',
        'Sitze',
        'Treibstoff',
        'Türen',
        'Zylinder',
        'co2emission(g/km)',
        'klasse',
        'marke',
        'mfk',
        'verbrauch_land',
        'verbrauch_stadt',
        'verbrauch_total',

        '2-Zonen-Klimaautomatik',
        '3 Kopfstützen hinten',
        '5-Gang-Getriebe',
        '6-Gang-Getriebe',
        'Airbag Fahrer und Beifahrer',
        'Allradantrieb permanent',
        'Antiblockiersystem (ABS)',
        'ABS, EBD elektronische Bremskraft- verteilung',
        'ABS und TCS',
        'Aussenspiegel elektrisch verstellbar',
        'Automatische Stabilitäts- und Traktions- kontrolle',
        'Aux-In Anschluss',
        'Beleuchtetes Handschuhfach',
        'Bordcomputer',
        'Bluetooth Freisprecheinrichtung',
        'Bremsassistent (BAS)',
        'Dachspoiler',
        'Drehzahlmesser',
        'Direkt-/Parallelimport',
        'Drittes Bremslicht',
        'ECO Start-Stopp-Funktion',
        'Einparkhilfe',
        'Elektrische Fensterheber hinten',
        'Elektrische Fensterheber vorne',
        'Elektrische Fensterheber vorne + hinten',
        'Elektrische Heckklappe',
        'Elektronisches Stabilitäts-Programm (ESP)',
        'Fahrwerk tiefergelegt',
        'Garantie',
        'Halogenscheinwerfer',
        'Klimaanlage',
        'Kopfstützen hinten',
        'Licht- und Regensensor',
        'Motor Start-/Stop-Anlage',
        'Nebelscheinwerfer',
        'Rückfahrkamera',
        'Seitenairbags',
        'Sportfahrwerk',
        'Sportsitze vorne',
        'Spurassistent',
        'Spurhalteassistent',
        'Start-/Stop-Knopf',
        'Start/Stop-Funktion',
        'Stop/Start-System',
        'Tempomat',
        'Tuning',
        'Vordersitze heizbar',
        'Überrollschutzsystem',
        'Window-Kopfairbags',
        'Wegfahrsperre elektronisch',
        'Seitenairbag für Fahrer und Beifahrer',
        'Scheibenwischer vorne mit Intervall',
        'Reifendruck-Kontrollanzeige',
        'Pollenfilter (Staubfilter)',
        'Nebelschlussleuchte',
        'Laderaumabdeckung',
        'Knie-Airbag für Fahrer',
        'ISOFIX Kindersitzvorrichtung',
        'Heckscheibenheizung',
        'Heckscheiben-Wisch-/Waschanlage',
        'Getönte Scheiben',
        'Fahrersitz höhenverstellbar',
        'Beide Make up-Spiegel beleuchtet',
        'Aussentemperaturanzeige',
        'Antriebsschlupfregelung (ASR)',
        'Airbag Beifahrer deaktivierbar',
        'LED-Tagfahrlicht',
        'LED Heckleuchten',
        'Blinker in Aussenspiegel',
        'Aussenspiegel rechts und links beheizbar und elektrisch verstellbar',
        'Fahrersitz höhenverstellbar',
        'Zentralverriegelung mit Fernbedienung',
        'Wartungsintervall-Anzeige',
        'Vordersitze höhenverstellbar',
        'USB-Anschluss',
        'USB + AUX-Anschluss',
        'Stoff-Ausstattung',
        'Servolenkung',
        'Seitenaufprall-Schutzsystem',
        'Reifenreparatur-Set mit Kompressor',
        'Regensensor für Scheibenwischer vorne',
        'Partikelfilter und Oxydationskatalysator',
        'Multifunktionslenkrad',
        'Lenkrad längs- und höhenverstellbar',
        'Klimatisierungsautomatik',
        'Höhenverstellbare Gurten vorne',
        'Brillenfach',
        'Aussenspiegel rechts und links beheizt, elektrisch verstell- / und einklappbar',
        'Aussenspiegel rechts und links beheizt und elektrisch verstellbar, asphärisch gewölbtes Spiegelglas',
        'Aktive Kopfstützen',




    ]
    for val in df.columns.tolist():
        if val not in neworder:
           neworder.append(val)
    return df[neworder]

def show_frame():
    cars = pickle.load( open( "loaded_cars.pickle", "rb" ) )

    df = pd.DataFrame(cars)
    df = reorer_df(df)
    start = 0
    print(df[df.columns[start:start+20]])
    #for col in df.columns.tolist():
        #print(str(df[[col]].sum()))


#load_cars()
show_frame()
