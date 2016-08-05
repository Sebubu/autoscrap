from bs4 import BeautifulSoup
import urllib.request as urllib
from urllib.request import Request
from cached_property import cached_property
import datetime
main_address ="http://www.autoscout24.ch"

headers = {'User-Agent': 'Mozilla/5.0'}

def vehid_list(page):
    result = []
    autoscout = 'http://www.autoscout24.ch/de/autos/alle-marken?page=' + str(page) + '&st=1&vehtyp=10'
    r = urllib.urlopen(Request(autoscout, headers=headers)).read()
    soup = BeautifulSoup(r, "html.parser")
    liste = soup.find(id='list')
    elements = liste.find_all('li')
    for element in elements:
        div = element.find(class_='object-data')
        if div is None:
            continue
        title = div.find(class_="title-tertiary")
        href = title.find(class_="primary-link")
        part_link = href['href']
        vehid_str = part_link.split('&')[3]
        vehid = vehid_str.split("=")[1]
        result.append(vehid)
    return result

def huge_vehid_list(start_page, end_page):
    res = []
    for i in range(start_page, end_page + 1):
        res += vehid_list(i)
    return res


class Car:
    def __init__(self, vehid):
        self._vehid = vehid
        self._link = main_address + "/" + str(vehid)
        self._soup = None

    def serializable_obj(self):
        return (self._vehid, str(self.soup))



    @classmethod
    def by_serializable_obj(cls, obj):
        vehid, soup = obj
        car = cls(vehid)
        car._soup = BeautifulSoup(soup, "html.parser")
        return car

    @property
    def link(self):
        return self._link

    @property
    def soup(self):
        if self._soup is not None:
            return self._soup
        else:
            r = urllib.urlopen(Request(self.link, headers=headers)).read()
            self._soup = BeautifulSoup(r, "html.parser")
            return self._soup

    @property
    def vehicle_details(self):
        return self.soup.find(class_='vehicle-details')

    @cached_property
    def fahrzeugdaten(self):
        res_dict = {}
        list = self.vehicle_details.find(class_="textlist-list")
        for item in list.find_all("li"):
            formated_key = item.find(class_="prop").text
            formated_key = str(formated_key).replace("\r\n", "")
            key = str(formated_key).strip()

            formated_value = item.find(class_="value").contents[0]
            value = str(formated_value).strip()

            if key == "Preis":
                v = item.find(class_="value")
                value = v.find('strong').contents[0]

            res_dict[key] = value
        return res_dict

    @property
    def ausstattung(self):
        equipment = self.soup.find(id="equipment")
        if(equipment is None):
            return None
        data_url = main_address + equipment['data-url']
        r = urllib.urlopen(Request(data_url, headers=headers)).read()
        soup = BeautifulSoup(r, "html.parser")

        equipmentBoxUngrouped = soup.find(id="equipmentBoxUngrouped")
        return equipmentBoxUngrouped

    @cached_property
    def serien_ausstattung(self):
        ausstattung = self.ausstattung
        if ausstattung is None:
            return None
        result = []
        liste = ausstattung.find(id="detailTextEquipmentStandard")
        if liste is None:
            return None
        bullets = liste.find_all("li")

        for bullet in bullets:
            result.append(bullet.text.strip())
        return result

    @property
    def titel(self):
        main = self.soup.find(class_="title-main")
        titel = main.contents[0]
        return titel.strip()

    @property
    def marke(self):
        return self.titel.split(" ")[0]

    @property
    def car_class(self):
        main = self.soup.find(class_="title-main")
        klass = main.find("span")
        return klass.text.strip().replace("(", "").replace(")", "")

    @property
    def data_dict(self):
        dict = {'vehid': self._vehid,
                'titel': self.titel,
                'marke': self.marke,
                'klasse': self.car_class,
                }
        for key, value in self.fahrzeugdaten.items():
            dict[key] = value

        ausstattung = self.serien_ausstattung
        if ausstattung is not None:
            for key in ausstattung:
                dict[key] = 1


        return dict


