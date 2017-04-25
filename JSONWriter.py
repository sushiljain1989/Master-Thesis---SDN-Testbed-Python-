import sys
import json
from DataWriter import DataWriter
class JSONWriter(DataWriter):

	def write(self , data):
		print "writing to json "
		#print result
		json_result = json.dumps(data, sort_keys=True)
		return json_result
