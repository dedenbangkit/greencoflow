## Pre-Installation
- Conda or Miniconda, see [Conda Docs](https://conda.io/docs/)
- NodeJS v7 or above, see [NodeJS Docs](https://nodejs.org/en/)

## Configuration File
mail to [deden@akvo.org](mailto:deden@akvo.org) to get the configuration file.

## Installation
```
// clone source
$ git clone https://github.com/dedenbangkit/greencoflow

// install environment
$ conda env create -f green-coffee.yml

```

## Usage 
```
// start the app 
$ sh run.sh 
* Running on http://127.0.0.1:5000
* type $ sh kill.sh to stop the program

// stop the app 
$ sh kill.sh 
* Stopping the program
```

## List of Endpoint
```
// Show folders
$ curl http://127.0.0.1:5000/folders
$ curl http://127.0.0.1:5000/folder/<FOLDER_ID>

// Show survey
$ curl http://127.0.0.1:5000/survey/<SURVEY_ID>

// Show Datapoint 
$ curl http://127.0.0.1:5000/datapoint/<DATAPOINT_ID>

// Post Data
$ curl http://127.0.0.1:5000/collections/<SURVEY_ID>/<FORM_ID>
  {
    "device": "Greencoffee - XXX",
    "id": "24450005",
    "identifier": "tb41-n8v1-1hva",
    "login": {
      "id": "XXX",
      "name": "XXX",
      "pass": "XXX"
    },
    "payload": "keymd5=c946415addc376cc50c91956a51823f1&ACC_ID=231&Date_var=12%2F07%2F2018&ID_Commodity=14&ID_Agency=21&min_price=89898.0&max_price=66666.0",
    "response": "<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<string xmlns=\"http://tempuri.org/\">28226</string>",
    "submited_at": "2018-07-11T18:14:00Z",
    "submitter": "admin"
  }
 
// Download Data 
$ curl http://127.0.0.1:5000/download/<SURVEY_ID>/

// Add Price 
$ curl http://127.0.0.1:5000/addprice/

```
...on progress
