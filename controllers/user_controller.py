from database.__init__ import database

def create_user(user):
        return database['SCHOOL_PY_PROJECT']['Users'].insert_one(user.__dict__)