class CarDict:
    def __init__(self, car):
        self.car = car
        self._plain_dict = car.data_dict

    def as_dict(self):
        self.anhangelast_geb()
        self.inverkehrsetzung()
        self.ab_mfk()
        self.hubraum()
        self.co2emission()
        self.kilometer()
        self.leergewicht()
        self.verbrauch_land()
        self.verbrauch_stadt()
        self.verbrauch_total()
        self.preis()
        self.neupreis()
        if 'Verbrauch in l/100 km' in self._plain_dict:
            del self._plain_dict['Verbrauch in l/100 km']
        return self._plain_dict


    def _plain_value(self, key):
        for dkey, value in self._plain_dict.items():
            if dkey == key:
                return value
        return None

    def _einheit(self, key):
        value = self._plain_value(key)
        if value is None:
            return None
        value = value.split(" ")[0]
        value = value.replace("'", "")
        return value

    def replace(self, key, newvalue, newkey):
        if key in self._plain_dict:
            del self._plain_dict[key]
        self._plain_dict[newkey] = newvalue

    def anhangelast_geb(self):
        key = 'Anhängelast geb.'
        value = self._einheit(key)
        self.replace(key,value, "Anhangelast(kg)")
        return value

    def inverkehrsetzung(self):
        key = 'Inverkehrsetzung'
        value = self._plain_value(key)
        if value is None:
            return None
        if value == "Neu":
            value = datetime.date.today().strftime('01.%m.%Y')
        else:
            value = "01." + value
        self.replace(key,value, key)
        return value

    def ab_mfk(self):
        key = 'Ab MFK'
        value = self._plain_value(key)
        if value is None:
            value = 0
        if value == 'Ja':
            value = 1
        self.replace(key,value, "mfk")
        return value

    def hubraum(self):
        key = 'Hubraum'
        value = self._einheit(key)
        self.replace(key,value, "Hubraum(ccm2)")
        return value

    def co2emission(self):
        key = 'CO2-Emission'
        value = self._einheit(key)
        self.replace(key,value, "co2emission(g/km)")
        return value

    def kilometer(self):
        key = 'Kilometer'
        value = self._einheit(key)
        self.replace(key,value, "Kilometer")
        return value

    def leergewicht(self):
        key = 'Leergewicht'
        value = self._einheit(key)
        self.replace(key,value, "Leergewicht(kg)")
        return value

    def verbrauch(self):
        key = 'Verbrauch in l/100 km'
        value = self._plain_value(key)
        if value is None:
            return None
        value = value.split(" ")[0]
        return value.split("/")

    def verbrauch_stadt(self):
        verbrauch = self.verbrauch()
        if verbrauch is None:
            return None
        value = verbrauch[0]
        if value == ".0":
            return None
        self._plain_dict["verbrauch_stadt"] = value
        return value

    def verbrauch_land(self):
        verbrauch = self.verbrauch()
        if verbrauch is None:
            return None
        value = verbrauch[1]
        if value == ".0":
            return None
        self._plain_dict["verbrauch_land"] = value
        return value

    def verbrauch_total(self):
        verbrauch = self.verbrauch()
        if verbrauch is None:
            return None
        value = verbrauch[0]
        if value == ".0":
            return None
        self._plain_dict["verbrauch_total"] = value
        return value

    def preis(self):
        key = 'Preis'
        value = self._plain_value(key)
        if value is None:
            return None
        value = value.split(" ")[1]
        value = value.replace("'", "")
        value = value.replace(".", "")
        value = value.replace("-", "")
        self.replace(key, value, "Preis(chf)")
        return value

    def neupreis(self):
        key = 'Neupreis'
        value = self._plain_value(key)
        if value is None:
            return None
        value = value.split(" ")[1]
        value = value.replace("'", "")
        value = value.replace(".", "")
        value = value.replace("-", "")
        self.replace(key, value, "Neupreis(chf)")
        return value

def car_dicts(start_page, end_page):
    dicts = []
    ids = huge_vehid_list(start_page, end_page)
    count = len(ids)
    i = 0
    last_percentage = 0
    for ident in ids:
        car = Car(ident)
        dict = CarDict(car).as_dict()
        dicts.append(dict)
        i+=1
        percentage =  (float(i)/count) * 100
        if last_percentage + 9.9 < percentage:
            print(str(int(percentage)) + "%")
            last_percentage = percentage
    return dicts