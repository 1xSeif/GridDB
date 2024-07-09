import griddb_python as griddb
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

# AES Encryption and Decryption Functions
def encrypt_data(key, plaintext):
    try:
        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(plaintext.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + ciphertext).decode('utf-8')
    except Exception as e:
        print("Encryption failed:", e)
        return None

def decrypt_data(key, ciphertext):
    try:
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
        return plaintext.decode('utf-8')
    except Exception as e:
        print("Decryption failed:", e)
        return None

try:
    # Connect to GridDB
    try:
        factory = griddb.StoreFactory.get_instance()
        gridstore = factory.get_store(
                host="127.0.0.1",
                port=41189,
                cluster_name="myCluster",
                username="admin",
                password="admin"
            )
    except griddb.GSException as e:
        print("Failed to connect to GridDB:", e)
        gridstore = None

    if gridstore:
        # Define Data Schema in Python with GridDB
        # Example: Encrypting sensitive information such as credit card numbers
        containerInfo = griddb.ContainerInfo("CreditCards",
                                             [["id", griddb.Type.INTEGER],
                                              ["cardNumber", griddb.Type.BLOB],
                                              ["expirationDate", griddb.Type.TIMESTAMP],
                                              ["ownerName", griddb.Type.STRING]],
                                             griddb.ContainerType.COLLECTION, True)
        container = gridstore.put_container(containerInfo)
        
        # Example encryption key
        encryptionKey = b'This is a key123'  # 16 bytes key for AES-128
        
        # Example data
        cardId = 1
        creditCardNumber = "1234567812345678"
        expirationDate = griddb.Timestamp(2024, 12, 31)
        ownerName = "Saif Eddine"
        
        # Encrypt Data using AES
        encryptedCardNumber = encrypt_data(encryptionKey, creditCardNumber)
        
        if encryptedCardNumber:
            # Store Encrypted Data in GridDB Container
            container.put([cardId, encryptedCardNumber, expirationDate, ownerName])
        
            # Retrieve Encrypted Data from GridDB Container
            query = container.query("SELECT * FROM CreditCards")
            rs = query.fetch()
            while rs.has_next():
                row = rs.next()
                decryptedCardNumber = decrypt_data(encryptionKey, row[1])
                if decryptedCardNumber:
                    print("Decrypted Credit Card Number:", decryptedCardNumber)
        else:
            print("Failed to encrypt the credit card number")
except griddb.GSException as e:
    print("GridDB operation failed:", e)
except Exception as e:
    print("An unexpected error occurred:", e)
