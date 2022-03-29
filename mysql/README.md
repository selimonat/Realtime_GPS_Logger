When the container is first built, an internal init script is ran to prepare the default databases and tables of the container.
All additional sql commands in mysql/config/*.sql files are also executed during this init phase. However, this only happens if,

- these commands span one single line each and must end with a semi-colon.
- the persistence folder mysql/db is empty.
