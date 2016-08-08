import pandas as pd
import CarScrapper as cs
import pickle
import matplotlib.pyplot as plt

from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.metrics import r2_score


def load_cars():
    print("Load cars")
    for i in range(20,40):
        cars = cs.car_dicts(i, i)
        pickle.dump(cars, open("car_depot/page" + str(i) + ".pickle", "wb"))

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
        #'Einparkhilfe',
        'Elektrische Fensterheber hinten',
        'Elektrische Fensterheber vorne',
        'Elektrische Fensterheber vorne + hinten',
        'Elektrische Heckklappe',
        'Elektronisches Stabilitäts-Programm (ESP)',
        #'Fahrwerk tiefergelegt',
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


def get_main_df():
    cars = []
    for i in range(1,40):
        cars_page = pickle.load(open("car_depot/page" + str(i) + ".pickle", "rb"))
        cars += cars_page

    df = pd.DataFrame(cars)
    df = reorer_df(df)
    df.columns = [c.replace(' ', '_') for c in df.columns]
    return df

def ps_preis(column):
    df = get_main_df()
    df['Inverkehrsetzung'] = pd.to_datetime(df['Inverkehrsetzung'])
    df = df[(df.Inverkehrsetzung.dt.year > 2000) & (df.Inverkehrsetzung.dt.year < 2015)]
    df = df.sample(frac=1).reset_index(drop=True)

    rdf = df[[column, 'Preis(chf)', 'vehid']].dropna().apply(pd.to_numeric)

    test_count = 100
    train = rdf[:-test_count]
    test = rdf[-test_count:]
    test = test.sort(column, ascending=True)
    #test = test[(test.Leistung_in_PS < 450)]
    #Remove outliers
    #train = train[train.apply(lambda x: np.abs(x - x.mean()) / x.std() < 2.5).all(axis=1)]
    #test = test[test.apply(lambda x: np.abs(x - x.mean()) / x.std() < 2.5).all(axis=1)]


    x_columns = [column]
    y_columns = ['Preis(chf)']


    x_train = train[x_columns]
    y_train = train[y_columns]
    x_test = test[x_columns]
    y_test = test[y_columns]



    plt.scatter(x_test, y_test, color='black')
    # Plot outputs
    colors = [
        "green",
        "brown",
        "violet",
        "blue",
        "red",
        "black",
        "orange",
        'yellow',
              ]
    start = 7
    for degree in range(start,8):
        color = colors[degree - start]
        regr = make_pipeline(PolynomialFeatures(degree), Ridge())
        regr.fit(x_train, y_train)

        plt.plot(x_test, regr.predict(x_test), color=color,
             linewidth=1, label="degree " + str(degree))

    plt.legend()
    plt.xlabel(column, fontsize=16)
    plt.ylabel('Price (CHF)', fontsize=16)
    plt.show()


def to_dummy_var(df, column):
    dummies = pd.get_dummies(df[column], prefix=column)
    df = df.join(dummies)
    df = df.drop(column, 1)
    return df

