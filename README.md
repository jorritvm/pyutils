# pyutils
Common utilities for python projects

## Development instructions
The project does not use the src/ layout. 
This means the package root is located directly in the project root. 

As such you do not need to install the project in editable mode `poetry add --editable ./pyutils/`.  
Instead, not installing the package at all will allow you to import the code directly from the project root.

- clone the repo
- install the dependencies
  ```
  poetry install --no-root
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
- push to github
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