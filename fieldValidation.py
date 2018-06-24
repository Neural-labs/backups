from pymongo import MongoClient

conn = MongoClient("mongodb://rex:groupten123!@34.193.29.224")

Agnes = conn.Agnes
EVENT = Agnes.events
USER = Agnes.users
GROUP = Agnes.groups

def getGroupFieldContent(collection):
	for collectionItem in collection.find():
		members = collectionItem["members"]
		pendingreq = collectionItem["pendingreq"]
		admin = collectionItem["admin"]
		events = collectionItem["events"]
		isFound = False
		print "#################"
		print collectionItem["_id"]

		#get data
		newMembers = []
		if members != []:
			for memberItem in members:
				if checkIdExist(USER, memberItem):
					newMembers.append(memberItem)
				else:
					isFound = True
		
		newPendingreq = []
		if pendingreq != []:
			for pendingreqItem in pendingreq:
				if checkIdExist(USER, pendingreqItem):
					newPendingreq.append(pendingreqItem)
				else:
					isFound = True

		newAdmin = []
		if admin != []:
			for adminItem in admin:
				if checkIdExist(USER, adminItem):
					newAdmin.append(adminItem)
				else:
					isFound = True

		newEvents = []
		if events != []:
			for eventItem in events:
				if checkIdExist(EVENT, eventItem):
					newEvents.append(eventItem)
				else:
					isFound = True

		newEvtcount = len(newEvents)
		newMemcount = len(newMembers)

		#notifaction
		if isFound == True:
			print "change!"

		#update collection
		collection.update_one({"_id":collectionItem["_id"]},{"$set": {"members":newMembers,"pendingreq":newPendingreq,"admin":newAdmin, "events":newEvents, "evtcount": newEvtcount, "memcount":newMemcount}})
		
		print "##################"
		#raw_input("Pause")
		

def getEventFieldContent(collection):
	for collectionItem in collection.find():
		attendees = collectionItem["attendees"]
		isFound = False
		print "###################"
		print collectionItem["_id"]

		newAttendees = []
		if attendees != []:
			for attendeeItem in attendees:
				if checkIdExist(USER, attendeeItem):
					newAttendees.append(attendeeItem)
				else:
					isFound = True

		newAttendcount = len(newAttendees)

		#notification
		if isFound == True:
			print "change!"

		collection.update_one({"_id":collectionItem["_id"]},{"$set": {"attendees":newAttendees, "attendcount":newAttendcount}})
		print "####################"

def checkIdExist(collection, itemId):
	for idItem in collection.find({"_id":itemId}):
		if idItem != None:
			#print "True"
			#print itemId
			return True
	# print "False"
	# print itemId
	return False

if __name__ == '__main__':
	getGroupFieldContent(GROUP)
	getEventFieldContent(EVENT)