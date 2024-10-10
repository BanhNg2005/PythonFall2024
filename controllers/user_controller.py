from database.__init__ import database
import app_config
import bcrypt

def generate_hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password

def create_user(user):

    try:
        user.name = user.name.lower()
        user.email = user.email.lower()
        user.password = generate_hash_password(user.password)

        print(user.__dict__)

        collection = database.database[app_config.CONST_USER_COLLECTION]

        if collection.find_one({"email": user.email}):
            return "Duplicated User"

        return collection.insert_one(user.__dict__)
    except:
        raise Exception("Error when creating user!")
    
def login_user(user_information):
    email = user_information["email"].lower()   
    password = user_information["password"].encode('utf-8')

    collection = database.database[app_config.CONST_USER_COLLECTION]

    current_user = collection.find_one({"email": email})

    if not current_user:
        return "Invalid email"
    
    if not bcrypt.checkpw(password, current_user["password"]):
        return "Invalid password"
    
    return "LOGGED IN"
