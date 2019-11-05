import os
import pymysql
import pymysql.cursors
import flask
import contextlib

app = flask.Flask(__name__)

roles = " PRIMARY SECONDARY".split()
states = "ONLINE OFFLINE RECOVERING ERROR UNREACHABLE".split()

@app.route("/metrics", methods=["GET"])
def metrics():
	lines = []
	
	con = pymysql.connect(host=os.environ["MYSQL_HOST"],
		user=os.environ["MYSQL_USER"],
		password=os.environ["MYSQL_PASSWORD"],
		cursorclass=pymysql.cursors.DictCursor)
	with contextlib.closing(con):
		cur = con.cursor()
		n = cur.execute('''SELECT MEMBER_ID, MEMBER_HOST, MEMBER_STATE, MEMBER_ROLE, MEMBER_VERSION
			FROM performance_schema.replication_group_members''')
		names = "MEMBER_ID MEMBER_HOST MEMBER_STATE MEMBER_ROLE MEMBER_VERSION".split()
		
		params = {}
		for o in cur:
			host = o["MEMBER_HOST"].replace("-","_").replace(".","_")
#			params["%s_state" % host] = o["MEMBER_STATE"]
#			params["%s_role" % host] = o["MEMBER_ROLE"]
			params["%s_state" % host] = states.index(o["MEMBER_STATE"])
			params["%s_role" % host] = roles.index(o["MEMBER_ROLE"])
		
		lines += ["replication_group_members{%s} %d" % (
			", ".join(['%s="%s"' % (k,v) for k,v in params.items()]),
			n)]
		
		names = [
			"COUNT_ALLOC",
			"COUNT_FREE",
			"LOW_COUNT_USED",
			"HIGH_COUNT_USED",
			"CURRENT_COUNT_USED",
			"SUM_NUMBER_OF_BYTES_ALLOC",
			"SUM_NUMBER_OF_BYTES_FREE",
			"LOW_NUMBER_OF_BYTES_USED",
			"HIGH_NUMBER_OF_BYTES_USED",
			"CURRENT_NUMBER_OF_BYTES_USED",
		]
		cur.execute('SELECT * FROM performance_schema.memory_summary_global_by_event_name')
		for r in cur:
			for name in names:
				lines += ['mysql_memory_%s{event="%s"} %d' % (name, r["EVENT_NAME"], r[name])]
	
	return "\r\n".join(lines)

