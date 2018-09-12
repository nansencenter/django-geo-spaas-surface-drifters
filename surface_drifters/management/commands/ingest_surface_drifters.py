from geospaas.utils import ProcessingBaseCommand
from geospaas.utils import uris_from_args
from surface_drifters.models import DrifterDataset
from datetime import datetime

class Command(ProcessingBaseCommand):

    def add_arguments(self, parser):
        # Inherit standard arguments
        super(Command, self).add_arguments(parser)
        # Input files
        parser.add_argument('i_files', nargs='*', type=str)

    def handle(self, *agrs, **options):
        options['start'] = datetime.strptime(options['start'], '%Y-%m-%d')
        options['end'] = datetime.strptime(options['end'], '%Y-%m-%d')
        geometry = self.geometry_from_options(extent=options['extent'], geojson=options['geojson'])
        for non_ingested_uri in uris_from_args(options['i_files']):
            ds = DrifterDataset.objects.get_or_create(non_ingested_uri, geometry, **options)