def get_good_columns():
    df = get_main_df()
    df['Inverkehrsetzung'] = pd.to_datetime(df['Inverkehrsetzung'])
    df = df[(df.Inverkehrsetzung.dt.year > 1990) & (df.Inverkehrsetzung.dt.year < 2016)]
    #df = df.sample(frac=1).reset_index(drop=True)
    df = df[['vehid',
        #'titel',
        'Leistung_in_PS',
        'Preis(chf)',
        'Anhangelast(kg)',
        'Antriebsart',
        'Aussenfarbe',
        'Energieeffizienz',
        'Euro_Norm',
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
        'verbrauch_total',]]

    df = to_dummy_var(df, "Antriebsart")
    df = to_dummy_var(df, "Aussenfarbe")
    df = to_dummy_var(df, "Fahrzeugart")
    df = to_dummy_var(df, "Getriebeart")
    df = to_dummy_var(df, "Treibstoff")
    df = to_dummy_var(df, "klasse")
    df = to_dummy_var(df, "marke")
    df = to_dummy_var(df, "Energieeffizienz")
    df = to_dummy_var(df, "Euro_Norm")
    df['inverkehrsetzung_jahr'] = pd.DatetimeIndex(df['Inverkehrsetzung']).year
    df.drop("Inverkehrsetzung",1)

    df = df.apply(pd.to_numeric)
    df = df.fillna(0)

    X = df.drop("Preis(chf)",1)
    Y = df[["Preis(chf)"]]

    return df, ['vehid', 'Leistung_in_PS', 'Anhangelast(kg)', 'Hubraum(ccm2)', 'Inverkehrsetzung', 'Kilometer', 'Leergewicht(kg)', 'Neupreis(chf)', 'Sitze', 'Türen', 'Zylinder', 'co2emission(g/km)', 'mfk', 'verbrauch_land', 'verbrauch_stadt', 'verbrauch_total', 'Antriebsart_Allrad', 'Antriebsart_Hinterradantrieb', 'Antriebsart_Vorderradantrieb', 'Aussenfarbe_blau mét.', 'Aussenfarbe_grau mét.', 'Aussenfarbe_grün mét.', 'Aussenfarbe_rot', 'Aussenfarbe_schwarz', 'Aussenfarbe_schwarz mét.', 'Aussenfarbe_silber mét.', 'Aussenfarbe_weiss', 'Fahrzeugart_Occasion', 'Getriebeart_Automat', 'Getriebeart_Automat sequentiell', 'Getriebeart_Automatisiertes Schaltgetriebe', 'Getriebeart_Schaltgetriebe', 'Getriebeart_Schaltgetriebe manuell', 'Treibstoff_Benzin', 'Treibstoff_Diesel', 'klasse_Cabriolet', 'klasse_Coupé', 'klasse_Kombi', 'klasse_Limousine', 'klasse_SUV / Geländewagen', 'marke_AC', 'marke_AUDI', 'marke_BENTLEY', 'marke_BMW', 'marke_FERRARI', 'marke_LAND', 'marke_MERCEDES-BENZ', 'marke_OPEL', 'marke_PORSCHE', 'Energieeffizienz_D', 'Energieeffizienz_E', 'Energieeffizienz_F', 'Energieeffizienz_G', 'Euro_Norm_Euro 1', 'Euro_Norm_Euro 4', 'Euro_Norm_Euro 5', 'Euro_Norm_Euro 6', 'inverkehrsetzung_jahr']
    model = RandomForestRegressor(n_estimators=200)
    from sklearn.feature_selection import RFE
    # create the RFE model and select 3 attributes
    rfe = RFE(model, 30)
    rfe = rfe.fit(X, Y)
    # summarize the selection of the attributes

    good_columns = []
    i=0
    for col in X.columns:
        rank = rfe.ranking_[i]
        if rank < 30:
            good_columns.append(col)
            print(col + ": " + str(rank))
        i+=1
    return df, good_columns

def all_preis(df, good_columns):

    column = 'Neupreis(chf)'

    test_count = 100
    train = df[:-test_count]
    test = df[-test_count:]
    test = test.sort(column, ascending=True)

    #Remove outliers
    #train = train[train.apply(lambda x: np.abs(x - x.mean()) / x.std() < 2.5).all(axis=1)]
    #test = test[test.apply(lambda x: np.abs(x - x.mean()) / x.std() < 2.5).all(axis=1)]


    x_columns = good_columns
    y_columns = ['Preis(chf)']


    x_train = train[x_columns]
    y_train = train[y_columns]
    x_test = test[x_columns]
    y_test = test[y_columns]



    plt.scatter(x_test[[column]], y_test, color='black')
    # Plot outputs
    colors = [
        "green",
        "brown",
        "violet",
        "blue",
        "red",
        "black",
        "orange",
        'yellow',
              ]
    from sklearn import cross_validation

    regr = RandomForestRegressor(n_estimators=200, max_features="sqrt")
    regr.fit(x_train, y_train)
    prediction = regr.predict(x_test)
    print(str(r2_score(y_test, prediction)))

    for i in range(0, len(prediction)):
        print(str(float(y_test.iloc[i])) + " - " + str(float(prediction[i])))
        difference = float(y_test.iloc[i]) - float(prediction[i])
        vehid = int(x_test[['vehid']].iloc[i])
        if difference < -6000:
            print(str(difference) + ": " + str(vehid))
        print()
    print()
    '''
    plt.plot(x_test[[column]], regr.predict(x_test), linewidth=1)

    plt.legend()
    plt.xlabel('PS', fontsize=16)
    plt.ylabel('Price (CHF)', fontsize=16)
    plt.show()
    '''


['vehid',
        #'titel',
        'Leistung_in_PS',
        'Preis(chf)',
        'Anhangelast(kg)',
        'Antriebsart',
        'Aussenfarbe',
        'Energieeffizienz',
        'Euro_Norm',
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
        'verbrauch_total',]

#load_cars()
ps_preis('marke_VW')
#df, good_columns = get_good_columns()
#all_preis(df, good_columns)
