#!/bin/sh
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=/dltk/app/index.py
export FLASK_DEBUG=1

umask 002
cp -R -n /dltk/app /srv
cp -R -n /dltk/notebooks /srv
#if ! whoami &> /dev/null; then
  if [ -w /etc/passwd ]; then
    echo "dltk:x:$(id -u):0:dltk user:/dltk:/sbin/nologin" >> /etc/passwd
  fi
#fi
export HOME=/dltk

jupyter lab --port=8888 --ip=0.0.0.0 --no-browser --LabApp.base_url=$JUPYTER_BASE_URL_PATH & tensorboard --bind_all --logdir /srv/notebooks/logs/ & flask run -h 0.0.0.0
