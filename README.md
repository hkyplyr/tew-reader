# TEW2020 Database Reader

## Requirements
* python3
* virtualenvwrapper
* meza (pip package)
* prettytable (pip package)

## Setup
#### Install Python and virtualenvwrapper (follow instructions from virtualenvwrapper output)
```
brew install python@3.8
pip3 install virtualenvwrapper
```

#### Clone and enter this repository
```
git clone ???/tew-reader
cd tew-reader
```

#### Create and use a new virtualenv named 'tew'
```
mkvirtualenv tew
workon tew
```

### Run program for the first time
```
pip install -r requirements.txt
python tew.py --help
```
