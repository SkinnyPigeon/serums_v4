# The SERUMS Data Lake

This project contains everything needed to launch the Serums Data Lake using Docker.

To launch you need to rename **Dockerfile-no-ENV** to simply **Dockerfile** and ensure the correct details are filled in for:
- PGPASSWORD
- PGPORT
- PGUSER
- BCPASSWORD

Then run:
```
$ docker-compose up --build
```

This process will set everything up and start the server on port 5000.

***

This project directory is structured as follows:

**/** - The Docker files for building the project

***

**/code/** - The initial configuration files and executed code used to build the data lake plus the directory for the actual API

***

**/code/api/** - Contains the actual API code as well as the basic functions and initial configuration for it to work
- `00-run-me.py` - Calls each of the construction files for building and launching the data lake
- `01-install-python-requirements.py` - A distinctly un-pythonic way of handling this :smile:. This updates the os and install all the dependencies
- `setup-datalake.py` - Creates the structure for the RAPTOR/CUBE data lake structure
- `start-database.py` - Ensures the PostgreSQL database is up and running
- `create-source-tables.py` - Calls the code to build all of the SQLAlchemy Table classes in the source database
- `05-fill-source-tables.py` - Inserts all of the data from the CSV files into the newly created source tables
- `06-convert-files.py` - Converts images and pdfs into ascii strings for storage in the database ready for transmission with rest of Smart Patient Health Record
- `07-run-api.py` - Starts the Gunicorn server on port 5000 with several workers

***

**/code/api/functions/** - A series of files that each handle each of the end point groups plus a couple helper files:
- `departments.py` - Used for querying the staff tables
- `encryption.py` - Used for handling the encryption and decryption of any requests and responses that require it
- `get_source_data.py` - The main code for creating the Smart Patient Health Record
- `jwt.py` - Used for validating the jwts in the request headers
- `lineage.py` - Calls the lineage blockchain during the creation process of the Smart Patient Health Record
- `ml.py` - Returns the data for the machine learning component of the SCHS
- `search.py` - Used for returning the Serums ID of a patient based on known information within a hospital's source systems
- `tags.py` - Returns lists of tags as well as translated/human readable versions

***

**/code/api/reset_sql/** - The files used to build and fill the source databases:
- `source_tables.py` - Complete collection of SQLAlchemy Table classes used to build all of the source tables
- `data/` - Series of CSV files which contain the data for the database
- `reset.md` - Used during development to quickly drop and rebuild the source database

***

**/code/api/sources/** - A couple sets of control files used in backend functions:
- `search_details` - Used to map the request query columns to their native values for use by the search functionality
- `tags` - A very important set of files which provide the *tag* definitions. Tags are used by the end users to create rules governing access to their data. They achieve this by selecting tags in the frontend to suit their current requirements. Tags are designed by the hospitals themselves in order to intelligently group subsets of data into useful packets as well as ensuring any data that can be selected falls within their governance

***

**/code/config/** - Contains a semi-randomly generated key used by the server. It can be changed before deploying the container

***

**/code/entrypoint/** - Contains a small bash script that is ran once the Docker container has been built. This starts the database and begins the process of building and filling the data lake, as well as finally starting the server