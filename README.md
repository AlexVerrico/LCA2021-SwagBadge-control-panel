# #LCA2021 SwagBadge Web Control Panel

A basic control panel for your Linux Conference Australia 2021 SwagBadge.
The included basic web interface allows you to clear the screen and push text to the screen.

The API also allows you to do everything that can be done through the web interface as well as turn individual pixels on.

It communicates with the badge over MQTT and is designed to work with the stock firmware/code on the badge. 

---
### Setup Instructions:
You need to have Python 3.6 or higher with pip, git, and SQLite3 installed on your system.  
Clone the repository: `git clone https://github.com/AlexVerrico/LCA2021-SwagBadge-control-panel.git && cd LCA2021-SwagBadge-control-panel`  
Install the requirements: `pip3 install -r requirements.txt`  
Rename the file `default.env` to `.env` and set the values inside it to match your setup.  
Rename the file `default.sqlite` to `main.sqlite` and add a username and password to the table `auth` in the database.  
Run the program using `python app.py`  
The server should now be running, to access it navigate to the port and IP address that you are running it on.  

  ---
  
#### Note: 
As of 24/1/21 an update for the swagbadge has being released (v05), which adds a "time since reset" timer to the screen.   
While strictly speaking this doesn't interfere with this project, it does produce some interesting side effects.  
To prevent these side-effects, you can disable this timer by editing the file `/applications/swagbadge.py` and changing these lines:
```python
def swagbadge_handler():
    global timer
    hours, minutes, seconds = convert_time(timer)
    timer += 1
    text = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    screen = aiko.oled.oleds[0]
    screen.fill_rect(0, 16, 128, 8, 0)
    screen.text(text, 0, 16)
    screen.show()
```
to this:
```python
def swagbadge_handler():
    # global timer
    # hours, minutes, seconds = convert_time(timer)
    # timer += 1
    # text = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    # screen = aiko.oled.oleds[0]
    # screen.fill_rect(0, 16, 128, 8, 0)
    # screen.text(text, 0, 16)
    # screen.show()
    pass
```
