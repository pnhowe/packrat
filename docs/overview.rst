Building the Packages
---------------------

After cloing the software to a working directory, first install the packaging
 requirements::

  sudo apt install dpkg-dev debhelper cdbs python-dev python-setuptools

next build the package::

  make dpkg

this will make a debian package, you install this package on your target
Packrat controller.

Installing the Package
----------------------

Copy the packrag-X.X.X.dpkg file to your desired Packrat master server and
install it.  After it is installed, run::

  /usr/lib/packrat/setup/setupWizard

to setup up the database.

now use your favorite web browser and goto http://<ip address of server> and
Packrat's AJAX style front end should load.  As a note this front end also consumes
the HTTP API, anything it can do, you can make your own client to automate if
desired.  NOTE: this being a django website http://<ip address>/admin pulls up
the standard Django admin site, this is not a part of the HTTP API.  The admin
username is root, password root.  Please change the defaults, you don't want
anyone else in ther promoting your files ;-)

If you are hosting more than one site on this server, you may need to modify
the server name in /etc/apache2/sites-available/packrat.conf


TODO: setting up first package


---- old stuff ----



Now we can try loading our first package, goto the ip/host of your new packrat server in a browser.  Click the `UI` link. Now login, you can use your admin user/password, click on Packages, click on "Add New Package".
Enter the basename of the package you would like to store, for example the base name of `packrat_0.4-1_all.deb` is `packrat`.  Now click "Add File", enter the Provenance of the File and the Justificaion for the File and
click "Select File", this will pop up a file selection dialog, select your package file and confirm you want to upload the file.  The select Submit.  If Packrat can not autodetect the distro that package belongs to, a dropdown
will apear and ask you to select the distro to apply the file to, if it does, select the distro and click submit again.  Now click on "Packages", then select you package base name, you should have your new file listed on the right.
click the Up Arrow to promote it to Ci, Dev, and the Stage, clicking the up arrow again will prompt you for a Change Controll number, enter the number and save, then click the up arrow again. It is now in the Production repo.  If
you click on the file drawer, it will set that file to the archive status.

On your packrat server, you should see the package file in /var/www/packrat/files.

You now need a Mirror entry for your packrat-agent to login with, in your url goto `http://< host or ip >/admin/` login with your admin user/pass, on the left click "+Add" by the Mirrors.  Give it a name, description, and a PSK
( ie a Pre Shared Key/Password) select from the Repo List which Repo Types and Release levels you would like to be sent to this mirror.

You are good to go, enjoy.
