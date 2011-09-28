from flask import Flask
import webapp.settings

app = Flask('webapp')
app.config.from_object('webapp.settings')

import views