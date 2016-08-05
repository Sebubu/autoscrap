from unittest import TestCase
import CarScrapper as cs
import pickle


def read_car_list():
    car_list = pickle.load(open("car.pickle","rb"))
    cars = []
    for obj in car_list:
        car = cs.Car.by_serializable_obj(obj)
        cars.append(car)
    return cars


class CarScrapperTest(TestCase):
    links_per_site = 20

    def test_vehid_list(self):
        links = cs.vehid_list(1)
        self.assertEqual(len(links), self.links_per_site)

    def test_huge_vehid_list(self):
        links = cs.huge_vehid_list(1, 2)
        self.assertEqual(len(links), 2 * self.links_per_site)

    def test_car_load(self):
        vehid = "4170512"
        car = cs.Car(vehid)
        self.assertIsNotNone(car.soup)

    def test_car_vehicle_details(self):
        car = read_car_list()[0]
        self.assertIsNotNone(car.vehicle_details)

    def test_car_fahrzeugdaten(self):
        car = read_car_list()[0]
        self.assertIsNotNone(car.fahrzeugdaten)
        self.assertEqual(len(car.fahrzeugdaten), 23)

    def test_car_ausstattung(self):
        car = read_car_list()[0]
        self.assertIsNotNone(car.ausstattung)

    def test_car_serienausstattung_None(self):
        vehid = "4109894"
        car = cs.Car(vehid)
        self.assertIsNone(car.serien_ausstattung)

    def test_car_serienausstattung(self):
        car = read_car_list()[0]
        self.assertIsNotNone(car.serien_ausstattung)
        self.assertEqual(len(car.serien_ausstattung), 40)

    def test_car_titel(self):
        car = read_car_list()[0]
        self.assertEqual(car.titel, "FIAT Panda 1.3 MJ Climbing 4x4")

    def test_car_class(self):
        car = read_car_list()[0]
        self.assertEqual(car.car_class, "Kleinwagen")

    def test_car_data_dict(self):
        car = read_car_list()[0]
        self.assertIsNotNone(car.data_dict)
        print(car.data_dict)


class CarDictTest(TestCase):

    def test_print_dict(self):
        cars = read_car_list()
        for car in cars:
            cardict = cs.CarDict(car)
            print(cardict.as_dict())


    def test_anhangelast_geb(self):
        cars = read_car_list()
        for car in cars:
            cardict = cs.CarDict(car)
            last = cardict.anhangelast_geb()
            if last is not None:
                self.assertTrue(str(last).isdigit())

    def test_ab_mfk(self):
        cars = read_car_list()
        for car in cars:
            cardict = cs.CarDict(car)
            last = cardict.ab_mfk()
            self.assertTrue(str(last).isdigit())

    def test_hubraum(self):
        cars = read_car_list()
        for car in cars:
            cardict = cs.CarDict(car)
            last = cardict.hubraum()
            if last is not None:
                self.assertTrue(str(last).isdigit())

    def test_c02emission(self):
        cars = read_car_list()
        for car in cars:
            cardict = cs.CarDict(car)
            last = cardict.co2emission()
            if last is not None:
                self.assertTrue(str(last).isdigit())

    def test_kilometer(self):
        cars = read_car_list()
        for car in cars:
            cardict = cs.CarDict(car)
            last = cardict.kilometer()
            if last is not None:
                self.assertTrue(str(last).isdigit())

    def test_leergewicht(self):
        cars = read_car_list()
        for car in cars:
            cardict = cs.CarDict(car)
            last = cardict.leergewicht()
            if last is not None:
                self.assertTrue(str(last).isdigit())

    def test_verbauch(self):
        cars = read_car_list()
        for car in cars:
            cardict = cs.CarDict(car)
            last = cardict.verbrauch()
            if last is not None:
                self.assertEqual(len(last), 3)

    def test_preis(self):
        cars = read_car_list()
        for car in cars:
            cardict = cs.CarDict(car)
            last = cardict.preis()
            if last is not None:
                print(last)
                self.assertTrue(str(last).isdigit())


class HugeInternetTest(TestCase):

    def big_serialize(self):
        car_list = []
        ids = cs.huge_vehid_list(1, 1)
        for ident in ids:
            car = cs.Car(ident)
            car_list.append(car.serializable_obj())

        pickle.dump(car_list, open("car.pickle", "wb"))



    def test_one_page(self):
        ids = cs.huge_vehid_list(1,1)

        for ident in ids:
            car = cs.Car(ident)
            print(car.car_class + ": " + car.titel)
            self.assertIsNotNone(car.fahrzeugdaten)


