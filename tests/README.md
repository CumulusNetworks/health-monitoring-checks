**Testing Health Check Monitors**

Some health monitoring checks are written in python, so it is possible to write
tests to simulate switch behavior to see how the check performs

To date only the cumulus-sw-temp plugin has been tested.

To run the tests, first you need a working python environment, i.e python is
installed.

Then install the latest version of pip using ``easy_install pip``. Pip should be
higher than 7.0

Then install the test python packages using ``pip install -r tests/pip_requirements.txt``

Finally from the root directory of the github repo, run ``nosetests``.

Example:

```
easy_install pip
pip -V
pip install -r tests/pip_requirements.txt
nosetests -v
```

