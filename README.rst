****************************
Mopidy-VKontakte
****************************

.. image:: https://pypip.in/v/Mopidy-VKontakte/badge.png
    :target: https://crate.io/packages/Mopidy-VKontakte/
    :alt: Latest PyPI version

.. image:: https://pypip.in/d/Mopidy-VKontakte/badge.png
    :target: https://crate.io/packages/Mopidy-VKontakte/
    :alt: Number of PyPI downloads

.. image:: https://travis-ci.org/sibuser/mopidy-vkontakte.png?branch=master
    :target: https://travis-ci.org/sibuser/mopidy-vkontakte
    :alt: Travis CI build status

.. image:: https://coveralls.io/repos/sibuser/mopidy-vkontakte/badge.png?branch=master
   :target: https://coveralls.io/r/sibuser/mopidy-vkontakte?branch=master
   :alt: Test coverage

Mopidy extension for VKontakte allows to listen to music from VKontakte social network."


Installation
============

Install by running::

    pip install Mopidy-VKontakte

Or, if available, install the Debian/Ubuntu package from `apt.mopidy.com
<http://apt.mopidy.com/>`_.


Configuration
=============

Before starting Mopidy, you must add configuration for
Mopidy-VKontakte to your Mopidy configuration file::

    [vkontakte]
    email    = your_email@maild_domen.com or phone number
    password = secret
    client_id = optional

#. You must register for a user account at http://www.vk.com/

#. Add the email and password to the ``mopidy.conf`` config file::

#. Hence VKontakte has only one playlist you can add and remove songs only from it.






Project resources
=================

- `Source code <https://github.com/sibuser/mopidy-vkontakte>`_
- `Issue tracker <https://github.com/sibuser/mopidy-vkontakte/issues>`_
- `Download development snapshot <https://github.com/sibuser/mopidy-vkontakte/tarball/master#egg=Mopidy-VKontakte-dev>`_


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
