#!/usr/bin/env python3
import os

os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'packrat.settings' )

import django
django.setup()

from django.conf import settings
from packrat.Package.models import Package, PackageFile

# clean up deprocated files
for package in Package.objects.all():
  deprocated_list = list( package.packagefile_set.all().filter( deprocated_at__isnull=False ).order_by( 'deprocated_at' ) )
  while len( deprocated_list ) > package.deprocated_count:
    package_file = deprocated_list.pop( 0 )
    print( 'Deleting Deprocated "{0}"...'.format( package_file ) )
    package_file.delete()

  failed_list = list( package.packagefile_set.all().filter( failed_at__isnull=False ).order_by( 'failed_at' ) )
  while len( failed_list ) > package.failed_count:
    package_file = failed_list.pop( 0 )
    print( 'Deleting Failed "{0}"...'.format( package_file ) )
    package_file.delete()

# clean up files that are not refrenced
good_list = [ i[0][2:] for i in PackageFile.objects.all().values_list( 'file' ) ]  # take off the ./

for filename in os.listdir( settings.MEDIA_ROOT ):
  if filename not in good_list:
    print( 'Removing "{0}"...'.format( filename ) )
    os.unlink( os.path.join( settings.MEDIA_ROOT, filename ) )
