Installing / Upgrading
======================
.. highlight:: bash

**LiveTribe Plugins** is in the `Python Package Index
<http://pypi.python.org/pypi/livetribe-plugins/>`_.

Installing with pip
-------------------

We prefer `pip <http://pypi.python.org/pypi/pip>`_
to install livetribe-plugins::

  $ pip install livetribe-plugins

To get a specific version of livetribe-plugins::

  $ pip install livetribe-plugins==1.0.0

To upgrade using pip::

  $ pip install --upgrade livetribe-plugins

Installing with easy_install
----------------------------

If you must install livetribe-plugins using
`setuptools <http://pypi.python.org/pypi/setuptools>`_ do::

  $ easy_install livetribe-plugins

To upgrade do::

  $ easy_install -U livetribe-plugins

Installing from source
----------------------

If you'd rather install directly from the source (i.e. to stay on the
bleeding edge), check out the latest source from github and install
from the resulting tree::

  $ git clone git://github.com/livetribe/livetribe-plugins.git livetribe-plugins
  $ cd livetribe-plugins/
  $ python setup.py install


Building LiveTribe Plugins egg Packages
---------------------------------------

Some organizations do not allow compilers and other build tools on production
systems. To install LiveTribe Plugins on these systems you may need to
build custom egg packages. Make sure that you have installed the dependencies
listed above for your operating system then run the following command in the
LiveTribe Plugins source directory::

  $ python setup.py bdist_egg

The egg package can be found in the dist/ subdirectory. The file name will
resemble “livetribe_plugins-1.0.0-py2.6.egg” but may have a different name
depending on your platform and the version of python you use to compile.

Copy this file to the target system and issue the following command to install the
package::

  $ sudo easy_install livetribe_plugins-1.0.0-py2.6.egg

Installing a release candidate
------------------------------

LiveTribe may occasionally tag a release candidate for testing by the community
before final release. These releases will not be uploaded to pypi but can be
found on the
`github tags page <https://github.com/livetribe/livetribe-plugins/tags>`_.
They can be installed by passing the full URL for the tag to pip::

  $ pip install https://github.com/livetribe/livetribe-plugins/tarball/2.2rc1

or easy_install::

  $ easy_install https://github.com/livetribe/livetribe-plugins/tarball/2.2rc1
