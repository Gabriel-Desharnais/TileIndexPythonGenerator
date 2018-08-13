#! /usr/bin/python3

# Copyright (c) Gabriel Desharnais July 2018
# Copyright (c) Government of Canada July 2018

import ogr
import os

def getFieldInfoFromIndex(index):
	# This function returns a dictionary containing as key the
	# fields and as values the max lenght contaign by the field

	## The first step is to define a recursive function that
	## will keep the max len of the strings and the names of
	## dimmentions.

	# declare the dictionary that will store the dimentions
	fields = {}
	def fields_info(index, fields):
		# This function will fill the maximum and name of
		# fields in the fields dict.

		# Get all labels of this dimension and look for max len
		keys = index[1].keys()
		try:
			fields[index[0]] = max( max(map(len,keys)),
						fields[index[0]] )
		except KeyError:
			fields[index[0]] = max(map(len,keys))

		# look if values are all of type dict or all of type
		# str if not issue error
		values = index[1].values()
		if all(map(lambda x : isinstance(x,str),values)):
			# Check lenght of string
			try:
				fields["LOCATION"] = max( max(map(len,values)),
							fields["LOCATION"] )
			except KeyError:
				fields["LOCATION"] = max(map(len,values))
		elif all(map(lambda x : isinstance(x,list),values)):
			# for each list apply this function
			for i in map(lambda x : fields_info(x,fields),values):
				pass

		else:
			raise(Exception(
			"invalid index struct not same type at the same level"))
	fields_info(index,fields)
	return fields
def fillLayer(tIndex, index, fields=[]):
	# This function will be called recursively

	thisFieldName = index[0]

	values = index[1].values()
	if all(map(lambda x : isinstance(x,str), values)):
		# Write every feature
		for nameOfField,location in index[1].items():
			tIndex.add(fields+[(thisFieldName, nameOfField)], location)

	elif all(map(lambda x : isinstance(x,list),values)):
		# for each list apply this function
		for i in map(lambda x : fillLayer(tIndex, x[1], fields+[(thisFieldName,x[0])]), index[1].items()):
			pass
			# Recursive call
	else:
		raise(Exception(
			"invalid index struct not same type at the same level"))

def createFromListStruct(fileToCreate, index, doNotOpen=None, fieldsType=[]):
	# This function will create a new tileIndex see doc for more
	# information.

	# Get fields name and lenght
	fieldsInfo = getFieldInfoFromIndex(index)

	# Create a layer object
	tIndex = tileIndex(fileToCreate, fieldsInfo.items(), doNotOpen)

	# Fill the layer with the features
	fillLayer(tIndex, index)



class tileIndex:
	# This class defines an object to create and manipulate a tileIndex
	def __init__(self, fileToCreate, fields, polygon):
		# This will create the tileIndex file
		## First step is to create a new file named %fileToCreate%.
		# The created tileindex will be a shapefile
		driver = ogr.GetDriverByName("ESRI Shapefile")
		# Open %fileToCreate% and allow read/write
		self.dataSource = driver.CreateDataSource(fileToCreate)

		## Now that we have a good editable Shapefile, we have to
		## create a layer. This layer will be named after the name
		##  of %fileToCreate%.
		# The file name is retrieved via os.path.basename
		# The geom_type will be set to ogr.wkbPolygon
		self.layer = self.dataSource.CreateLayer(os.path.basename(fileToCreate).replace('.shp','')
					, geom_type=ogr.wkbPolygon)
		## Now it is time to create a default polygone that will be
		## associated with every layer. No support for polygon=None
		## for now.
		# Create a ring
		ring = ogr.Geometry(ogr.wkbLinearRing)
		# Add all point to the ring
		for point in polygon:
			ring.AddPoint(*point) # pass coord directly to ogr

		# Create the actual polygon from the ring
		self.poly = ogr.Geometry(ogr.wkbPolygon)
		self.poly.AddGeometry(ring)

		## Create the fields
		for name, maxLenght in fields:
			# Add each fields
			# Create field definition

			id = ogr.FieldDefn(name, ogr.OFTString)
			# Set width
			id.SetWidth(min(maxLenght,254))
			# Add field to layer
			self.layer.CreateField(id)

	def add(self, fields, location):
		# This function will add a feature in the layer
		# Write every field
		feature = ogr.Feature(self.layer.GetLayerDefn())
		feature.SetGeometry(self.poly) # Add geometry
		for fieldName, fieldValue in fields:
			feature.SetField(fieldName,fieldValue)
		# Write the location field
		feature.SetField("LOCATION",location)
		# Add feature to layer
		self.layer.CreateFeature(feature)

	def close(self):
		# This function will close the layer file.
		self.dataSource.Destroy() # Close shapefile

class tileIndexes:
	def __init__(self, fileToCreate, fieldsInPath , fieldsInTile, polygon):
		# This will create the tileIndex object that create multiple tileindexes files
		self.fileToCreate = fileToCreate
		self.fieldsInPath = fieldsInPath
		self.fieldsInTile = fieldsInTile
		self.polygon = polygon
		self.tileIndexes = {}
		# Create an empty set for every field available
		self.values = {}
		for field in fieldsInPath:
			self.values[field] = set()

		for field, len in fieldsInTile:
			self.values[field] = set()
	def add(self, fields, location):
		# This function add info to the right tileIndex
		# Save info in values variable
		for field, value in fields.items():
			self.values[field].add(value)
		# Create the key tuple
		key = tuple([fields[x] for x in self.fieldsInPath])
		try:
			self.tileIndexes[key]
		except KeyError:
			self.tileIndexes[key] = tileIndex(self.fileToCreate.format(**fields), self.fieldsInTile, self.polygon)
		for fieldsToDelete in self.fieldsInPath:
			del fields[fieldsToDelete]

		self.tileIndexes[key].add(fields.items(), location)

	def max(self, field):
		# This function will return the maximum value of a dimension
		return max(self.values[field])

	def min(self, field):
		# This function will return the minimum value of a dimension
		return min(self.values[field])

	def close(self):
		# Close all files
		for tile in self.tileIndexes.values():
			tile.close()
