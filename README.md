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
```

# Bot commands

> /messages

Lists all the messages from the message list with its index and content.
___

> /m_add\
> {Your message here}

Adds a new message to the message list.
___

> /m_remove {index}

Removes the message with the given index from the message list.
___

> /m_clear

Removes all the messages from the message list.
___

> /k_add {keyword 1} {keyword 2} {keyword 3}

Adds the keywords to the keyword list.
___

> /k_remove {keyword 1} {keyword 2} {keyword 3}

Removes the given keywords from the keyword list.
___

> /k_clear

Removes all the keywords from the keyword list.
___

> /info

Returns the info about delay, keywords and message count.
___

> /delay {seconds}

Sets the delay to the given delay input.
___

> /clear

Deletes all the command messages (inside 'Saved Messages') from the current session.
___

> /exit

Terminates the program and deletes all the messages (inside 'Saved Messages') from the session.
___