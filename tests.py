from src.rectangle_detection import RectangleDetector
from src.cell_detection import CircleDetector
from src.agar import AgarAi
from train.train import TrainAgents

def test_alive(take_ss=False):
    agent = AgarAi()
    ss_path = 'img/current_screenshot.jpg'
    if take_ss:
        ss_path = 'img/test_alive.jpg'
        agent.gui_driver.capture_map_screenshot(ss_path)
    r = RectangleDetector(ss_path)
    rects = r.detect_rectangles()

    next_button = r.get_widest_rectangle(rects)
    r.draw_rectangles([next_button[1]])
    print(f"With the las ss agent says am alive? {agent.im_alive (next_button)}")

def test_resetart():
    trainer = TrainAgents()
    trainer.restart_world(take_ss=True)
    
def test_save_stats():
    agent = AgarAi()
    trainer = TrainAgents()
    stats = agent.get_stats()
    trainer.dump_stats(stats, 'data/agent_stats.csv')

def test_ready_to_play():
    agent = AgarAi()
    print(agent.im_ready_to_play())
    #print(agent.me.x, agent.me.y, agent.me.radius)
    #print("others", agent.objects)

def test_detect_circles():
    detector = CircleDetector('img/current_screenshot.jpg')
    detector.detect_circles()
    detector.draw_detected_circles()
    detector.save_image('img/test-save.jpg')
    print(detector.circles)

def test_attack():
    agent = AgarAi()
    #agent.update_state()
    agent.im_ready_to_play()
    agent.attack()


test_attack()

