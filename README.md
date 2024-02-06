# A large multi-focus WBC dataset

This repository demonstrates the generation process of multi-focal white blood cell images provided from the paper "A large multi-focus WBC dataset". 


## Running the script 

```
python main.py  --test_dir ./examples/miLab_test
``` 
This script will generate a same directory under ```./tidy_data``` that contains the cropped and concatenated images of white blood cells.

## Test input directory
Every diagnosis test from miLab:tm: generates a folder with a unique test name. 
Under the examples, ```miLab_test``` is provided to mock the directory that is generated from miLab:tm:.
It contains a multiple stacks of focal planes for a sample FoV image and 
```anlayze_result.json``` from miLab:tm:. 
Note that ```analyze_result.json``` is a metadata deserialized from serialized data obtained from miLab:tm:.

### JSON metadata in detail
For example, ```analyze_result.json``` contains a dictionary structure as shown below.

```json
{
  "0": { //image index
    "img_name": "0001_12345_12345_001_12345.jpg", // img name
    "cell_prediction": 
        { "0": // cell_index
            { "prediction": 5, // cell pre-classification index from miLab. 
            "location": [1374, 621, 117, 102], //cell bounding box prediction from miLab.
            "focus": 5}, // focused image stack number that is determined by miLab.  
          "1": ...
        }
           
  },
  "1" : ...
```
In general, almost 200~300 images are obtained to image WBCs in each slide. 
The first image that is obtained is given an index of 0 with a name starting with```0001_```. 
The ```img_name``` that is in the JSON structure is the name of the image that was used by miLab:tm:.
The image name contains, ```image number```, ```x coordinate```, ```y coordinate```, ```stack number```, and ```focus measure``` respectively.
The ```focus measure``` is given by miLab:tm: using its internal algorithm.
In ```cell_prediction```, cell indices were identified from miLab:tm:. 
Each cell has a pre-classification class. Class of 0 means the cell is a red blood cell, while 1 means the cell is a platelet. 
Other than the two, the cell is considered a subtype of white blood cells.

## Data generation process
As the above file contains the cell information, it can be used to crop each z-stack image and concatenate horizontally. 

See the ```process.py``` for the details.

## Data output
By default, the script generates a directory under ```./tidy_data```, which then contains slide directories and image files of white blood cells in ascending orders. 
```labels.csv``` file contains corresponding labels ```crop_index```,```test_id```,```img_num```,```cell_location```.
```labels.csv``` is later used to trace back the original cells for generating the dataset. 
While this multi-focal image had been used for the annotation, the open dataset was organized as the cropped one such as ```0_0```, ```0_1```, ..., ```0_9```.
