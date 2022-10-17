#!/usr/bin/bash

page_dir='../leisure_prog_page'

echo 'Generate ICS'

source env/bin/activate
python run.py
deactivate

echo 'Deploy'

mv *.ics $page_dir
cd $page_dir
ls -l
git status
git add *.ics
git commit -m 'update ics'
git push

echo 'Done'
