from agar import AgarAi
from gui_utils import *
# Example usage

#Run experiment
for i in range(100):
    agent = AgarAi()
    agent.move_random(2)
    agent.revive()


#agent.update_state()
#agent.im_alive()

