python3 -c "import cv2" > /dev/null 2>&1
if [ $? -eq 0 ] 
then
	echo "";
	echo "";
	echo "";
else
	sudo -H pip install -r requirements.txt
fi
python3 -c "import Flask" > /dev/null 2>&1
if [ $? -eq 0 ] 
then
	echo "";
	echo "";
	echo "";
else
	sudo -H pip install -r requirements.txt
fi
python3 -c "import subprocesses" > /dev/null 2>&1
if [ $? -eq 0 ] 
then
	echo "";
	echo "aaa";
	echo "";
else
	sudo -H pip install -r requirements.txt
fi
python3 -c "import numpy" > /dev/null 2>&1
if [ $? -eq 0 ] 
then
	echo "";
	echo "";
	echo "";
else
	sudo -H pip install -r requirements.txt
fi
python3 -c "import simplejson" > /dev/null 2>&1
if [ $? -eq 0 ] 
then
	echo "";
	echo "";
	echo "";
else
	sudo -H pip install -r requirements.txt
fi
python3 -c "import pprint" > /dev/null 2>&1
if [ $? -eq 0 ] 
then
	echo "";
	echo "";
	echo "";
	
else
	sudo -H pip install -r requirements.txt
fi
python3 -c "import matplotlib" > /dev/null 2>&1
if [ $? -eq 0 ] 
then
	echo "";
	echo "";
	echo "";
	
else
	sudo -H pip install -r requirements.txt
fi
python3 -c "import nltk" > /dev/null 2>&1
if [ $? -eq 0 ] 
then
	echo "";
	echo "";
	echo "";
	
else
	sudo -H pip install -r requirements.txt
fi

python app.py