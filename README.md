# TileIndexPythonGenerator
This python package will enable you to generate a shapefile TileIndex for MapServer. This TileIndex can be generated for any number of dimension.

## Installation
Install via  pip `pip install tileIndexPythonGenerator`

### Requirements

- python3
- gdal/ogr
- python3 gdal/ogr package

## User Manual
### Creating a TileIndex
To create a TileIndex you will call the function `tileIndexPythonGenerator.createFromListStruct(fileToCreate,index,doNotOpen=geometry)`.
Where:

| Parameter | Type | Default value | Mandatory | Meaning |
|---------- | ---- | ------------- | --------- | ------- |
| fileToCreate | str |  | Yes | This is the complete path where the tileindex will be created the layer name will be the name of the file. The file must not already exist or else a fileAlreadyExists exception will be thrown. |
| index | list of dict | Yes |  | This is a python list *r.f.* [Index structure](#Index_structure) section. |
| doNotOpen | list | No | None | This will ask this function to skip the step where it open every file to catch the geometry of the data. doNotOpen is simply a list of point (tuple) **Default value not working, list mandatory** |

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

LTS : Long Term Support

DS : Developer Support

Names are choosen from:
[https://en.wikipedia.org/wiki/List_of_named_passenger_trains_of_Canada](https://en.wikipedia.org/wiki/List_of_named_passenger_trains_of_Canada)
