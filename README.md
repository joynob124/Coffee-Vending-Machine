# Coffee Vending Machine 

A console-based coffee vending machine simulator built in standard Python.

## Features
- Multiple drink orders with quantity
- Size (Small/Regular/Large), sugar, extra shot customization
- Resource management and low resource warning and checking
- Payment system with change
- Management secret commands for reporting and turn off the machine
- Data saving and loading

## How to Run
```bash
python main.py
``` 
## For customers
Type **start** to start ordering. 
Choose your drinks and press **0** when drink selection is completed.

## For Management
**Secret management commands**

Admin or Management type **report** -> **password** (admin123) instead of typing *start* to see the sales report and other management based tasks. 
Or,
Admin or Management type **off** instead of typing *start* to save data in **Sales Data.json** file and turn off the machine. 

Here **report** and **off** are 2 secret commands that customers won't know about. 
 
