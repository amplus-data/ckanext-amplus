[![Gitter][]][1] [![Python][]][2] [![CKAN][]][3]

# ckanext-amplus

This extension provides Amplus theme for CKAN.

## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.9             | yes   |

This extension requires [ckanext-c3charts](https://github.com/keitaroinc/ckanext-c3charts) to be installed and enabled.

## Installation

To install ckanext-amplus:

1. Activate your CKAN virtual environment, for example:

   ```. /usr/lib/ckan/default/bin/activate```

2. Clone the source and install it on the virtualenv

   ```
   git clone https://github.com/amplus-data/ckanext-amplus.git
   cd ckanext-amplus
   pip install -e .
   pip install -r dev-requirements.txt 
   ```

3. Add `amplus` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).\
   `ckan.plugins = amplus`

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

   ```sudo service apache2 reload```


## Config settings

None at present

## Developer installation

To install ckanext-amplus for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/amplus-data/ckanext-amplus.git
    cd ckanext-amplus
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-amplus

If ckanext-amplus should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

       pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)


  [Gitter]: https://badges.gitter.im/keitaroinc/ckan.svg
  [1]: https://gitter.im/keitaroinc/ckan?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
  [Python]: https://img.shields.io/badge/python-3.8-blue
  [2]: https://www.python.org
  [CKAN]: https://img.shields.io/badge/ckan-2.9-red
  [3]: https://www.ckan.org