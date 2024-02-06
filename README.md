# A large multi-focus WBC dataset

This repository demonstrates the process of generating images that were used in the annotation from the paper "A large multi-focus WBC dataset". 


## Running the script 

```
python main.py
``` 


Running ```main.py``` will demonstrate how the processing is done. 
Every diagnosis test from miLab:tm: generates a folder with unique test name. 
In the example, ```Example_TEST``` is provided to mock the directory that is generated from miLab:tm:.
Example_TEST contains sample images  and 
```anlayze_result.json``` from miLab:tm:. 
```analyze_result.json``` is a mocked CSV file deserialized from serialized data obtained from miLab:tm:.

## JSON file structure
```analyze_result.json``` contains a dictionary structure as shown below.

```json
{
  "0": { //image index
    "img_name": "0001_12345_12345_001_12345.jpg", // img name
    "cell_prediction": 
        { "0": // cell_index
            { "prediction": 5, // cell pre-classification from miLab. 0: rbc. 1: plt.
            "location": [1374, 621, 117, 102], //cell bounding box prediction from miLab.
            "focus": 5}, // focused image stack number that is determined by miLab.  
          "1": ...
        }
           
  },
  "1" : ...
```
From each slide, almost 200~300 images are obtained to image WBCs. 
For example, the first image that is obtained is given an index of 0 with a name starting with```0001_```. 
The ```img_name``` that is in the JSON structure is the name of the image that was used by miLab:tm:.
The image name contains, ```image number```, ```x coordinate```, ```y coordinate```, ```stack number```, and ```focus measure``` respectively.
The ```focus measure``` is given by miLab:tm: using its internal algorithm.
In ```cell_prediction```, there are cell indices that were identified from miLab:tm:. 
Each cell has a pre-classification class. Class of 0 means the cell is a red blood cell, while 1 means the cell is a platelet. 
Other than the two, it is considered that the cell is a white blood cell. 

## Crop cells and concatenation
As the JSON file contains the cell information, it can be used to crop each z-stack images and concatenate horizontally.
This image can be further used for the annotation.

![0.jpg](label%2FExample_TEST%2F0.jpg)

By default, the script generates ```./label``` directory, which then contains slide directories and image files of white blood cells in ascending orders. 
```label.csv``` file contains corresponding labels ```crop_index```,```test_id```,```img_num```,```cell_location```.
```label.csv``` is later used to trace back the original cells for generating the dataset. 