from setuptools import find_packages, setup


with open("README.md") as f:
	setup(
			name = "NoSQLMap",
			version = "0.7",
			packages = find_packages(),
			scripts = ['nosqlmap.py', 'nsmmongo.py', 'nsmcouch.py', 'nsmscan.py', 'nsmweb.py', 'exception.py'],
			
			entry_points = {
				"console_scripts": [
					"NoSQLMap = nosqlmap:main"
					]
				},
			
			install_requires = [ "CouchDB==1.0", "httplib2==0.19.0", "ipcalc==1.1.3",\
								 "NoSQLMap==0.7", "pbkdf2==1.3", "pymongo==2.7.2",\
								 "requests==2.32.0"],
	
			author = "tcstool",
			author_email = "codingo@protonmail.com",
			description = "Automated MongoDB and NoSQL web application exploitation tool",
			license = "GPLv3",
			long_description = f.read(),
			url = "http://www.nosqlmap.net"
		)
