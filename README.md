# TileIndexPythonGenerator
This python package will enable you to generate a shapefile TileIndex for MapServer. This TileIndex can be generated for any number of dimension.

## Installation
Install via  pip `pip install tileIndexPythonGenerator`

### Requirements

- python3
- gdal/ogr
- python3 gdal/ogr package

## User Manual
### Creating a TileIndex from listStruct
To create a TileIndex you will call the function `tileIndexPythonGenerator.createFromListStruct(fileToCreate,index,doNotOpen=geometry)`.
Where:

| Parameter | Type | Default value | Mandatory | Meaning |
|---------- | ---- | ------------- | --------- | ------- |
| fileToCreate | str |  | Yes | This is the complete path where the tileindex will be created the layer name will be the name of the file. The file must not already exist or else a fileAlreadyExists exception will be thrown. |
| index | list of dict | Yes |  | This is a python list *r.f.* [Index structure](#Index_structure) section. |
| doNotOpen | list | No | None | This will ask this function to skip the step where it open every file to catch the geometry of the data. doNotOpen is simply a list of point (tuple) **Default value not working, list mandatory** |
### Creating a TileIndex with an object
You can create an tileIndex object that will allow you to add one feature at a time. You can use the function `create` to declare a new tileIndex object.
`tileIndexPythonGenerator.create(fileToCreate, fields, polygon)`
| Parameter | Type | Default value | Mandatory | Meaning |
|---------- | ---- | ------------- | --------- | ------- |
| fileToCreate | str |  | Yes | This is the complete path where the tileindex will be created the layer name will be the name of the file. The file must not already exist or else a fileAlreadyExists exception will be thrown. |
| fields | list |  | Yes | This field must contain a tuple for every field in shapefile. The first element of the tuple is the name of the field, the second one is the len of the string (can't be more than 254). |
| polygon | list |  | Yes | polygon is simply a list of point (tuple) |
#### Index structure
For a no dimension, the python list must be organised this way:
**Not Yet implemented**
``` python
[path0, ... pathN]
```
This will map to a shapefile organised this way:

| LOCATION |
| -------- |
| path0 |
...
| pathN |

For multiple dimensions, the python dictionary must be organised this way:
``` python
["dim_1",{
	label1_0:[
		"dim_2",{
			"label2_0":"path0_0",
			...
			"label2_N":"path0_N"}
		],
	....
	"label1_M":[
		"dim_2",{
			"label2_0":"pathM_0",
			...
			"label2_N":"pathM_N"}
		]
	}
]
```
This will map to a shapefile organised this way:

| DIM_1 | DIM_2 | LOCATION |
| ----- | ----- | -------- |
| label1_0 | label2_0 | path0_0 |
| label1_0 |    ...   |    ...  |
| label1_0 | label2_N | path0_N |
|    ...   |    ...   |   ...   |
| label1_M | label2_0 | pathM_0 |
| label1_M |    ...   |    ...  |
| label1_M | label2_M | path0_M |

#### Example

``` python
index = ["dim_1",{"label1_0":["dim_2",{"label2_0":"path0_0","label2_N":"path0_N"}],"label1_M":["dim_2",{"label2_0":"pathM_0","label2_N":"pathM_N"}]}]
fileToCreate = "index.shp"
tipg.createFromListStruct(fileToCreate, index, doNotOpen=[(180,90),(180,-90),(-180,-90),(-180,90)])
```

#### Fields list structure
``` python
import tileIndexPythonGenerator as tipg
fields = [(fieldName1, 23), (fieldName2, 230), ("location", 254 )]
polygon = [(180,90),(180,-90),(-180,-90),(-180,90)]
tIndex = tipg.create("fileName.shp", fields, polygon)

tIndex.add([(fieldName1, value1), (fieldName2, value1)], pathToData)
# Close the tIndex
tIndex.close()
```

To test the result:
`ogrinfo -al -geom=yes index.shp`
## Limitation
Remember: shapefile can't be more than 4 Gb.

Remenber: shapefile can't have more than 254 char in a string.

## Developer note
All variable, functions, etc. are named using **pascal case** (also known as **camel case**). *i.e.* name will always begin by a lower case letter and upper case letter will be used to separate letter.

No space will be used to do indention in programs **tab** shall be used instead.

Some care will be put in readability of the code but the number one priority is for the code to be as efficient as it can.

## Support
There is limited support for these version

| version | name | type | End of support date |
| -- | -- | -- | -- |
| 0.0.0.3 | Atlantic Express | DS | 2018-08-01T00:00:00Z |
| 0.0.0.5 | Adirondack | LTS | 2020-08-01T00:00:00Z |
| 1.0.0.0 | Acadian | ULTS | 2040-01-01T00:00:00Z |

LTS : Long Term Support

DS : Developer Support

ULTS : Ultra long term support

DS support is really short term it should be used in two scenarios

- You need new features not available in the latest LTS
- You are develloping an application that will be operational only after the next projected LTS puplishement.

DS is minimal it mostly should be considered as beta testing.

LTS is generaly supported for anything from 2 to 5 years. You should use it for your operational project. The pip repo default version will always be a LTS.

ULTS is generaly supported for at least 15 years. This version can be downloaded via pip by giving the right version number. ULTS should be used for incredibly stable systems. Systems that requires to be runed for years without any change.

version numbering is done this way:
```
0.0.0.0
| | | |---Update number changes every time an update is done
| | |-----DS number
| |-------LTS number
|---------ULTS number
```
Support means that no functionnality will be added to the software, but that any bug or vulnerabilities will be patched as long as the devellopers can do it. If you want vendor support (paid support to solve bug or even add new functionnality or improve the software) please contact [gabriel.desharnais@hotmail.com](gabriel.desharnais@hotmail.com).

Names are choosen from:
[https://en.wikipedia.org/wiki/List_of_named_passenger_trains_of_Canada](https://en.wikipedia.org/wiki/List_of_named_passenger_trains_of_Canada)
