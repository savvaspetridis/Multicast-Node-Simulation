#!/bin/sh


#2013-02-20 04:14:44 - AP sets TX PHY bitrate to 6Mbps
#2013-02-20 04:14:54 - AP sets TX PHY bitrate to 9Mbps
#2013-02-20 04:15:05 - AP sets TX PHY bitrate to 12Mbps
#2013-02-20 04:15:15 - AP sets TX PHY bitrate to 18Mbps
#2013-02-20 04:15:25 - AP sets TX PHY bitrate to 24Mbps
#2013-02-20 04:15:35 - AP sets TX PHY bitrate to 36Mbps
#2013-02-20 04:15:45 - AP sets TX PHY bitrate to 48Mbps
#2013-02-20 04:15:55 - AP sets TX PHY bitrate to 54Mbps
#2013-02-20 04:16:05 - End of experiment

echo "import os
os.environ.setdefault(\"DJANGO_SETTINGS_MODULE\", \"amuse_project.settings\")
# your imports, e.g. Django models
from multicast_simulator.models import Interval_pFive, Interval_One, Interval_Two" > DjangoQueries.py

# 6 mbps:

python addAvgDjangoTable.py ../Logs 6 2 20 2013 4 14 45 8 0.5 1 2 >> DjangoQueries.py

# 9 mbps

python addAvgDjangoTable.py ../Logs 9 2 20 2013 4 14 55 8 0.5 1 2 >> DjangoQueries.py

# 12 mbps

python addAvgDjangoTable.py ../Logs 12 2 20 2013 4 15 06 8 0.5 1 2 >> DjangoQueries.py

# 18 mbps

python addAvgDjangoTable.py ../Logs 18 2 20 2013 4 15 16 8 0.5 1 2 >> DjangoQueries.py

# 24 mbps

python addAvgDjangoTable.py ../Logs 24 2 20 2013 4 15 26 8 0.5 1 2 >> DjangoQueries.py

# 36 mbps

python addAvgDjangoTable.py ../Logs 36 2 20 2013 4 15 36 8 0.5 1 2 >> DjangoQueries.py

# 48 mbps

python addAvgDjangoTable.py ../Logs 48 2 20 2013 4 15 46 8 0.5 1 2 >> DjangoQueries.py

# 54 mbps 

python addAvgDjangoTable.py ../Logs 54 2 20 2013 4 15 56 8 0.5 1 2 >> DjangoQueries.py
