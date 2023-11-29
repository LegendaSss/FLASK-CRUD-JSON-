from flask import Flask

app = Flask(__name__)
app.secret_key= 'dsfdsf2eer423423423dfdf'


from core import routes

