from pymongo import MongoClient
from bson.objectid import ObjectId
import urllib2
import re
import datetime
import sys
#conn = MongoClient("mongodb://Rex:12345678@localhost")
conn = MongoClient("mongodb://rex:groupten123!@34.193.29.224")
Agnes = conn.Agnes
USERS = Agnes.users
GROUPS = Agnes.groups

def groupAdmin(userID, useremail):
	for group in GROUPS.find():
		if useremail in group["grpemail"]:
			groupID = group["_id"]
			if userID not in group["admin"]:
				admin = group["admin"]
				admin.append(ObjectId(userID))
				GROUPS.update_one({"_id":groupID},{"$set":{"admin":admin}})
				#print admin
				print "update group successfully!"

			user = USERS.find_one({"_id":ObjectId(userID)})
			grpItem = {}
			grpItem["groups_id"] = groupID
			grpItem["admin"] = True
			#print "123123123"
			if grpItem not in user["grp"]:
				grp = user["grp"]
				grp.append(grpItem)
				USERS.update_one({"_id":ObjectId(userID)},{"$set":{"grp":grp}})
				#print grp
				print "update user successfully!"

if __name__ == '__main__':
	if len(sys.argv) == 3:
		userID = sys.argv[1]
		useremail = sys.argv[2]
		groupAdmin(userID, useremail)
	else:
		print "Missing parameter!"