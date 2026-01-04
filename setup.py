from setuptools import find_packages, setup


with open("README.md") as f:
    setup(
        name="NoSQLMap",
        version="0.8",
        packages=find_packages(),
        scripts=[
            "nosqlmap.py",
            "nsmmongo.py",
            "nsmcouch.py",
            "nsmscan.py",
            "nsmweb.py",
            "exception.py",
        ],
        entry_points={"console_scripts": ["NoSQLMap = nosqlmap:main"]},
        install_requires=[
            "CouchDB",
            "httplib2",
            "ipcalc",
            "pbkdf2",
            "pymongo",
            "requests",
        ],
        author="tcstool",
        author_email="codingo@protonmail.com",
        description="Automated MongoDB and NoSQL web application exploitation tool",
        license="GPLv3",
        long_description=f.read(),
        url="http://www.nosqlmap.net",
    )
