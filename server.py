from src.app import app
import src.controllers.ironhackers_controller
import src.controllers.repositories_controller

from config import PORT

app.run("0.0.0.0", PORT, debug=True)
