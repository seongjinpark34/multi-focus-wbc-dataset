# A large multi-focus WBC dataset

This repository demonstrates the process of generating images that were used in the annotation from the paper "A large multi-focus WBC dataset". 


## Running the script 

```
python main.py
``` 

Running ```main.py``` will demonstrate how the processing is done. 
Every diagnosis test from miLab:tm: generates a folder with unique test name. 
In the example, ```Example_TEST``` is given to mock the directory that is generated from miLab:tm:.
Example_TEST contains sample images  and 
```anlayze_result.json``` from miLab:tm:. 
```analyze_result.json``` is a mocking CSV file that is deserialized from serialized data obtained from miLab:tm:.

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
For example, the first image that is obtained is given an index of 0 with a name starting with```0001_12345_12345_001_12345.jpg```. 