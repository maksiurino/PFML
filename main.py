from pfml.Graphics import *

window = sf.Window(sf.VideoMode((640 * 2, 360 * 2)), "Sample Window")

mario_1_stand = sf.Texture("./data/sma4/graphics/mario/mario-1.png", False, sf.lntRect((( 496, 0 ), ( 32, 31 ))))

mario_1 = sf.Sprite(mario_1_stand)

mario_1.setScale((2, 2))

TAB_COLOR = (243, 243, 243)

while window.isOpen():
    for event in window.pollEvent():
        if event.type == sf.pygame.QUIT:
            window.close()
    
    window.clear(TAB_COLOR)
    
    window.draw(mario_1)
    
    window.display()
