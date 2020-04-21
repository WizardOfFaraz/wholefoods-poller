# Whole Foods Delivery Slot Poller

This is a simple script that will poll the delivery slot window until a delivery slot is available.  I've only tested this on Mac OS but it should work for windows, however, Chrome is required.

# Instructions

1. Install Chrome Driver: https://chromedriver.chromium.org/
2. Clone the project.
3. In your shell, install Python requirements (```$ pip install -r requirements.txt```)
4. Run the script (```$ python whole_foods_poller.py ```)
5. A Chrome window will appear.  Login to your Amazon account, add any items to your Whole Foods cart.  Proceed to checkout as far as you can go, eventually you will see a window stating there are no delivery slots availble.  Leave the window here, the script will do the rest.
