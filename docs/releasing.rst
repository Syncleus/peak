=========
Releasing
=========

* Ensure you have an account on PyPI, if you do not create one `here <https://pypi.python.org/pypi?%3Aaction=register_form>`_.

* Create or verify your `~/.pypirc` file. It should look like this::

    [distutils]
    index-servers =
      pypi
      pypitest

    [pypi]
    repository=https://pypi.python.org/pypi
    username = <username>
    password = <password>

    [pypitest]
    repository=https://testpypi.python.org/pypi
    username = <username>
    password = <password>


* Update CHANGELOG.rst

* Commit the changes::

    git add CHANGELOG.rst
    git commit -m "Changelog for upcoming release 0.1.1."


* Install the package again for local development, but with the new version number::

    python setup.py develop


* Run the tests::

    tox


* Release on PyPI by uploading both sdist and wheel::

    python setup.py sdist upload -r pypi
    python setup.py sdist upload -r pypitest
    python setup.py bdist_wheel --universal upload -r pypi
    python setup.py bdist_wheel --universal upload -r pypitest

  NOTE: Make sure you have Python Wheel installed for your distribution or else the above commands will not work.

* Create git tag for released version::

    git tag -a v0.1.1 -m "version 0.1.1"


* Update version number (can also be minor or major)::

    bumpversion patch


* Commit the version bump changes::

    git add .
    git commit -m "Bumping version for release cycle"


* Test that it pip installs::

    pip install apex-radio
    <try out my_project>


* Push: `git push`

* Push tags: `git push --tags`

* Check the PyPI listing page to make sure that the README, release notes, and roadmap display properly. If not, copy
  and paste the RestructuredText into `ninjs <http://rst.ninjs.org/>`_ to find out what broke the formatting.

* Edit the release on `GitHub <https://github.com/Syncleus/apex/releases>`_ . Paste the release notes into the
  release's release page, and come up with a title for the release.
