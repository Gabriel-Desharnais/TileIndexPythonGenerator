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
def fillLayer(layer, polygon, index, fields=[]):
	# This function will be called recursively
	thisFieldName = index[0]
	
	values = index[1].values()
	if all(map(lambda x : isinstance(x,str), values)):
		# Write every feature
		for nameOfField,location in index[1].items():
			# Write every field
			feature = ogr.Feature(layer.GetLayerDefn())
			feature.SetGeometry(polygon) # Add geometry
			for fieldName, fieldValue in fields+[(thisFieldName, nameOfField)]:
				feature.SetField(fieldName,fieldValue)
			# Write the location field
			feature.SetField("LOCATION",location)
			# Add feature to layer
			layer.CreateFeature(feature)
	elif all(map(lambda x : isinstance(x,list),values)):
		# for each list apply this function
		for i in map(lambda x : fillLayer(layer, polygon, x[1], fields+[(thisFieldName,x[0])]), index[1].items()):
			pass
			# Recursive call
	else:
		raise(Exception(
			"invalid index struct not same type at the same level"))
	
def createFromListStruct(fileToCreate, index, doNotOpen=None, fieldsType=[]):
	# This function will create a new tileIndex see doc for more
	# information.
	
	## First step is to create a new file named %fileToCreate%.
	# The created tileindex will be a shapefile
	driver = ogr.GetDriverByName("ESRI Shapefile")
	# Open %fileToCreate% and allow read/write
	dataSource = driver.CreateDataSource(fileToCreate)

	## Now that we have a good editable Shapefile, we have to 
	## create a layer. This layer will be named after the name
	##  of %fileToCreate%.
	# The file name is retrieved via os.path.basename
	# The geom_type will be set to ogr.wkbPolygon
	layer = dataSource.CreateLayer(os.path.basename(fileToCreate).replace('.shp','')
					, geom_type=ogr.wkbPolygon)
	
	## Now it is time to create a default polygone that will be
	## associated with every layer. No support for doNotOpen=None
	## for now.
	# Create a ring
	ring = ogr.Geometry(ogr.wkbLinearRing)
	# Add all point to the ring
	for point in doNotOpen:
		ring.AddPoint(*point) # pass coord directly to ogr 
 	
	# Create the actual polygon from the ring
	poly = ogr.Geometry(ogr.wkbPolygon)
	poly.AddGeometry(ring)

	## Create the fields
	# Get info on the fields
	fieldsInfo = getFieldInfoFromIndex(index)
	index = 0
	for name, maxLenght in fieldsInfo.items():
		# Add each fields
		# Create field definition
		if not (fieldsType == []) and fieldsType[index] == "int":
			id = ogr.FieldDefn(name, ogr.OFTInteger)
		else:
			id = ogr.FieldDefn(name, ogr.OFTString)
			# Set width
			id.SetWidth(min(maxLenght,254))
			# Add field to layer
		layer.CreateField(id)
		index += 1
	
	# Fill the layer with the features
	fillLayer(layer,poly,index)
	
	# Close dataSource
	dataSource.Destroy() # Close shapefile
