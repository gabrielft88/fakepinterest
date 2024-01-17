from fakeprinterest import database, app
from fakeprinterest.models import Foto, Usuario

with app.app_context():
    database.create_all()
