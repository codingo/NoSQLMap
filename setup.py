from setuptools import find_packages, setup


with open("README.md") as f:
	setup(
			name = "NoSQLMap",
			version = "0.5",
			packages = find_packages(),
			scripts = ['nosqlmap.py', 'nsmmongo.py', 'nsmcouch.py'],
			
			entry_points = {
				"console_scripts": [
					"NoSQLMap = nosqlmap:main"
					]
				},
			
			install_requires = [ "CouchDB==1.0", "httplib2==0.9", "ipcalc==1.1.3",\
								 "NoSQLMap==0.5", "pbkdf2==1.3", "pymongo==2.7.2",\
								 "requests==2.5.0"],
	
			author = "tcstools",
			author_email = "nosqlmap@gmail.com",
			description = "Automated MongoDB and NoSQL web application exploitation tool",
			license = "GPLv3",
			long_description = f.read(),
			url = "http://www.nosqlmap.net"
		)
