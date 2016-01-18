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

NOTE: If you're having issues with migrations (python manage.py makemigrations/migrate/runserserver aren't working) try turn off the virtual environment. 

# Video Setup:

Note: The video is the most complicated feature on the app, and setup on each system so far has been different.

1. In Demo/amuse_project run 'make'. This will create the 'correlator' executable which actually modifies the video.
2. In Demo/amuse_project run the following command to generate the directory structure to play the 'football' video. Detailed instructions on how to play different videos will be given in the section on modifying video functionality.
			
			./splice_video.sh Football ../Video/football.y4m 1020K 1440K 1800K 2480K 3060K 4000K 4660K 4900K 8



# Add a New Dataset

Overview: To add a new dataset you must first add the information from an experiment to the Django database. This is done by writing a script (in this example addAllDjangoTables.py) which generates a script (Django_Queries_set_1.py) which when run in the /Demo/amuse_project directory will add the new dataset to the Django database.

1.  Copy tar file of the new dataset to Demo/amuse_project/multicast_simulator/pcapScripts/Datasets
2.  Create a new file in pcapScripts and save it as *.py where *.py is the name of the script.
3.  Open addAllDjangoTables.py script and copy the contents to your new file. The format of the new python script should be something like this:


		#!/bin/sh


		# 2015-01-06 12:41:32 - AP sets TX PHY bitrate to 6Mbps
		# 2015-01-06 12:41:42 - AP sets TX PHY bitrate to 9Mbps
		# 2015-01-06 12:41:52 - AP sets TX PHY bitrate to 12Mbps
		# 2015-01-06 12:42:02 - AP sets TX PHY bitrate to 18Mbps
		# 2015-01-06 12:42:12 - AP sets TX PHY bitrate to 24Mbps
		# 2015-01-06 12:42:23 - AP sets TX PHY bitrate to 36Mbps
		# 2015-01-06 12:42:33 - AP sets TX PHY bitrate to 48Mbps
		# 2015-01-06 12:42:43 - AP sets TX PHY bitrate to 54Mbps
		# 2015-01-06 12:42:53 - End of experiment
		
		echo "import os
		os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"amuse_project.settings\")
		# your imports, e.g. Django models
		from multicast_simulator.models import Node, Packet_List" > DjangoQueries_set_1.py
		
		# 6 mbps:
		
		
		python addAvgDjangoTable.py ./set_1 6 1 6 2015 12 41 34 8 set_1_1 0.5 1 2 >> DjangoQueries_set_1.py
		
		# 9 mbps
		
		python addAvgDjangoTable.py ./set_1 9 1 6 2015 12 41 43 8 set_1_1 0.5 1 2 >> DjangoQueries_set_1.py
		
		# 12 mbps
		
		python addAvgDjangoTable.py ./set_1 12 1 6 2015 12 41 53 8 set_1_1 0.5 1 2 >> DjangoQueries_set_1.py
		
		# 18 mbps
		
		python addAvgDjangoTable.py ./set_1 18 1 6 2015 12 42 03 8 set_1_1 0.5 1 2 >> DjangoQueries_set_1.py
		
		# 24 mbps
		
		python addAvgDjangoTable.py ./set_1 24 1 6 2015 12 42 13 8 set_1_1 0.5 1 2 >> DjangoQueries_set_1.py
		
		# 36 mbps
		
		python addAvgDjangoTable.py ./set_1 36 1 6 2015 12 42 24 8 set_1_1 0.5 1 2 >> DjangoQueries_set_1.py
		
		# 48 mbps
		
		python addAvgDjangoTable.py ./set_1 48 1 6 2015 12 42 34 8 set_1_1 0.5 1 2 >> DjangoQueries_set_1.py
		
		# 54 mbps 
		
		python addAvgDjangoTable.py ./set_1 54 1 6 2015 12 42 44 8 set_1_1 0.5 1 2 >> DjangoQueries_set_1.py

4. In the line:
 


		echo "import os
		os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"amuse_project.settings\")
		# your imports, e.g. Django models
		from multicast_simulator.models import Node, Packet_List" > DjangoQueries_set_1.py

    Replace 'DjangoQueries_set_1.py' or the name of the script the script generates to the name you want that script to have (for convention it should probably be something like DjangoQueries_{experiment name you specify for the queries}

5. Open bitrate_log.txt in new experiment directory and copy contents and replace the access point information (the nine lines commented out two lines bellow #!/bin/sh) in your new file with the copied contents. Be sure to comment it out.
6. Replace 1st command line argument (./set1 in this example) in each 'python addAvgDjangoTable.py ..." line of the script with the new path to the new dataset directory in Demo/amuse_project/multicast_simulator/pcapScripts/Datasets.
6. The 2nd command line argument in each of these commands is the bit-rate, so you'll probably want to leave that alone unless you're adding a dataset with a bit-rate which is not in the set {6, 9, 12, 18, 24, 36, 48, 54} (all MBPS) or adding a dataset without one of these bitrates, in which case there may be extra steps needed. 
7. The 3rd (day), 4th (month), 5th (year), 6th (hour), 7th (minute) and 8th (second) command line arguments correspond to the start time of the bit-rate in the given experiment.  Copy these values for each bit rate bitrate_log.txt. Keep in mind you probably want to shave off the first second (record the seconds in this script as one or two more than in bitrates.txt) or two of each experiment to ignore eronious interference. 
8. The 9th command line argument is the length of the experiment, or how many seconds after the start time the script will take into account when generating queries. 
9. The 10th command line argment is the name of the experiment you want in the Django database. This should probably be the same for all experiments. 
10.
