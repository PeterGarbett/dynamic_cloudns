
This is the python I use to update my dns record on cloudns.

Usage
-----

You need to open an account https://www.cloudns.net/dynamic-dns/ 
and obtain a lease renewing url which will be of the form

"https://ipv4.cloudns.net/api/dynamicURL/?q=kJaqdJQDjbkqjbjjKJNSDSwhbdSBdswDK;W"

Which you edit into the file dynamic_cloudns . Then sudo ./setup,
then the usual systemctl stuff for services run by a timer





~                                                      
