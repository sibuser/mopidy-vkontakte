****************************
Mopidy-VKMusic
****************************

.. image:: https://pypip.in/v/Mopidy-VKMusic/badge.png
    :target: https://crate.io/packages/Mopidy-VKMusic/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/Mopidy-VKMusic/badge.png
    :target: https://crate.io/packages/Mopidy-VKMusic/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/sibuser/mopidy-vkmusic.png?branch=master
    :target: https://travis-ci.org/sibuser/mopidy-vkmusic
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/sibuser/mopidy-vkmusic/badge.png?branch=master
   :target: https://coveralls.io/r/sibuser/mopidy-vkmusic?branch=master
   :alt: Test coverage

Mopidy extension for VKMusic allows to listen to music from VKontakte social network."


Installation
============

Install by running::

    pip install Mopidy-VKMusic

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-VKMusic to your Mopidy configuration file::

    [vkmusic]
    email    = your_email@maild_domen.com or phone number
    password = secret
    client_id = optional

#. You must register for a user account at http://www.vk.com/

#. Add the email and password to the ``mopidy.conf`` config file::

#. Hence VKontakte has only one playlist you can add and remove songs only from it.






Project resources
=================

- `Source code <https://github.com/sibuser/mopidy-vkmusic>`_
- `Issue tracker <https://github.com/sibuser/mopidy-vkmusic/issues>`_
- `Download development snapshot <https://github.com/sibuser/mopidy-vkmusic/tarball/master#egg=Mopidy-VKMusic-dev>`_


Changelog
=========

v0.1.2 (Beta)
----------------------------------------

- FIXED: In some cases your token can be expired and you needed to remove a db file manually.

v0.1.1 (UNRELEASED)
----------------------------------------

- Code style fixed. Setup a test cover system.

v0.1.0 (UNRELEASED)
----------------------------------------

- Initial release.
