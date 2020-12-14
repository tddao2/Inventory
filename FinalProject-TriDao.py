#Final Project - CIS 2348 - Fall 2020
#Tri Dao
#1954347

import datetime

class InventoryReports:

	# constructor
	def __init__(self, ManufactureFile, PriceFile, ServiceFile):
		# holds the list of manufacturing details
		self.manufactureList = []
		# dictionary to hold the price of an item
		self.priceDict = dict()
		# dictionary to hold the service date of an item
		self.serviceDateDict = dict()

		# loads the data from given files.
		self.loadData(ManufactureFile, PriceFile, ServiceFile)
		print("[...] Loaded Data")
		# opens the reports
		self.OpenReports()
		print("[...] Reports Opened")

	# loads the manufacturing details into the self.manufactureList
	def loadManufactureData(self, ManufactureFile):
		f = open(ManufactureFile)
		data = f.readlines()
		for line in data:
			# splitting on comma
			splitted = line.strip().split(',')
			# converting the first item to integer (bcz id)
			splitted[0] = int(splitted[0])
			# adding it to the list.
			self.manufactureList.append(splitted)
		# closing the file
		f.close()

	# loads the price detials into self.priceDict
	def loadPriceData(self, PriceFile):
		f = open(PriceFile)
		data = f.readlines()
		for line in data:

			splitted = line.strip().split(',')
			# converting values to integer (because id and price)
			for i in range(len(splitted)):
				splitted[i] = int(splitted[i])
			# adding to dictionary
			self.priceDict[splitted[0]] = splitted[1]

		# closing the file
		f.close()

	def loadServiceData(self, ServiceFile):
		f = open(ServiceFile)
		data = f.readlines()
		for line in data:
			splitted = line.strip().split(',')
			splitted[0] = int(splitted[0])
			self.serviceDateDict[splitted[0]] = splitted[1]

		# closing the file
		f.close()

	# calls the other loading functions
	def loadData(self, ManufactureFile, PriceFile, ServiceFile):
		self.loadManufactureData(ManufactureFile)
		self.loadPriceData(PriceFile)
		self.loadServiceData(ServiceFile)

	# opens the FullInventory.csv file
	def OpenFullInventory(self):
		self.fullInventory = [] # creating an empty full inventory list
		# looping through the manufacture list (sorted by manufacturer, then type)
		for data in sorted(self.manufactureList, key=lambda l:(l[1], l[2])):
			# making a full inventory data
			currentList = data[:-1]
			currentList.append(self.priceDict[currentList[0]])
			currentList.append(self.serviceDateDict[currentList[0]])
			currentList.append(data[-1])
			# adding the data to list
			self.fullInventory.append(currentList)

		# writing the full inventory list to the file
		with open('FullInventory.csv', 'w') as f:
			for data in self.fullInventory:
				f.write(','.join(map(str,data)) + "\n")
		# print(fullInventory)

	# opens the csv files based on type of items.
	def OpenTypeInventory(self):
		# getting the total numbers of types in full inventory
		types = set()
		for data in self.fullInventory:
			types.add(data[2])

		# for each type
		for typeName in types:
			# getting the data
			filteredInput = []
			for data in self.fullInventory:
				if (data[2] == typeName):
					copyList = data[:]
					del copyList[2]
					filteredInput.append(copyList)
			# writing the data to that types file (CSV)
			typeName = typeName.capitalize()
			with open(typeName + "Inventory.csv", 'w') as f:
				for data in sorted(filteredInput, key=lambda l:l[0]):
					f.write(','.join(map(str,data)) + "\n")

	# opens the 'PastServiceDateInventory.csv'
	def OpenPastServiceInventory(self):
		# getting the current date (today's date)
		CurrentDate = datetime.datetime.today()
		filteredInput = [] # holds the filtered input (past input)
		for data in self.fullInventory:
			# converting the data's date to datetime document
			dateCheck = datetime.datetime.strptime(data[-2], "%m/%d/%Y")
			if (dateCheck < CurrentDate):
				filteredInput.append(data)

		# writing the data(filtered) to file
		with open('PastServiceDateInventory.csv', 'w') as f:
			for data in sorted(filteredInput, key=lambda l:l[-2]):
				f.write(','.join(map(str,data)) + "\n")

	# opens the "DamagedInventory.csv"
	def OpenDamagedInventory(self):

		filteredInput = [] # empty filtered list at first
		for data in self.fullInventory:
			if (data[-1] == "damaged"): # if the data is damaged then add to list
				filteredInput.append(data[:-1])

		# writing to the file
		with open('DamagedInventory.csv', 'w') as f:
			for data in sorted(filteredInput, key=lambda l:l[3]):
				f.write(','.join(map(str,data)) + "\n")

	# calls the other open functions
	def OpenReports(self):
		self.OpenFullInventory()
		self.OpenTypeInventory()
		self.OpenPastServiceInventory()
		self.OpenDamagedInventory()

	# code to ask the user for interactive queries
	def interactiveQuery(self):
		# QuitDecision tells if user want to exit or not
		QuitDecision = True
		# getting the current date of today
		CurrentDate = datetime.datetime.today()
		# while user doesn't want to quit
		while QuitDecision:
			# getting the query.
			userInput = input("Enter manufacturer and item type (q for exit): ")
			# if query is for exit
			if (userInput.lower() == 'q'):
				print("Exited")
				QuitDecision = False
			else:
				# otherwise split of space(' ')
				splitted = userInput.split(",")
				if len(splitted) < 2: # if there are less than 2 words then invalid
					print("Sorry, your input must be separated by a comma. Please try again...")
				else:
					splitted = splitted[-2:]
					# getting the manufacturer and itemType from the splitted
					manufacturer, itemType = splitted[0], splitted[1]
					# gettings the filtered input, (not damaged and not past service date)
					ItemInformation = []
					ProductInformation = []
					for data in self.fullInventory:
						serviceDate = datetime.datetime.strptime(data[-2], "%m/%d/%Y")
						if (data[2].strip().lower() == itemType.strip().lower()
							and data[-1] != 'damaged' and serviceDate > CurrentDate):
							if (data[1].strip().lower() == manufacturer.lower()):
								ItemInformation.append(data)
							else:
								ProductInformation.append(data)

					# if no item found
					if len(ItemInformation) == 0:
						print("No such item in inventory")
					else: # otherwise print the most expensive found item
						ItemInformation = sorted(ItemInformation, key=lambda l:l[3], reverse=True)
						print("\nYour item is:", ItemInformation[0][0], ItemInformation[0][1], ItemInformation[0][2], ItemInformation[0][3])

						# checking if there is similar type of item in other manufacturer.
						current_min = -1
						# getting the nearest(closest) item to it.
						if len(ProductInformation) != 0:
							for i in range(len(ProductInformation)):
								if (abs(ProductInformation[i][3] - ItemInformation[0][3]) < current_min or current_min == -1):
									index = i
									current_min = abs(ProductInformation[i][3] - ItemInformation[0][3])
							print("\nYou may also consider:", ProductInformation[index][0], ProductInformation[index][1], ProductInformation[index][2], ProductInformation[index][3], "\n")

ManufactureFile = 'ManufacturerList.csv'
PriceFile = "PriceList.csv"
ServiceFile = "ServiceDatesList.csv"

GivenDodument = InventoryReports(ManufactureFile, PriceFile, ServiceFile)
GivenDodument.interactiveQuery()