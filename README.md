# Install and run

Make sure that the lastest version of Python is installed on your machine.

Then install and upgrade pip:

```
py -m pip install --upgrade pip
```

Then install all the required packages:

```
pip install --upgrade telethon python-dotenv
```

To run the program, open the terminal, navigate to the working dir, and execute:

```
py ./program.py
```

# Env file

Create an empty __.env__ file in the working dir, and paste the variables that can be found below this text. Make sure to assign the variables your own values. _API_ID_ and _API_HASH_ are required to make the program work, the other env variables are optional.

```
API_ID=
API_HASH=""
DELAY=
KEYWORDS=""
REPLY_MESSAGE=""
```
