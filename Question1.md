# Title
How do you correctly use the TIMESTAMP Data Type in GridDB with Python for the Credit Card Expiry Date?

# Problem
I'm currently developing a Python application that stores encrypted credit card information in GridDB. I'm attempting to use the TIMESTAMP data type to store the credit card expiration date instead of a STRING. However, I'm facing errors when I try to implement TIMESTAMP for the expiration date. My current code works with the expiration date as a STRING, but it fails when I attempt to switch to TIMESTAMP.

# What did you try and what were you expecting?
I modified the column definition for 'expirationDate' to use 'griddb.Type.TIMESTAMP' instead of 'griddb.Type.STRING'. I also tried to convert the expiration date into a Python 'datetime' object before inserting it into the GridDB container. I expected the data to be stored without issues and to be able to query it. However, I keep getting errors related to the data type, and I'm unsure how to properly format or handle the 'TIMESTAMP' data in this context."

Below is my code:
```
import datetime

# Attempt to store expirationDate as a TIMESTAMP
expirationDate = datetime.datetime(2028, 12, 1)
container = griddb.ContainerInfo("CreditCard",
                                 [["id", griddb.Type.INTEGER],
                                  ["cardNumber", griddb.Type.BLOB],
                                  ["expirationDate", griddb.Type.TIMESTAMP],
                                  ["ownerName", griddb.Type.STRING]],
                                 griddb.ContainerType.COLLECTION, True)
container.put([cardId, encryptedCardNumber, expirationDate, ownerName])
```

Tags: GridDB, Python
