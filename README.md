NoSQLMap 
========

[http://www.nosqlmap.net](NoSQLMap) v0.1 

Introduction
============

NoSQLMap is an open source Python tool designed to audit for as well as automate injection attacks and exploit default configuration weaknesses in NoSQL databases as well as web applications using NoSQL in order to disclose data from the database.  It is named as a tribute to Bernardo Damele and Miroslav's Stampar's popular SQL injection tool SQLmap, and its concepts are based on and extensions of Ming Chow's excellent presentation at Defcon 21, "Abusing NoSQL Databases".  Presently the tool's exploits are focused around MongoDB, but additional support for other NoSQL based platforms such as CouchDB, Redis, and Cassandra are planned in future releases.

Requirements 
============

Varies based on features used:
-Python with PyMongo, httplib2, and urllib available; There are some various other libraries required that a normal Python installation should have readily available.  Your milage may vary, check the script.  
-Metasploit Framework

Usage:

-Start with

```
./nosqlmap.py 
```

or

```
python nosqlmap.py.
```
-NoSQLMap uses a menu based system for building attacks.  Upon starting NoSQLMap you are presented with with the main menu:

```
1-Set options (do this first)
2-NoSQL DB Access Attacks
3-NoSQL Web App attacks
4-Exit
```

**ALWAYS USE OPTION 1 FIRST TO SET THE PARAMETERS!**

Explanation of options:
Set target host/IP-The target web server (i.e. www.google.com) or MongoDB server you want to attack.
1 - Set web app port-TCP port for the web application if a web application is the target
2 - Set URI Path-The portion of the URI containing the page name and any parameters but NOT the host name (e.g. acct.php?acctid=102)
3 - Set HTTP Request Method (GET/POST)-Set the request method to a GET or POST; Presently only GET is implemented but working on implementing POST requests exported from Burp. 
4 - Set my local Mongo/Shell IP-Set this option if attacking a MongoDB instance directly to the IP of a target Mongo installation to clone victim databases to or open Meterpreter shells to.
5 - Set shell listener port-If opening Meterpreter shells, specify the port.
6 - Back to main menu

Once options are set head back to the main menu and select DB access attacks or web app attacks as appropriate.  Send emails to tcstool@gmail.com or find me on Twitter [https://twitter.com/tcstoolHax0r](@tcstoolHax0r) if you have any questions or suggestions.  
