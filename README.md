# pyutils
Common utilities for python projects

## Development instructions
- clone the repo
- install the dependencies
  ```
  poetry install
  ```
- make changes
- add tests and run them with 
  ```cmd
  pytest
  ```
- commit changes
- bump version depending on the level of changes
  ```cmd
  bump2version patch
  bump2version minor
  bump2version major
  ```
- push
  ```cmd
  git push --follow-tags
  ```

## Usage
To install from github:
```cmd
pip install git+https://github.com/jorritvm/pyutils.git
or
poetry add git+https://github.com/jorritvm/pyutils.git
```

To install from pypi (coming soon):
```
pip install pyutils-jvm
or
poetry add pyutils-jvm
```

## Author
Jorrit Vander Mynsbrugge