#rm zinat.db
#./clone.sh
#python populate.py

gunicorn --bind unix:zinat.sock main:app \
	 --keep-alive 5 \
	 --reload \
	 --log-level DEBUG \
	 --workers 3

#uwsgi uwsgi.ini
