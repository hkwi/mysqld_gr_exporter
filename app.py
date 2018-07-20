import os
import pymysql
import flask
import contextlib

app = flask.Flask(__name__)

roles = " PRIMARY SECONDARY".split()
states = "ONLINE OFFLINE RECOVERING ERROR UNREACHABLE".split()

@app.route("/metrics", methods=["GET"])
def metrics():
	lines = ""
	con = pymysql.connect(host=os.environ["MYSQL_HOST"],
		user=os.environ["MYSQL_USER"],
		password=os.environ["MYSQL_PASSWORD"])
	with contextlib.closing(con):
		cur = con.cursor()
		n = cur.execute('''SELECT MEMBER_ID, MEMBER_HOST, MEMBER_STATE, MEMBER_ROLE, MEMBER_VERSION
			FROM performance_schema.replication_group_members''')
		names = "MEMBER_ID MEMBER_HOST MEMBER_STATE MEMBER_ROLE MEMBER_VERSION".split()
		
		params = {}
		for r in cur:
			o = dict(zip(names,r))
			host = o["MEMBER_HOST"]
			params["%s.state" % host] = o["MEMBER_STATE"]
			params["%s.role" % host] = o["MEMBER_ROLE"]
			params["%s.state.index" % host] = states.index(o["MEMBER_STATE"])
			params["%s.role.index" % host] = roles.index(o["MEMBER_ROLE"])
		
		lines += "replication_group_members{%s} %d\r\n" % (
			", ".join(['%s="%s"' % (k,v) for k,v in params.items()]),
			n)
		
		return lines

