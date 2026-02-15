import bcrypt
from database.DbManager import Create, Read, Update, Delete



def Passwordhash(password):

    PasswordBytes = password.encode('utf-8')
    # Changes password from character to byte string. This is needed for bcrypt to hash the password

    # pseudorandom string which will be attached to the password before hashing for security
    salt = bcrypt.gensalt()

    # Hashing the password
    hashedPassword = bcrypt.hashpw(PasswordBytes, salt)
    return hashedPassword.decode('utf-8')#returns a string version of the hashed password that can be stored in the database


def login(connection, email, password):
    try:
        UserCredentials = Read(connection, 'users', {'email': email})# attempts to find an instance of a user with the email provided
        stored_hash = UserCredentials[0]['passwordhash'].encode('utf-8')# converts stored password string into bytes
        PasswordBytes = password.encode('utf-8')# converts password string into bytes


        if bcrypt.checkpw(PasswordBytes, stored_hash):#this checks if the hashed versions match as hashed passwords cannot be unhashed
            return UserCredentials     
        else:
            return -1


    except:
        return -1

def signup(connection, email, password):
    # Check duplicate email
    existingEmail = Read(connection, 'users', {'email': email})
    if existingEmail != -1:
        return -1

    #hashing given password
    hashedPassword = Passwordhash(password)
    try:
        UserCredentials = Create(connection, 'users', {'email':email, 'passwordhash': hashedPassword})
        #this creates a new record for the user as the email does not exist in any records
        return UserCredentials
    except:
        return -1

