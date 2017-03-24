from selenium import webdriver
import time
import logging
import os
import sys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

SLEEP_TIME = 0 #This is used to slow the transaction entry speed for visual confirmaton and debugging.
STATEMENT = "072016.bccStatement.txt"
MINT_START_PAGE = "https://mint.intuit.com/login.event?task=L&messageId=6&country=US&nextPage=overview.event"
TIMEOUT = 30
logFile = "transactionEntryEngine.log"
USERID = "jonathan.kopp@gmail.com"
PW = "gunther13"
GECKODRIVER_PATH = "/Users/jkopp/git/myWorkspace/scripts/mint/"

# create logger
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
try:
    os.remove(logFile)
except OSError:
    pass
global logger
logging.basicConfig(filename=logFile, format=FORMAT, level=logging.DEBUG)
logger = logging.getLogger('transactionEntryEngine')


class TransactionEntryEngine():
    restaurantCategory = ["Terrace Food",
                          "Terrace Beverage",
                          "Terrace Wine",
                          "Terrace Beer",
                          "Fireside Food",
                          "Fireside Beverage",
                          "Fireside Wine",
                          "Fireside Beer",
                          "Club Function beer"
                          ]
    fastFoodCategory = ["Snack Bar Food",
                        "Snack Bar Bev",
                        "Athletic Center F & B"
                        ]
    entertainCategory = ["Pool guest outdoor"]
    massageCategory = ["Massage/SkinCare Fees",
                       "Massage/SkinCare Tips"
                       ]
    tennisCategory = ["Adult Tennis Clinic",
                      "Adult Tennis Mixer",
                      "Semi Private Tennis",
                      "USTA League Fee",
                      "CTA Daytime Dbl's",
                      "USTA 40+",
                      "CTA Twilight",
                      "Pct Balls",
                      "Permanent Court Time",
                      "Private Tns Lessons"
                      ]
    sportsEquipCategory = ["Demo Racket Fees",
                   "Golf Mdse Sales",
                   "Stringing",
                   "Athletic Center Merchandi"
                   ]
    sportsCategory = ["Golf Cart Rental",
                      "Greens Fees",
                      "Golf Lessons"
                      ]
    duesCategory = ["Accrue Monthly Dues",
                    "Par3 Capital Fee",
                    "Holiday Bonus"
                    ]
    kidsActivityCategory = ["Jr Group Tennis",
                            "Junior Golf",
                            "Summer Jr Tennis"
                            ]
    gymCatagory = ["Personal Training"]



    def __init__(self):
        # create a new Firefox session and navigate to Mint Cash Account
        self.driver = webdriver.Firefox(executable_path=r'/Users/jkopp/Documents/geckodriver')
        self.driver.maximize_window()
        logger.debug("Driver loading webpage: " + MINT_START_PAGE)
        self.driver.get(MINT_START_PAGE)


        field = self.wait("ius-userid")
        field.clear()
        logger.debug("Logging on to mint with USERID: " + USERID)
        field.send_keys(USERID)
        field = self.driver.find_element_by_id("ius-password")
        field.clear()
        field.send_keys(PW)
        self.driver.find_element_by_id("ius-sign-in-submit-btn").click()
        try:
            element_present = EC.presence_of_element_located((By.LINK_TEXT, "Transactions"))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            logger.debug("Found Transactions")
        except TimeoutException:
            logger.error("Could not find Transactions")
            sys.exit()
        self.driver.find_element_by_link_text("Transactions").click()
        time.sleep(5)
        self.driver.find_element_by_link_text("Cash Only").click()
        time.sleep(5)

    def enterTransaction(self, date, description, catagory, amount):
        self.driver.find_element_by_id("controls-add").click()
        time.sleep(SLEEP_TIME)
        field = self.wait("txnEdit-date-input")
        field.clear()
        field.send_keys(date)
        logger.debug("Entering date: " + date)
        time.sleep(SLEEP_TIME)
        field = self.driver.find_element_by_id("txnEdit-merchant_input")
        field.clear()
        field.send_keys("BCC - " + description)
        logger.debug("Entering description: " + description)
        time.sleep(SLEEP_TIME)
        field = self.driver.find_element_by_id("txnEdit-category_input")
        field.clear()
        field.send_keys(catagory + "\n")
        logger.debug("Entering catagory: " + catagory)
        time.sleep(SLEEP_TIME)
        field = self.driver.find_element_by_id("txnEdit-amount_input")
        field.clear()
        field.send_keys(amount)
        logger.debug("Entering amount: " + amount)
        time.sleep(SLEEP_TIME)
        self.driver.find_element_by_id("txnEdit-submit").click()
        time.sleep(3) # This is needed to give time for transaction to save so "+ Transaction" can be clicked.


    def wait(self, id):
        try:
            element_present = EC.presence_of_element_located((By.ID, id))
            WebDriverWait(self.driver, TIMEOUT).until(element_present)
            logger.debug("Found " + id)
        except TimeoutException:
            logger.error("Could not find " + id)
            sys.exit()
        return self.driver.find_element_by_id(id)

    def quit(self):
        self.driver.quit()

    def getCategory(self, desc):
        if desc in self.restaurantCategory:
            cat = "Restaurants"
        elif desc in self.fastFoodCategory:
            cat = "Fast Food"
        elif desc in self.entertainCategory:
            cat = "Entertainment"
        elif desc in self.massageCategory:
            cat = "Spa & Massage"
        elif desc in self.tennisCategory:
            cat = "Tennis"
        elif desc in self.sportsEquipCategory:
            cat = "Sports Equipment"
        elif desc in self.sportsCategory:
            cat = "Sports"
        elif desc in self.duesCategory:
            cat = "BCC Fee"
        elif desc in self.kidsActivityCategory:
            cat = "Kids Activities"
        elif desc in self.gymCatagory:
            cat = "Gym"
        else:
            cat = "Uncategorized"

        return cat



def parseStatement():
    with open(STATEMENT) as f:
        content = f.readlines()
    logger.debug("Starting TransactionEntryEngine")
    engine = TransactionEntryEngine()
    for line in content:
        if "Balance Forward" in line or "Payment" in line:
            continue
        elements = line.split("\t")
        date = elements[0]
        description = elements[3].strip()
        category = engine.getCategory(description)
        amount = elements[8].rstrip('\r\n')
        engine.enterTransaction(date, description, category, amount)
        print date + "\t: " + description + "\t: " + category + "\t: " + amount

    print "Import complete."


if __name__ == "__main__":
    logger.debug("Stating main")
    parseStatement()

