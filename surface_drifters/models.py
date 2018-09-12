# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from geospaas.catalog.models import Dataset as CatalogDataset
from surface_drifters.managers import DrifterDatasetManager


class DrifterDataset(CatalogDataset):

    objects = DrifterDatasetManager()

    class Meta:
        proxy = True
