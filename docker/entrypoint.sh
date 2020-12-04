#!/bin/sh

UWSGI_PORT="${UWSGI_PORT:-9001}"
UWSGI_PROCS=${UWSGI_PROCS:-4}
UWSGI_THREADS=${UWSGI_THREADS:-4}

export APP_INSTALL_DIR=/run/app/
export PRODUCTION_DB=${PRODUCTION_DB:-/var/lib/app/db/production.db}
chdir /run/app

export PATH=/run/app/venv/bin:$PATH
# if you want to use python's reference server ...
# good for debugging, don't use in production

# exec python3 manage.py serve -p 9001 -H 0.0.0.0

exec uwsgi --need-app \
	--honour-stdin \
	--pythonpath /run/app \
	--processes "${UWSGI_PROCS}" \
	--threads "${UWSGI_THREADS}" --http-socket 0.0.0.0:"${UWSGI_PORT}" \
	--wsgi-file=/run/app/app.py --callable=app --master \
	--vacuum \
	--log-master \
	--logformat 'pid: %(pid)|app: -|req: -/-] %(var.HTTP_X_REAL_IP) (%(user)) {%(vars) vars in %(pktsize) bytes} [%(ctime)] %(method) %(uri) => generated %(rsize) bytes in %(msecs) msecs (%(proto) %(status)) %(headers) headers in %(hsize) bytes (%(switches) switches on core %(core))'
