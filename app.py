import os
import pymysql
import flask
import contextlib

app = flask.Flask(__name__)

@app.route("/metrics", methods=["GET"])
def metrics():
	lines = ""
	con = pymysql.connect(host=os.environ["MYSQL_HOST"],
		user=os.environ["MYSQL_USER"],
		password=os.environ["MYSQL_PASSWORD"])
	with contextlib.closing(con):
		cur = con.cursor()
		cur.execute('''SELECT * FROM performance_schema.replication_group_members''')
		names = [d[0].lower() for d in cur.description]
		for r in cur:
			params = ", ".join(['%s="%s"' % nv for nv in zip(names, r)])
			lines += "replication_group_members{%s} 1\r\n" % params
		
		return lines

