from guizero import App, Text
from StateMachine import StateMachine

app = App(title="UppSense")
displayMessage = Text(app, text="Here you can configure the application")
app.display()
