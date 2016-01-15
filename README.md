# How to set up a local version of the web application:

1. Install Python. We use (Python 2.7.10): https://www.python.org/downloads/ 

2. Navigate to the directory in which you’d like to store the project and proceed to clone it. 

		git clone https://github.com/Wimnet/Demo

3. Install virtualenv: http://virtualenv.readthedocs.org/en/latest/installation.html

		[sudo] pip install virtualenv

4. Make a new virtual environment. It does not matter where you create it, but I like to keep the directory next to the root of the specific project directory structure. So, in the same directory that you cloned the project run the following command: 
	
		virtualenv amuse_env 

   ‘amuse_env’ is the name of the virtual environment.

5. Turn on the virtual environment
	
		cd amuse_env/bin
		source activate

	To turn off the virtual environment:
	
	 	deactivate

6. Add the rest of the dependencies to the virtual environment

    	pip install django
    	pip install psycopg2

7. Install PostgreSQL: http://www.postgresql.org/download/
   
   We used a handy video on Lynda.com that guides you through the process of installing PostgreSQL, creating a user for it, and installing a very helpful interface to interact with Postgres without using the command line:
   
   http://www.lynda.com/PostgreSQL-tutorials/Installing-PostgreSQL-Mac/73930/93118-4.html

   If you do not want to use the video to install postgres/the useful interface: 

   Install postgres and create a new user for it:  
 
	  1. On a Mac to create a new user for Postgres:
	  2. Go to Systems Preferences
	  3. Make a new Standard user with the Full Name being “PostgreSQL” and Account Name as “postgres” with a password of your choice (remember this password!).

8. Create a new PostgreSQL database
	1. With the handy interface (pgAdmin III): 
		1. Connect to Postgres (Double click PostgreSQL X.X (localhost:port)
		2. Enter the password
	 	3. Select ‘Databases’ 
		4. Press on the blue arrow above with ‘Databases’ selected. The blue arrow button creates a new object of whatever is highlighted.
		5. Name the database and give it a user.

	2. Without the handy interface:
      1. Interact with Postgres using the ‘psql’ command 

       			psql -U postgres

			A new command prompt should appear once you’ve connected to Postgres as a specific user. Use the ‘\l’ command to see what databases are currently there. 

				postgres=# \l 

			Go ahead and create a new database for the Multicast Emulator: 

				postgres=# CREATE DATABASE amuse;;

9. Connect Multicast Emulator with the new database: 

	Let’s assume the database you’ve created is called “dbamuse” and the user is “amuse” and the password is “cool beans” 

	Go to settings.py (from the directory you cloned the project and created the virtualenv): 
		vim Demo/amuse_project/amuse_project/settings.py
	Once the file is opened, find the database section labeled “DATABASES”. Change the NAME, USER, and PASSWORD section to reflect the relevant fields of the new database you have created. 

	Let’s set up the beginnings of our new dataless database! 

	Before we move on, it is necessary to address possible errors. First check for any previous migrations: 

		cd Demo/amuse_project/multicast_simulator/migrations 

	If you see a “0001…”.py file, delete it. 

	Next, navigate to the directory in the project that contains the file ‘manage.py’: 

		cd Demo/amuse_project

	Run the following commands: 

		python manage.py makemigrations
		python manage.py migrate

	How to add Datasets: 

	add dumby datat

		python creator_new_db.py >> name.py
		
	where name.py is the name of the new python file
	
		python name.py

