import os
import tarfile
import glob
from math import isnan

import pandas as pd

from road_collisions_base import logger
from road_collisions_base.models.generic import GenericObjects
from road_collisions_base.models.raw_collision import RawCollision


class Collisions(GenericObjects):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('child_class', RawCollision)
        super().__init__(*args, **kwargs)

    @staticmethod
    def from_file(filepath):
        data = None

        ext = os.path.splitext(filepath)[-1]
        if ext == '.tgz' or ext == '.gz':
            tar = tarfile.open(filepath, "r:gz")
            tar.extractall(path=os.path.dirname(filepath))
            tar.close()

            data = []
            for sub_file in glob.iglob(os.path.dirname(filepath) + '/**', recursive=True):
                ext = os.path.splitext(sub_file)[-1]
                if ext == '.csv':
                    csv_data = pd.read_csv(
                        sub_file.replace('.csv.tgz', '.csv')
                    ).to_dict(orient='records')

                    data.extend(csv_data)

        else:
            raise Exception()

        collisions = Collisions()
        for collision_dict in data:
            obj = Collision.parse(
                collision_dict
            )

            # TODO: filter the object out here by whatever prop params
            # and save some mem

            collisions.append(obj)

        return collisions

    @staticmethod
    def from_dir(dirpath, region=None):
        collisions = Collisions()
        if region is None:
            search_dir = f'{dirpath}/**'
        else:
            search_dir = f'{dirpath}/{region}/**'

        for filename in glob.iglob(search_dir, recursive=True):
            if os.path.splitext(filename)[-1] not in {'.tgz', '.gz'}:
                continue
           
            collision = Collisions.from_file(
                filename
            )

            collisions.extend(
                collision
            )

        return collisions

    def filter(self, **kwargs):
        '''
        By whatever props that exist
        '''
        logger.debug('Filtering from %s' % (len(self)))

        filtered = [
            d for d in self if all(
                [
                    getattr(d, attr) == kwargs[attr] for attr in kwargs.keys()
                ]
            )
        ]

        return Collisions(
            data=filtered
        )

    @staticmethod
    def load_all():
        import road_collisions_anz
        return Collisions.from_dir(
            os.path.join(road_collisions_anz.__path__[0], 'resources'),
            region='anz'
        )


