## name 15/3/24
server_client_group_project, creates server-client connection used to send basic, preset data 

## description 15/3/24
Contains two main components, the server and client
There are several files containing supporting code and tests

The entry point is main.py, can be run from the same directory as this README.md

```
python3 main.py -help: options
```
```
python3 main.py -sos: starts server and will print to screen
```
```
python3 main.py -sof: starts server and will print to file
```
```
python3 main.py -c: starts client
```


## visualisation

## usage
This application can be used as the server or the client \n



## requirements
python3
install requirements with: 
```
pip3 install -r requirements.txt
```

## support
Please contact sgpclar2@liverpool.ac.uk for issues with product   
Please contact t.gonsiorova@liverpool.ac.uk for issues with unit tests    
Please contact y.han51@liverpool.ac.uk for issues with performance tests    

## roadmap
Support use on different machines
Allow custom data entry

## testing
to run the tests:
```
python3 -m unittest tests/unit_tests.py
```

### Coverage
to run tests with coverage run:
```
python3 -m coverage run tests/unit_tests.py
```
to see current coverage run:
```
python3 -m coverage report -m     
```

### Contributing
Contact support if you have suggestions
Project uses autopep8 to format
