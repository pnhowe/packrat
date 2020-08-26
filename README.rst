Packrat
=============================

Packrat is an HTTP/JSON service the manages the life cycle of packages.
A package file (package file is a Packrat term for an individual package for example,
.deb, .rpm, .img, container, binary blob, etc.), can be tagged with customizable tags,
such as testing, staging, production, legal, security, etc.  These tags can be
configured to require that the package file be tagged with other tags before the tag
can be added, for example, the production tag can require staging, security, and
legal.   Tags can also require an id from a Change Ticket.   A planned enhancement
is to have packrat verify the Change Ticket is valid and for the right package.
A Repo in Packrat is a view of the Package Files of a specified type and a specific
tag applied, for exmaple, you can create a repo called "apt-stage" which will
expose all deb type files that have the stage tag.

Packrat is simply a Django website that stores the PackageFiles and
tracks their status and what mirror/repo they belong to.  An agent is required
to poll Packrat and build on-disk repositories such as APT, YUM, or docker repo.  A related
project, packrat-agent, is available to perform this task if desired, otherwise, you
can consume the web API and put it to disk as if fits your needs.



To build the docs::

  sudo apt install python3-sphinx texlive-latex-base texlive-latex-extra

the for local html::

  make docs-html

point your browser to the docs/build/index.html file

for pdf::

  make docs-pdf

This will build packrat.pdf

Enjoy
