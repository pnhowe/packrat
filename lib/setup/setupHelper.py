#!/usr/bin/env python3
import os

if __name__ == '__main__':
  os.environ.setdefault( 'DJANGO_SETTINGS_MODULE', 'packrat.settings' )

  import django
  django.setup()

from django.contrib.auth.models import User, Permission
from packrat.Repo.models import Repo, Mirror
from packrat.Attrib.models import DistroVersion, Tag
from packrat.lib.info import OTHER_TYPE_LIST


def load_tags():
  tag_list = [ ( 'dev', [], False ), ( 'stage', [ 'dev' ], False ), ( 'prod', [ 'stage' ], True ) ]

  for name, required_list, cc in tag_list:
    t = Tag( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', name=name, change_control_required=cc )
    t.full_clean()
    t.save()
    for required in required_list:
      t.required_list.add( Tag.objects.get( name=required ) )


def load_users():
  User.objects.create_superuser( username='root', email='root@none.com', password='root' )

  u = User.objects.create_user( 'mcp', password='mcp' )
  for name in ( 'can_tag', 'can_fail', 'tag_dev', 'tag_stage', 'delete_packagefile' ):
    u.user_permissions.add( Permission.objects.get( codename=name ) )

  u = User.objects.create_user( 'nullunit', password='nullunit' )
  for name in ( 'add_packagefile', ):
    u.user_permissions.add( Permission.objects.get( codename=name ) )

  u = User.objects.create_user( 'manager', password='manager' )
  for name in ( 'can_tag', 'can_untag', 'can_fail', 'can_unfail', 'can_deprocate', 'can_undeprocate', 'add_package', 'add_packagefile', 'tag_dev', 'tag_stage', 'tag_prod' ):
    u.user_permissions.add( Permission.objects.get( codename=name ) )

  User.objects.create_user( 'mirror', password='mirrormirror' )


def load_distro_versions():
  for version in ( 'trusty', 'xenial', 'bionic' ):
    d = DistroVersion( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', name=version, file_type='deb', version=version, release_names=version, distro='debian' )
    d.full_clean()
    d.save()

  for version, release_name, name in ( ( '6', 'el6	centos6', 'rhel6' ), ( '7', 'el7	centos7', 'rhel7' ), ( '8', 'el8	centos8', 'rhel8' ) ):
    d = DistroVersion( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', name=name, file_type='rpm', version=version, release_names=release_name, distro='rhel' )
    d.full_clean()
    d.save()

  for version, name in ( ( 'sles11', '11' ), ( 'sles12', '12' ) ):
    d = DistroVersion( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', name=version, file_type='rpm', version=version, release_names=name, distro='sles' )
    d.full_clean()
    d.save()

  d = DistroVersion( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', name='docker', file_type='docker', distro='none' )
  d.full_clean()
  d.save()

  d = DistroVersion( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', name='pypi', file_type='python', distro='none' )
  d.full_clean()
  d.save()

  for type in list( OTHER_TYPE_LIST ) + [ 'resource', 'ova', 'respkg' ]:
    d = DistroVersion( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', name=type, file_type=type, distro='none' )
    d.full_clean()
    d.save()


def load_repos():
  release_list = ( ( 'dev', 'dev' ), ( 'stage', 'stage' ), ( 'prod', 'prod' ) )

  for release, tag in release_list:
    r = Repo( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', description='APT - {0}'.format( release.title() ), manager_type='apt', name='apt-{0}'.format( release ), filesystem_dir='apt-{0}'.format( release ) )
    r.tag_id = tag
    r.full_clean()
    r.save()
    r.distroversion_list = [ 'trusty', 'xenial', 'bionic' ]

  for release, tag in release_list:
    r = Repo( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', description='YUM - {0}'.format( release.title() ), manager_type='yum', name='yum-{0}'.format( release ), filesystem_dir='yum-{0}'.format( release ) )
    r.tag_id = tag
    r.full_clean()
    r.save()
    r.distroversion_list = [ 'rhel6', 'rhel7', 'rhel8', 'sles11', 'sles12' ]

  for release, tag in release_list:
    r = Repo( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', description='Docker - {0}'.format( release.title() ), manager_type='docker', name='docker-{0}'.format( release ), filesystem_dir='docker-{0}'.format( release ), show_only_latest=False )
    r.tag_id = tag
    r.full_clean()
    r.save()
    r.distroversion_list = [ 'docker' ]

  for release, tag in release_list:
    r = Repo( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', description='PYPI - {0}'.format( release.title() ), manager_type='pypi', name='pypi-{0}'.format( release ), filesystem_dir='pypi-{0}'.format( release ), show_only_latest=False )
    r.tag_id = tag
    r.full_clean()
    r.save()
    r.distroversion_list = [ 'pypi' ]

  for release, tag in release_list:
    r = Repo( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', description='JSON - {0}'.format( release.title() ), manager_type='json', name='json-{0}'.format( release ), filesystem_dir='json-{0}'.format( release ), show_only_latest=False )
    r.tag_id = tag
    r.full_clean()
    r.save()
    r.distroversion_list = list( OTHER_TYPE_LIST ) + [ 'resource', 'ova', 'respkg' ]


def load_mirrors():
  m = Mirror( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', name='prod', description='Production' )
  m.full_clean()
  m.save()
  repo_list = []
  for release in ( 'prod', ):
    for item in ( 'apt', 'yum', 'json', 'docker', 'pypi' ):
      repo_list.append( '{0}-{1}'.format( item, release ) )
  m.repo_list = repo_list

  m = Mirror( updated='2010-01-01T00:00:00.000Z', created='2010-01-01T00:00:00.000Z', name='lab', description='Lab' )
  m.full_clean()
  m.save()
  repo_list = []
  for release in ( 'stage', 'dev' ):
    for item in ( 'apt', 'yum', 'json', 'docker', 'pypi' ):
      repo_list.append( '{0}-{1}'.format( item, release ) )
  m.repo_list = repo_list


def load():
  print( 'Creating Tags...' )
  load_tags()

  print( 'Creating Users...' )
  load_users()

  print( 'Creating Distro Versions...' )
  load_distro_versions()

  print( 'Creating Repos...' )
  load_repos()

  print( 'Creating Mirrors...' )
  load_mirrors()


if __name__ == '__main__':
  load()
