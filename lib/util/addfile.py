#!/usr/bin/env python3
import os

os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'packrat.settings' )

import django
django.setup()

import sys
import types
from optparse import OptionParser
from django.core.files import File
from packrat.Package.models import PackageFile

oparser = OptionParser( description='Add Package File', usage="Usage: %prog [options] file" )

oparser.add_option( '-l', '--list-distroversions', default=False, action='store_true' )

oparser.add_option( '-d', '--distroversion', help='Set the distroversion, needed when packrat is unable to auto-detect the distroversion (optional)', default=None )
oparser.add_option( '-j', '--justification', help='Justification for the package file', default=None )
oparser.add_option( '-p', '--provenance', help='Provenance for the package file', default=None )
oparser.add_option( '-t', '--type', help='Specify the type of the file, ie: deb, respkg, ova, etc..., if not specified packrat will auto-detect it(optional)', default=None )

( options, args ) = oparser.parse_args()

try:
  filepath = args[0]

except IndexError:
  print( 'file required' )
  oparser.print_help()
  sys.exit( 1 )

if not os.path.exists( filepath ):
  print( 'file "{0}" not found'.format( filepath ) )
  sys.exit( 1 )

file = File( open( filepath, 'rb' ), os.path.basename( filepath ) )

if options.list_distroversions:
  item_list = PackageFile.distroversionOptions( file, options.type )
  print( 'Distro List' )
  for item in item_list:
    print( item )

  sys.exit( 0 )

if not options.justification or not options.provenance:
  print( 'Justification and Provenance are required' )
  oparser.print_help()
  sys.exit( 1 )

if options.distroversion is None:
  item_list = PackageFile.distroversionOptions( file, options.type )
  if len( item_list ) == 1:
    distro_version = item_list[0]

  else:
    print( 'Multiple distro versions detected.  One of the following must be specified' )
    for item in item_list:
      print( item )

    sys.exit( 1 )

else:
  distro_version = options.distroversion

user = types.SimpleNamespace()
user.username = 'cli'

PackageFile.create( user, file, options.justification, options.provenance, distro_version, options.type )
print( 'done' )
