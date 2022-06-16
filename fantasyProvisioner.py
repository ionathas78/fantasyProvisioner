import os
from random import randint

#   General Functions

##  Function for reporting change based on currency total
def makeChange(cashTotal):
    change = round(cashTotal * 100, 0)
    dollars = int(change / 100)
    change %= 100
    quarters = int(change / 25)
    change %= 25
    dimes = int(change / 10)
    change %= 10
    nickels = int(change / 5)
    change %= 5
    pennies = int(change)

    msg = ""
    if (dollars > 0):
        msg += " Dollars: " + str(dollars) + "\n"
    if (quarters > 0):
        msg += " Quarters: " + str(quarters) + "\n"
    if (dimes > 0):
        msg += " Dimes: " + str(dimes) + "\n"
    if (nickels > 0):
        msg += " Nickels: " + str(nickels) + "\n"
    if (pennies > 0):
        msg += " Pennies: " + str(pennies) + "\n"
    if (msg == ""):
        msg = " No cash"

    return msg

##  Function for multiplying currency floats
def calcPrice(unitPrice, count):
    unitCents = int(unitPrice * 100)
    totalCents = unitCents * count
    return totalCents / 100

##  Function for rolling an Abiliy Score (like Strength)
def roll4d6DropLow():
    rolls = [randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
    rollTotal = 0
    lowRoll = rolls[0]
    for currentRoll in rolls:
        if (lowRoll > currentRoll):
            lowRoll = currentRoll
        rollTotal += currentRoll
    rollTotal -= lowRoll

    return rollTotal

#   Classes
##  Class for an item in the store inventory. Does not account for stock.
class Product:
    def __init__(self, name, price, weight, notes):
        self.name = name
        self.price = price
        self.weight = weight
        self.notes = notes
    def listing(self):
        msg = self.name 
        if (self.notes != ""):
            msg += " (" + self.notes + ")"
        msg += " (" + str(self.weight) + " lbs.): $" + str(self.price)
        return msg

##  Class for an item in the user inventory.
class Gear:
    def __init__(self, name, weight, count):
        self.name = name
        self.weight = weight
        self.count = count
    def listing(self):
        msg = self.name + " x{count} ({totalWeight:.2f} lbs.)"
        return msg.format(count = self.count, totalWeight = self.weight * self.count)

##  Class for the user's character
class Customer:
    def __init__(self, name, purse, carryLimit):
        self.name = name
        self.purse = purse
        self.stuff = []
        self.carryLimit = carryLimit
    def status(self):
        msg = self.name + " has: ${cash:.2f}\n".format(cash = self.purse)
        msg += str(makeChange(self.purse))
        return msg
    def encumbrance(self):
        totalWeight = 0
        for item in self.stuff:
            totalWeight += item.weight * item.count
        return totalWeight
    def pack(self):
        msg = self.name + "'s stuff:"
        if (len(self.stuff) == 0):
            msg += "\n nada"
        else:
            carryWeight = self.encumbrance()

            msg += " ({weight:.2f} / {maxWeight:.2f} lbs.)".format(weight = carryWeight, maxWeight = self.carryLimit * 3)
            if (carryWeight > self.carryLimit * 3):
                msg += " You cannot move."
            elif (carryWeight > self.carryLimit * 2):
                msg += " Your are heavily encumbered."
            elif (carryWeight > self.carryLimit):
                msg += " You are encumbered."
                
            msg += "\n"

            for i in range(len(self.stuff)):
                item = self.stuff[i]
                msg += " " + str(i + 1) + ": " + item.listing() + "\n"
        
        return msg

#   Program Code
#   Set up the character and store inventory

startingCash = 10 * (randint(1, 4) + randint(1, 4) + randint(1, 4))
maxEncumbrance = 5 * roll4d6DropLow()
user = Customer(input("Your name: "), startingCash, maxEncumbrance)
storeInventory = [ 
    Product("Bedroll", round(15 + randint(0, 1000) / 100, 2), 7, ""),
    Product("Grappling Hook", round(10 + randint(0, 500) / 100, 2), 4, ""),
    Product("Trail Ration", round(2 + randint(0, 100) / 100, 2), 1, "1 day"),
    Product("Healing Potion", round(50 + randint(0, 2500) / 100, 2), 0.5, ""),
    Product("Soap", round(1 + randint(0, 100) / 100, 2), 0.2, ""),
    Product("Torch", round(1 + randint(0, 200) / 100, 2), 1, ""),
    Product("Candle", round(randint(0, 25) / 100, 2), 0.1, ""),
    Product("Hempen Rope", round(2 + randint(0, 250) / 100, 2), 10, "50 ft"),
    Product("Silk Rope", round(15 + randint(0, 500) / 100, 2), 5, "50 ft")
    ]

#   Display the UI

os.system("clear")
print(user.status())
print()
for i in range(len(storeInventory)):
    item = storeInventory[i]
    print(str(i + 1) + ": " + item.listing())

buyIndex = 1

#   Purchase interface loop

INDEX_ENDOFLOOP = -1
INDEX_STOREINVENTORY = 12
INDEX_USERINVENTORY = 13

while (buyIndex > 0):
    print()
    userInput = input("Buy which item (0 to end, 's' to list store stock, 'i' to list personal inventory)? ")
    
    #   See if the user entered a number or char
    try:
        buyIndex = int(userInput)
    except:
        if (userInput == ""):
            buyIndex = INDEX_ENDOFLOOP
        elif (userInput[0].lower() == 's'):
            buyIndex = INDEX_STOREINVENTORY
        elif (userInput[0].lower() == 'i'):
            buyIndex = INDEX_USERINVENTORY
        else:
            buyIndex = INDEX_ENDOFLOOP
    
    #   Process the user's response
    if (buyIndex == INDEX_STOREINVENTORY):
        print()
        print(user.status())
        print()
        for i in range(len(storeInventory)):
            item = storeInventory[i]
            print(str(i + 1) + ": " + item.listing())

    elif (buyIndex == INDEX_USERINVENTORY):
        print()
        print(user.status())
        print(user.pack())

    elif (buyIndex > 0):
        buyItem = storeInventory[buyIndex - 1]
        buyCount = int(input("How many " + buyItem.name + "s? "))

        if (buyCount < 1):
            print("Bought none of " + buyItem.name)
        
        else:
            buyGear = Gear(buyItem.name, buyItem.weight, buyCount)
            buyPrice = calcPrice(buyItem.price, buyCount)

            if (buyPrice > user.purse):
                print("Not enough cash!")
            else:
                user.purse -= buyPrice
                user.stuff.append(buyGear)
                print("Bought " + buyItem.name + " x" + str(buyCount))
    
        print(user.status())
        print(user.pack())

#   Exit code

print("Thanks for your business!")
print(user.status())
print(user.pack())
