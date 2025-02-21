import random

from pgzero.actor import Actor

music.play('running_music')

WIDTH = 1024  # Largura da área do jogo.
HEIGHT = 384  # Altura da área do jogo.
DISTANCE = 200  # A distância 
LEVEL_UP = 100  # Número de passos antes de aumentar a dificuldade.
speed = 20  # Velocidade dos objetos não jogadores.
object_frequency = 100  # Quanto menor, mais frequente.
steps = 0  # Conta o número de quadros até agora no jogo.
FALL = 10  # Penalidade ao bater em algo.
STARTED = False  # A corrida começou?
END = False  # O jogo terminou?

ground_objects = {
    'small_ground': {
        'pos': [320, 320],
        'items': [
            'cat',
            'dog',
            'box',
            'fire_hydrant',
            'traffic_cone',
            'undergrowth',
        ],
    },
    'large_ground': {
        'pos': [312, 312],
        'items': [
            'barrels',
            'barrier',
            'bushes',
            'fence', 
            'motorbike',
        ],
    },
}


active_objects = []  # Objetos não jogadores a serem evitados.


red = Actor('red_run1') # Representa "Vermelho"
red.name = 'red'  
red.pos = (512, 304)  
red.frame = 1  
red.jumping = False  
red.landing = False  
red.hit = False  

blue = Actor('blue_run1') # Representa "Azul"
blue.name = 'blue'  
blue.pos = (512, 304)  
blue.frame = 3  
blue.jumping = False  
blue.landing = False  
blue.hit = False  


# Chão
floor_a = Actor('floor')
floor_a.pos = 0, 332
floor_b = Actor('floor')
floor_b.pos = 1024, 332


def update_player(player):
    """
    Given a player, will ensure the correct image is used
    for their current state.
    """
    if player.jumping:
        player.image = "{}_run3".format(player.name)
    else:
        player.image = "{}_run{}".format(player.name, player.frame)
        player.frame += 1
        if player.frame > 5:
            player.frame = 1

def animate_update():
    """
    Update images so we have around 12 FPS.
    """
    global steps
    global speed
    global object_frequency
    global active_objects
    global power_up
    global END
    # Aumenta a dificuldade gradualmente
    steps += 1
    if steps % LEVEL_UP == 0:
        speed = min(40, speed + 4)  # Non plays move faster.
        # Objetos aparecem mais
        object_frequency = max(50, object_frequency - 5)
    # Update das imagens
    update_player(red)
    update_player(blue)
    # MOvimento do chão
    floor_a.left -= speed
    floor_b.left -= speed
    if int(floor_a.right) < 0:
        floor_a.left = floor_b.right
    if int(floor_b.right) < 0:
        floor_b.left = floor_a.right
    # Move objetos
    for obj in active_objects:
        obj.left -= speed

    # Condição de Vitoria
    distance_between_players = abs(red.left - blue.left)
    if (red.right < 0 or blue.right < 0):
        END = True
    else:

        clock.schedule_unique(animate_update, 0.08)

def jump(player, on_finished):
    player.jumping = True
    x, y = player.pos
    animate(player, pos=(x, 204), duration=0.5,
            on_finished=on_finished, tween='decelerate')

def fall(player, on_finished):
    x, y = player.pos
    animate(player, pos=(x, 304), duration=0.3, 
            on_finished=on_finished, tween='accelerate')

def red_reset():
    red.jumping = False
    red.landing = False

def red_jump():
    jump(red, red_fall)

def red_fall():
    fall(red, red_reset)
 
def blue_land():
    land(blue, blue_reset)
    
def blue_jump():
    jump(blue, blue_fall)

def blue_fall():
    fall(blue, blue_reset)
    
def blue_reset():
    blue.jumping = False
    blue.landing = False

def update():
  
    if END:  # The race has finished
        update_end()
    elif STARTED:  # The race has started
        update_race()
    else:  # Just display the intro screen
        update_intro()

def update_intro():
    global STARTED
    if keyboard[keys.SPACE]:
        STARTED = True
        clock.schedule_unique(animate_update, 0.08)

