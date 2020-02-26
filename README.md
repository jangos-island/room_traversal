# CS Build Week 2

## Intitializing Project
___
## Python 3.8 Installation for MacOS 

### Method 1:

Install via this link: https://www.python.org/ftp/python/3.8.0/python-3.8.0a2-macosx10.9.pkg

Follow the instructions appropiately and then check version after installing to verify version:
```
~ python3.8 -V
Python 3.8.0a2
```

### Method 2: Using pyenv

```
brew install pyenv #if not installed
```

List available python versions.

```
pyenv install --list | grep 3.8
3.8-dev
miniconda-3.8.3
miniconda3-3.8.3
```

Now install python 3.8-dev

```
pyenv install 3.8-dev
```

### Python 3.8 Installation for Windows, Linux/UNIX, Mac OS X, Other

Utilize the following link to install Python for the above menttioned Operating Systems:

https://www.python.org/downloads/

----
## Adding .env File

Insert an  `.env` file to the projects root directory with the `API Key` from your respective TL/PM:

```
API_KEY="your_key"
```

## Run Pipenv Commands

Once all of the above has been completed then run the appropiate pipenv commands per usual:

```
pipenv install
pipenv shell
```


