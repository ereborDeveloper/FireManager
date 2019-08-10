from Explorer import *
from View import *
from Controller import *

model = Explorer("C")
controller = Controller(model)
view = View(model, controller)
view.mainloop()