def update_end():
    global STARTED
    global END
    global speed
    global object_frequency
    global steps
    global active_objects
    if keyboard[keys.SPACE]:
        STARTED = True
        END = False
        speed = 20  # How fast non-player objects move.
        object_frequency = 100  # Smaller = more frequent.
        steps = 0
        red.pos = (512, 304)
        blue.pos = (512, 304)
        red.jumping = False
        blue.jumping = False
        red.antigravity = 0
        blue.antigravity = 0
        active_objects = []
        # Start the race.
        clock.schedule_unique(animate_update, 0.08)
    
def update_race():

    global active_objects
    global power_up
    if keyboard[keys.W] and not red.jumping:
        red_jump()
   
    if keyboard[keys.UP] and not blue.jumping:
        blue_jump()

    # Colisões
    for obj in active_objects:
        # Objeto passou direto
        if obj.right < 0:
            active_objects.remove(obj)
        # Colisao com vermelho
        if red.colliderect(obj):
            red.left -= FALL
            obj.red_hit = True

        # Colisão com azul
        if blue.colliderect(obj):
            blue.left -= FALL
            obj.blue_hit = True
                
    if random.randint(0, object_frequency) == 0 or not active_objects:
        make_obstacle(ground_objects)

def make_obstacle(objects):
    global active_objects
    obj_collection = objects[random.choice(list(objects.keys()))]    
    low = obj_collection['pos'][0]
    high = obj_collection['pos'][1]
    new_object = Actor(random.choice(obj_collection['items']), 
                       pos=(1024, random.randint(low, high)))
    new_object.red_hit = False
    new_object.blue_hit = False
    active_objects.append(new_object)

def draw():
    screen.blit('paper', (0, 0))
    if END:  
        draw_end()
    elif STARTED:  
        draw_race()
    else:  
        draw_intro()

def draw_intro():
    
    screen.draw.text('Corrida', (240, 10),
                     fontname='funsized', fontsize=56,
                     color=(0, 0, 255))
    
    screen.draw.text('Maluca', (530, 10),
                     fontname='funsized', fontsize=56,
                     color=(255, 0, 0))

    story = ("Voce e seu amigo decidiram apostar corrida! \n"
             "O vermelho eh o acelerado e impulsivo \n"
             "Ja o azul eh frio e calculista \n"
             "Escolha sua cor e entre na \"Corrida Maluca\" \n"
             "(O primeiro a sair da tela perde!!)").format(DISTANCE)
    screen.draw.text(story, (50, 80), width=900,
                     fontname='rudiment', fontsize=30,
                     color=(0, 0, 0))
    screen.draw.text('W - PULA AZUL', (50, 240),
                     fontname='rudiment', fontsize=30,
                     color=(0, 0, 255))
    screen.draw.text('Seta pra cima - PULA VERMELHO', (500, 240),
                     fontname='rudiment', fontsize=30,
                     color=(255, 0, 0))                 
    screen.draw.text('aperte ESPACO para comecar.', (270, 320),
                     fontname='rudiment', fontsize=38,
                     color=(0, 0, 0))


def draw_end():
    winner = 'Vermelho' if red.left > blue.left else 'Azul'
    color = (255, 0, 0) if red.left > blue.left else (0, 0, 255)
    screen.draw.text('{} venceu!'.format(winner), (260, 100),
                     fontname='funsized', fontsize=56,
                     color=color)
    screen.draw.text('Aperte Espaco para recomecar.', (360, 250),
                     fontname='rudiment', fontsize=38,
                     color=(0, 0, 0))
    
def draw_race():
    red.draw()
    blue.draw()
    floor_a.draw()
    floor_b.draw()
    for obj in active_objects:
        obj.draw()
    distance_between_players = int(abs(red.left - blue.left))
    distance_to_display = distance_between_players - (distance_between_players % 10)
    color = (255, 0, 0) if red.left > blue.left else (0, 0, 255)
    screen.draw.text('Distancia entre os dois: {}'.format(distance_to_display),
                         (10, 340), fontname='rudiment', fontsize=38,
                         color=color)