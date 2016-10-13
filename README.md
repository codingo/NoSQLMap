NoSQLMap 
========

[NoSQLMap](http://www.nosqlmap.net) v0.7

Introduction
============

NoSQLMap is an open source Python tool designed to audit for as well as automate injection attacks and exploit default configuration weaknesses in NoSQL databases as well as web applications using NoSQL in order to disclose data from the database.  

It is named as a tribute to Bernardo Damele and Miroslav's Stampar's popular SQL injection tool [sqlmap](http://sqlmap.org), and its concepts are based on and extensions of Ming Chow's excellent presentation at Defcon 21, ["Abusing NoSQL Databases"](https://www.defcon.org/images/defcon-21/dc-21-presentations/Chow/DEFCON-21-Chow-Abusing-NoSQL-Databases.pdf). Presently the tool's exploits are focused around MongoDB, but additional support for other NoSQL based platforms such as CouchDB, Redis, and Cassandra are planned in future releases.
A NoSQL (originally referring to "non SQL", "non relational" or "not only SQL") database provides a mechanism for storage and retrieval of data which is modeled in means other than the tabular relations used in relational databases. Such databases have existed since the late 1960s, but did not obtain the "NoSQL" moniker until a surge of popularity in the early twenty-first century, triggered by the needs of Web 2.0 companies such as Facebook, Google, and Amazon.com. NoSQL databases are increasingly used in big data and real-time web applications. NoSQL systems are also sometimes called "Not only SQL" to emphasize that they may support SQL-like query languages.

Requirements 
============
On a Debian or Red Hat based system, the setup.sh script may be run as root to automate the installation of NoSQLMap's dependencies.  

Varies based on features used:
- Metasploit Framework,
- Python with PyMongo, 
- httplib2, 
- and urllib available.
- A local, default MongoDB instance for cloning databases to.  Check [here](http://docs.mongodb.org/manual/installation/) for installation instructions.

There are some various other libraries required that a normal Python installation should have readily available. Your milage may vary, check the script.  

Setup
============
``python setup.py install``
Usage
=====

-Start with

```
NoSQLMap
```

NoSQLMap uses a menu based system for building attacks.  Upon starting NoSQLMap you are presented with with the main menu:

```
1-Set options (do this first)
2-NoSQL DB Access Attacks
3-NoSQL Web App attacks
4-Scan for Anonymous MongoDB Access
x-Exit
```


Explanation of options:
```
1. Set target host/IP-The target web server (i.e. www.google.com) or MongoDB server you want to attack.
2. Set web app port-TCP port for the web application if a web application is the target.
3. Set URI Path-The portion of the URI containing the page name and any parameters but NOT the host name (e.g. /app/acct.php?acctid=102).
4. Set HTTP Request Method (GET/POST)-Set the request method to a GET or POST; Presently only GET is implemented but working on implementing POST requests exported from Burp. 
5. Set my local Mongo/Shell IP-Set this option if attacking a MongoDB instance directly to the IP of a target Mongo installation to clone victim databases to or open Meterpreter shells to.
6. Set shell listener port-If opening Meterpreter shells, specify the port.
7. Load options file-Load a previously saved set of settings for 1-6.
8. Load options from saved Burp request-Parse a request saved from Burp Suite and populate the web application options.
9. Save options file-Save settings 1-6 for future use.
x. Back to main menu-Use this once the options are set to start your attacks.
```

Once options are set head back to the main menu and select DB access attacks or web app attacks as appropriate for whether you are attacking a NoSQL management port or web application. The rest of the tool is "wizard" based and fairly self explanatory, but send emails to nosqlmap@gmail.com or find me on Twitter [@tcstoolHax0r](https://twitter.com/tcstoolHax0r) if you have any questions or suggestions. 

Video
=====

NoSQLMap MongoDB Management Attack Demo.

<a href="http://www.youtube.com/watch?feature=player_embedded&v=xSFi-jxOBwM" target="_blank"><img src="http://img.youtube.com/vi/xSFi-jxOBwM/0.jpg" alt="NoSQLMap MongoDB Management Attack Demo" width="240" height="180" border="10" /></a> 

Contribute
==========

If you'd like to contribute, please create [new issue](https://github.com/tcstool/NoSQLMap/issues) or [pull request](https://github.com/tcstool/NoSQLMap/pulls).
