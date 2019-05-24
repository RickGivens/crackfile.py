# crackfile.py
This program will read the contents of two files into separate dictionaries, search for identical keys in both dictionaries, and return the corresponding values. The original intent of this program is to compare a list of usernames and hashed passwords to a rainbow table. The program will search the rainbow table for the hashed password, and return both the username and password.

Example:

plato:73cd7520e0d5ab04fb196ba97a499de3

1f5b6d6065ab46634ba71e8f656f4f3d He#a0

If the hash (key) of the user file matches the hash of the rainbow table, the program will return the username and password

Current benchmark: The program will return three usernames and passwords from a rainbow table of five million entries in seven seconds.

To test this program, use the provided rainbowGenerator to create the rainbowTable and the provided shadow.txt file.

