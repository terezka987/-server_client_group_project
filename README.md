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
This application can be used as the server or the client    
It should be run from the repository directory. e.g. ~/server_client_group_project   

# Server    
- Will stay running until it receives a stop message (Option 5 for Client)
- Once started will print to screen or file as selected in the command line   
- Will prompt for password if a encrypted message is received  
- If in file mode, the files with prefix 'received_message' will be saved to repository directory   
    
# Client   
- Can complete one option when run     
- Once started will present options     
    1. Save unencrypted text file to repository directory and send to server   
    2. Create a dictionary in bytes   
    3. Create a dictionary in JSON   
    4. Create a dictionary in XML   
    5. Stop Server   
- Options 2,3,4 will prompt if the contents should be encrypted, if yes a password will be required



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
