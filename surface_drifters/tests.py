# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase
from django.core.management import call_command
from django.utils.six import StringIO
from geospaas.catalog.models import Dataset


class TestCommand(TestCase):
    fixtures = ['vocabularies', 'platforms']

    def setUp(self):
        self.test_csv = '/vagrant/shared/FRUHOLME_HFR_S1AB_IW_VV_' \
                        'NEW_PRODUCT/data/drifters/lofoten/iSLDMB_12.csv'

        call_command('ingest_surface_drifters',
                     self.test_csv,
                     extent=[0, 360, 0, 90],
                     start='2016-05-01',
                     end='2016-05-02')

    def test_dataset(self):
        ds = Dataset.objects.filter(source__platform__short_name='iSLDMB')
        self.assertEqual(len(ds), 49)
        self.assertEqual(ds.first().dataseturi_set.first().uri,
                         'file://localhost/vagrant/shared/FRUHOLME_HFR_S1AB_IW_VV_NEW'
                         '_PRODUCT/data/drifters/lofoten/iSLDMB_12.csv')

