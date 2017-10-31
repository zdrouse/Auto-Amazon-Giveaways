# Auto-Amazon-Giveaways
Implementation for this project is currently a work-in-progress.  Issues are expected.

## Install
[Python 2.7.X](https://www.python.org/downloads/) must be installed.

After Python is installed, open `command-prompt` and use `pip` to install dependencies:

 - `pip install selenium`
 - `pip install colorama`
 - `pip install playsound`

ChromeDriver must be installed.

 - [Download latest release of ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) from Google.
 - Place the ChromeDriver in a directory that matches the path you want for the script.

Assuming `git` is installed on the local machine:

 - Open `command-prompt` and `cd` to a location/folder to save the project.
 - Perform `git clone https://github.com/zdrouse/Auto-Amazon-Giveaways`.
 - Edit this line for your own chromedriver path:  `chromedriver = webdriver.Chrome('/PATH/TO/chromedriver', chrome_options=opts)`
 	- The script needs to know where your chromedriver is installed.

## Run
 - `python give_it_away_now.py`

## Profit
![bezos](http://i.imgur.com/L8yRHGN.jpg)
