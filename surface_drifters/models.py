# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from geospaas.catalog.models import Dataset as CatalogDataset
from surface_drifters.management import DrifterDatasetManager


class DrifterDataset(CatalogDataset):

    objects = DrifterDatasetManager()

    class Meta:
        proxy = True
