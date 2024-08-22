import griddb_python as griddb
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# AES Encryption and Decryption Functions
def encrypt_data(key, plaintext):
    try:
        # Create a new AES cipher object in CBC mode with the given key
        cipher = AES.new(key, AES.MODE_CBC)
        # Pad the plaintext and encrypt it
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        # Combine the IV and the ciphertext, then encode it in base64
        return base64.b64encode(cipher.iv + ciphertext).decode('utf-8')
    except Exception as e:
        # Handle encryption errors
        print("Encryption failed:", e)
        return None

def decrypt_data(key, ciphertext):
    try:
        # Decode the base64 encoded ciphertext
        ciphertext = base64.b64decode(ciphertext)
        # Extract the IV from the beginning of the ciphertext
        iv = ciphertext[:AES.block_size]
        # Create a new AES cipher object in CBC mode with the key and IV
        cipher = AES.new(key, AES.MODE_CBC, iv)
        # Decrypt the ciphertext and unpad it to get the plaintext
        plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
        return plaintext.decode('utf-8')
    except Exception as e:
        # Handle decryption errors
        print("Decryption failed:", e)
        return None

try:
    # Connect to GridDB
    factory = griddb.StoreFactory.get_instance()
    gridstore = factory.get_store(
        notification_member = "127.0.0.1:10001",  # Notification member (GridDB node address and port)
        cluster_name = "myCluster",  # Cluster name
        username = "admin",  # Username
        password = "admin"   # Password
    )

    # Define the GridDB container schema
    container = griddb.ContainerInfo("CreditCard",
                                     [["id", griddb.Type.INTEGER],        # Column 1: id (INTEGER)
                                      ["cardNumber", griddb.Type.BLOB],   # Column 2: cardNumber (BLOB)
                                      ["expirationDate", griddb.Type.STRING],  # Column 3: expirationDate (STRING)
                                      ["ownerName", griddb.Type.STRING]],  # Column 4: ownerName (STRING)
                                     griddb.ContainerType.COLLECTION, True)  # Container type: Collection (row-key)
    container = gridstore.put_container(container)  # Create the container in GridDB
    
    # Example encryption key (16 bytes key for AES-128)
    encryptionKey = b'1324151512412414'
    
    # Example data
    cardId = 1
    creditCardNumber = "4731324241234123"
    expirationDate = "12/2028"
    ownerName = "Saif Eddine"

    # Encrypt Data using AES
    encryptedCardNumber = encrypt_data(encryptionKey, creditCardNumber)
    print("Encrypted Credit Card Number:", encryptedCardNumber)
    
    if encryptedCardNumber:
        # Store Encrypted Data in GridDB Container
        container.put([cardId, encryptedCardNumber, expirationDate, ownerName])
    
        # Retrieve Encrypted Data from GridDB Container
        query = container.query("SELECT * FROM CreditCard")
        rs = query.fetch()
        while rs.has_next():
            row = rs.next()  # Get the next row of the query result
            decryptedCardNumber = decrypt_data(encryptionKey, row[1])
            if decryptedCardNumber:
                # Print the decrypted card number along with other details
                print("Decrypted Credit Card Number:", decryptedCardNumber)
                print("Expiration Date:", row[2])
                print("Owner Name:", row[3])
    else:
        print("Failed to encrypt the credit card number")

except griddb.GSException as e:
    # Handle GridDB exceptions
    for i in range(e.get_error_stack_size()):
        print("[", i, "]")
        print(e.get_error_code(i))
        print(e.get_location(i))
        print(e.get_message(i))
