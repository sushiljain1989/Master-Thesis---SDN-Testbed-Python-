import sys
import json
class json_writer:

	def write(self , result):
		print "writing to json "
		#print result
		json_result = json.dumps(result , sort_keys=True)
		print json_result
