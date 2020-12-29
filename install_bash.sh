#!bin/bash
python setup.py sdist bdist_wheel
# python3 -m pip install --user --upgrade twine
python -m twine upload --repository pypi dist/*