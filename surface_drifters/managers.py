from django.db import models
from django.contrib.gis.geos import Point, Polygon

from geospaas.catalog.models import Dataset, Source, DatasetURI, GeographicLocation
from geospaas.vocabularies.models import Platform, Instrument, DataCenter, ISOTopicCategory
from geospaas.utils.utils import nansat_filename

import pandas as pd
from datetime import datetime
import pytz


class DrifterDatasetManager(models.Manager):

    CHUNK_SIZE = 1  # every single measurement will be ingested separately
    TIMEZONE = pytz.timezone('UTC')

    @staticmethod
    def set_metadata():
        # The platform and instrument metadata are not in the metadata
        # Thus we will have to set it manually
        platform = Platform.objects.get_by_natural_key(short_name='iSLDMB')
        instrument = Instrument.objects.get(short_name='DRIFTING BUOYS')
        src = Source.objects.get_or_create(platform=platform,
                                           instrument=instrument)[0]
        dc = DataCenter.objects.get(short_name='NO/MET')
        iso = ISOTopicCategory.objects.get(name='Oceans')
        return dc, iso, src

    def get_or_create(self, uri, geometry, *args, **kwargs):
        filename = nansat_filename(uri)
        data = pd.read_csv(filename, header=0)
        data_center, iso, source = self.set_metadata()

        for i in range(len(data)):
            # Check if a buoy location is inside of a geometry (domain)
            buoy_location = Point(data[' LONGITUDE'][i], data[' LATITUDE'][i])
            # TODO: All <continue> should appear in/affect an output
            if isinstance(geometry, Polygon):
                if not geometry.contains(buoy_location):
                    continue
            else:
                continue

            buoy_time = datetime.strptime(data['Data Date (UTC)'][i], '%Y-%m-%d %H:%M:%S')
            if kwargs['end'] < buoy_time or kwargs['start'] > buoy_time:
                continue

            buoy_time = self.TIMEZONE.localize(buoy_time)
            geoloc, geo_cr = GeographicLocation.objects.get_or_create(geometry=buoy_location)
            ds, ds_cr = Dataset.objects.get_or_create(
                entry_title='Lofoten experiment 2016 ',
                ISO_topic_category=iso,
                data_center=data_center,
                summary='',
                time_coverage_start=buoy_time,
                time_coverage_end=buoy_time,
                source=source,
                geographic_location=geoloc)

            if ds_cr:
                data_uri, duc = DatasetURI.objects.get_or_create(uri=uri, dataset=ds)