class Collision(RawCollision):

    __slots__ = [
        'DCA_code',
        'animals',
        'approximate',
        'bicycle',
        'bus',
        'car_4x4',
        'car_sedan',
        'car_station_wagon',
        'car_utility',
        'car_van',
        'casualties',
        'comment',
        'country',
        'crash_id',
        'crash_type',
        'day_of_month',
        'day_of_week',
        'description_id',
        'drugs_alcohol',
        'fatalities',
        'hour',
        'inanimate',
        'intersection',
        'latitude',
        'lighting',
        'local_government_area',
        'longitude',
        'midblock',
        'minor_injuries',
        'month',
        'motor_cycle',
        'pedestrian',
        'road_position_horizontal',
        'road_position_vertical',
        'road_sealed',
        'road_wet',
        'scooter',
        'serious_injuries',
        'severity',
        'speed_limit',
        'state',
        'statistical_area',
        'suburb',
        'taxi',
        'traffic_controls',
        'train',
        'tram',
        'truck_large',
        'truck_small',
        'vehicle_other',
        'weather',
        'year'
    ]

    def __init__(self, **kwargs):
        self.DCA_code = kwargs['DCA_code']
        self.animals = int(kwargs['animals']) if not isnan(kwargs['animals']) else None
        self.approximate = kwargs['approximate']
        self.bicycle = int(kwargs['bicycle']) if not isnan(kwargs['bicycle']) else None
        self.bus = int(kwargs['bus']) if not isnan(kwargs['bus']) else None
        self.car_4x4 = int(kwargs['car_4x4']) if not isnan(kwargs['car_4x4']) else None
        self.car_sedan = int(kwargs['car_sedan']) if not isnan(kwargs['car_sedan']) else None
        self.car_station_wagon = int(kwargs['car_station_wagon']) if not isnan(kwargs['car_station_wagon']) else None
        self.car_utility = int(kwargs['car_utility']) if not isnan(kwargs['car_utility']) else None
        self.car_van = int(kwargs['car_van']) if not isnan(kwargs['car_van']) else None
        self.casualties = int(kwargs['casualties']) if not isnan(kwargs['casualties']) else None
        self.comment = kwargs['comment']
        self.country = kwargs['country']
        self.crash_id = kwargs['crash_id']
        self.crash_type = kwargs['crash_type']
        self.day_of_month = kwargs['day_of_month']
        self.day_of_week = int(kwargs['day_of_week']) if not isnan(kwargs['day_of_week']) else None
        self.description_id = kwargs['description_id']
        self.drugs_alcohol = kwargs['drugs_alcohol']
        self.fatalities = int(kwargs['fatalities']) if not isnan(kwargs['fatalities']) else None
        self.hour = int(kwargs['hour']) if not isnan(kwargs['hour']) else None
        self.inanimate = int(kwargs['inanimate']) if not isnan(kwargs['inanimate']) else None
        self.intersection = kwargs['intersection']
        self.latitude = kwargs['latitude']
        self.lighting = kwargs['lighting']
        self.local_government_area = kwargs['local_government_area']
        self.longitude = kwargs['longitude']
        self.midblock = kwargs['midblock']
        self.minor_injuries = int(kwargs['minor_injuries']) if not isnan(kwargs['minor_injuries']) else None
        self.month = int(kwargs['month']) if not isnan(kwargs['month']) else None
        self.motor_cycle = int(kwargs['motor_cycle']) if not isnan(kwargs['motor_cycle']) else None
        self.pedestrian = int(kwargs['pedestrian']) if not isnan(kwargs['pedestrian']) else None
        self.road_position_horizontal = kwargs['road_position_horizontal']
        self.road_position_vertical = kwargs['road_position_vertical']
        self.road_sealed = kwargs['road_sealed']
        self.road_wet = kwargs['road_wet']
        self.scooter = int(kwargs['scooter']) if not isnan(kwargs['scooter']) else None
        self.serious_injuries = int(kwargs['serious_injuries']) if not isnan(kwargs['serious_injuries']) else None
        self.severity = kwargs['severity']
        self.speed_limit = kwargs['speed_limit']
        self.state = kwargs['state']
        self.statistical_area = kwargs['statistical_area']
        self.suburb = kwargs['suburb']
        self.taxi = int(kwargs['taxi']) if not isnan(kwargs['taxi']) else None
        self.traffic_controls = kwargs['traffic_controls']
        self.train = int(kwargs['train']) if not isnan(kwargs['train']) else None
        self.tram = int(kwargs['tram']) if not isnan(kwargs['tram']) else None
        self.truck_large = int(kwargs['truck_large']) if not isnan(kwargs['truck_large']) else None
        self.truck_small = int(kwargs['truck_small']) if not isnan(kwargs['truck_small']) else None
        self.vehicle_other = int(kwargs['vehicle_other']) if not isnan(kwargs['vehicle_other']) else None
        self.weather = kwargs['weather']
        self.year = kwargs['year']

    @staticmethod
    def parse(data):
        if isinstance(data, Collision):
            return data

        return Collision(
            **data
        )

    def serialize(self):
        return {
            'DCA_code': self.DCA_code,
            'animals': self.animals,
            'approximate': self.approximate,
            'bicycle': self.bicycle,
            'bus': self.bus,
            'car_4x4': self.car_4x4,
            'car_sedan': self.car_sedan,
            'car_station_wagon': self.car_station_wagon,
            'car_utility': self.car_utility,
            'car_van': self.car_van,
            'casualties': self.casualties,
            'comment': self.comment,
            'country': self.country,
            'crash_id': self.crash_id,
            'crash_type': self.crash_type,
            'day_of_month': self.day_of_month,
            'day_of_week': self.day_of_week,
            'description_id': self.description_id,
            'drugs_alcohol': self.drugs_alcohol,
            'fatalities': self.fatalities,
            'hour': self.hour,
            'inanimate': self.inanimate,
            'intersection': self.intersection,
            'latitude': self.latitude,
            'lighting': self.lighting,
            'local_government_area': self.local_government_area,
            'longitude': self.longitude,
            'midblock': self.midblock,
            'minor_injuries': self.minor_injuries,
            'month': self.month,
            'motor_cycle': self.motor_cycle,
            'pedestrian': self.pedestrian,
            'road_position_horizontal': self.road_position_horizontal,
            'road_position_vertical': self.road_position_vertical,
            'road_sealed': self.road_sealed,
            'road_wet': self.road_wet,
            'scooter': self.scooter,
            'serious_injuries': self.serious_injuries,
            'severity': self.severity,
            'speed_limit': self.speed_limit,
            'state': self.state,
            'statistical_area': self.statistical_area,
            'suburb': self.suburb,
            'taxi': self.taxi,
            'traffic_controls': self.traffic_controls,
            'train': self.train,
            'tram': self.tram,
            'truck_large': self.truck_large,
            'truck_small': self.truck_small,
            'vehicle_other': self.vehicle_other,
            'weather': self.weather,
            'year': self.year
        }
