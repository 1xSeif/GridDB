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
    factory = griddb.StoreFactory.get_instance()
    gridstore = factory.get_store(
        notification_member = "127.0.0.1:10001",
        cluster_name = "myCluster",
        username = "admin",
        password = "admin"
    )


    container = griddb.ContainerInfo("CreditCard",
                                             [["id", griddb.Type.INTEGER],
                                              ["cardNumber", griddb.Type.BLOB],
                                              ["expirationDate", griddb.Type.STRING],
                                              ["ownerName", griddb.Type.STRING]],
                                             griddb.ContainerType.COLLECTION, True
                                             )
    container = gridstore.put_container(container)
    
    # Example encryption key
    encryptionKey = b'1324151512412414'  # 16 bytes key for AES-128
    
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
        container.put([cardId, encryptedCardNumber,expirationDate, ownerName])
    
        # Retrieve Encrypted Data from GridDB Container
        query = container.query("SELECT * FROM CreditCard")
        rs = query.fetch()
        while rs.has_next():
            row = rs.next()
            decryptedCardNumber = decrypt_data(encryptionKey, row[1])
            if decryptedCardNumber:
                print("Decrypted Credit Card Number:", decryptedCardNumber)
                print("Expiration Date:", row[2])
                print("Owner Name:", row[3])
    else:
        print("Failed to encrypt the credit card number")

except griddb.GSException as e:
    for i in range(e.get_error_stack_size()):
        print("[", i, "]")
        print(e.get_error_code(i))
        print(e.get_location(i))
        print(e.get_message(i))
