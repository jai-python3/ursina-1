from ursina import *
from ursina.shaders import normals_shader
import random

send_away = False
send_all_away = False

CUBE_COUNT = 400

FIELD_RANGE = 10
Z_FIELD_RANGE = 20
Z_EDGE = 150

min_x = FIELD_RANGE * -1
max_x = FIELD_RANGE

min_y = FIELD_RANGE * -1
max_y = FIELD_RANGE

min_z = FIELD_RANGE * -1
max_z = Z_FIELD_RANGE

random_generator = random.Random()

selected_cube_1 = None
selected_cube_2 = None
selected_cube_3 = None

cubes = []

app = Ursina()

window.title = 'Rotating Cubes'                # The window title
window.borderless = False               # Show a border
window.fullscreen = False               # Do not go Fullscreen
window.exit_button.visible = True      # Do not show the in-game red X that loses the window
window.fps_counter.enabled = True
window.color = color.black


unique_position_lookup = {}

def get_unique_position():
    position = (
        random.randint(min_x, max_x),
        random.randint(min_y, max_y),
        random.randint(min_z, max_z)
    )
    while position in unique_position_lookup:
        position = (
            random.randint(min_x, max_x),
            random.randint(min_y, max_y),
            random.randint(min_z, max_z)
        )
    unique_position_lookup[position] = True
    return position


class MyCube(Entity):
    def __init__(self, **kwargs):
        self.y_rotation_speed=kwargs.get('y_rotation_speed', random.randint(5, 200))
        position = get_unique_position()

        color = get_random_color()

        scale_dim = random.uniform(0.1, 1)
        scale = (scale_dim, scale_dim, scale_dim)

        super().__init__(
            position=position,
            model='cube',
            color=color,
            scale=scale,
            shader=normals_shader
        )


def get_random_color():
    red = random_generator.random() * 255
    green = random_generator.random() * 255
    blue = random_generator.random() * 255
    return color.rgb(red, green, blue)

def update():

    if held_keys['8']:  # camera up
        camera.position += (0, time.dt, 0)  # move up vertically
    if held_keys['2']:  # camera down
        camera.position -= (0, time.dt, 0)  # move down vertically
    if held_keys['6']:  # camera left
        camera.position += (time.dt, 0, 0)  # move up vertically
    if held_keys['4']:  # camera right
        camera.position -= (time.dt, 0, 0)  # move down vertically

    for cube in cubes:
        cube.rotation_y += time.dt * cube.y_rotation_speed
        if held_keys['r']:
            cube.color = get_random_color()
        if held_keys['f']:
            cube.y_rotation_speed = cube.y_rotation_speed + 5
        if held_keys['s']:
            if cube.y_rotation_speed > 0:
                cube.y_rotation_speed = cube.y_rotation_speed - 5
            if cube.y_rotation_speed < 0:
                cube.y_rotation_speed = 0

        if held_keys['b']:
            cube.rotation_z += time.dt * cube.y_rotation_speed
            # if cube.y_rotation_speed > 0
            #     cube.y_rotation_speed = cube.y_rotation_speed - 5

    global send_away
    global send_all_away

    if held_keys['j']:
        send_away = True
        send_all_away = False
    if held_keys['k']:
        send_away = False
    if held_keys['g']:
        # Send all away as group
        send_all_away = True

    if send_away:
        send_selected_cubes_away()
    elif send_all_away:
        send_all_cubes_away()

def send_all_cubes_away():
    selected_cube_4 = cubes[random.randint(0, len(cubes) - 1)]
    send_selected_cube(selected_cube_4, 10)

def send_selected_cubes_away():

    global selected_cube_1
    global selected_cube_2
    global selected_cube_3

    while selected_cube_1 is None:
        selected_cube_1 = cubes[random.randint(0, len(cubes) -1)]

    while selected_cube_2 is None:
        selected_cube_2 = cubes[random.randint(0, len(cubes) -1)]

    while selected_cube_3 is None:
        selected_cube_3 = cubes[random.randint(0, len(cubes) -1)]

    change_color(selected_cube_1, color.red)
    change_color(selected_cube_2, color.red)
    change_color(selected_cube_3, color.red)

    if send_selected_cube(selected_cube_1):
        selected_cube_1 = None

    if send_selected_cube(selected_cube_2):
        selected_cube_2 = None

    if send_selected_cube(selected_cube_3):
        selected_cube_3 = None


def change_color(selected_cube, color):
    selected_cube.color = color




def send_selected_cube(selected_cube, speed: int = 1):

    selected_cube_position = selected_cube.position
    z = selected_cube_position[2]
    # print(f"z: {z}")
    if z > Z_EDGE:
        selected_cube.visible = False
        print(f"cube has left")
        return True
        # selected_cube = None
    else:
        z = z + speed
        selected_cube.position = (selected_cube_position[0], selected_cube_position[1], z)
        return False


#def update():
#    cube.rotation_y += time.dt * 100    # Rotate every time update is called
#    if held_keys['t']:                  # If t is pressed
#        print(held_keys['t'])   


for x in range(CUBE_COUNT):
    cube = MyCube()
    cubes.append(cube)

app.run()                               # Run the app


