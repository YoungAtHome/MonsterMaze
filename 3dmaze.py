from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
import time
from collections import OrderedDict
from signal import pause
 
black = (0, 0, 0)
grey = (128, 128, 128)
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
turquoise = (0, 255, 255)

compass = OrderedDict()
compass['north'] = (-1, 0)
compass['east'] = (0, 1)
compass['south'] = (1, 0)
compass['west'] = (0, -1)



maze = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1], 
        [1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1], 
        [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 2, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
entry = (7, 3)
wayout = (13, 9)

pos = entry
dir = 'east' #(0, 1)
escaped = False

plan = [black, white]

modes = {'plan': 0, '3D': 1}
mode = 1

s = SenseHat()

"""
Anyone there?   
Well press something...

Roll up, roll up, see the amazing Tyrannosaurus Rex
King of the Dinosaurs in hus Lair.
Perfectly preserved in silicon since prehistoric times,
he is brought to you for your entertainment and exhilaration.

If you dare to enter his lair, you do so at your own risk.
The Managerment accept no responsibility for the health and safety
of the Adventuror who enters his realm. The Management advise 
that this is no  game for those of a nervous disposition.

If you are in any doubt, SHAKE with fear to stop.
If instructions are needed to proceed PRESS the joystick button,
otherwise just wait to be taken in.

The mists of time will pass over you while transporting 
you to the lair of the Tyrannosaurus Rex.
Best of Luck.....
"""

def intro():
  s.low_light = True
  s.show_message("Anyone there?   Well press something...", scroll_speed=0.1)
  event = s.stick.wait_for_event()
  s.show_message("""Roll up, roll up, see the amazing Tyrannosaurus Rex
King of the Dinosaurs in hus Lair.
Perfectly preserved in silicon since prehistoric times,
he is brought to you for your entertainment and exhilaration.
"""
    , scroll_speed=0.1)
  return
  s.show_message("""If you dare to enter his lair, you do so at your own risk.
The Managerment accept no responsibility for the health and safety
of the Adventuror who enters his realm. The Management advise 
that this is no  game for those of a nervous disposition.
"""
  )
  s.show_message("""If you are in any doubt, SHAKE with fear to stop.
If instructions are needed to proceed PRESS the joystick button,
otherwise just wait to be taken in.
"""
  )
  s.show_message("""The mists of time will pass over you while transporting 
you to the lair of the Tyrannosaurus Rex.
Best of Luck.....
"""
  )

#def rex_warning():
"""
Rex lies in wait
He is hunting for you
Footsteps approaching
Rex has seen you
RUN hs is beside you
"""
#pass

def rex_end():
  if escaped:
    s.show_message("""
You have eluded him and scored points.
Rex is very angry.
You'll need more luck this time.
"""
)
  else: 
    s.show_message("""
You have been posthumously awarded points
and sentenced to roam the maze forever.
If you wish to appeal SHAKE with fear
else wait to continue roaming.
"""
)



"""
Display plan view of maze around pos
"""
def display_plan(s):
  pixels = []
  #blank 1st row
  pixels = [black] * 8
  
  #print('rows', (pos[0]-3, pos[0]+4))
  for r in range(pos[0]-3, pos[0]+4):
    #print('maze', maze[r][pos[0]-3:pos[0]+4])
    #print('plan row',[plan[m] for m in maze[r][pos[0]-3:pos[0]+4]])
    pixels.extend([plan[m] for m in maze[r][pos[1]-3:pos[1]+4]])
    pixels.extend([black])
  
  pixels[3 + 4*8] = blue
  #print(len(pixels), pixels)
  
  #print(dir, 90 * ((5-(list(compass.keys()).index(dir)+1)) % 4))
  s.set_rotation(90 * ((5-(list(compass.keys()).index(dir)+1)) % 4))
  # display the pixels  
  s.set_pixels(pixels)

def set_column(pixels, column, length, colour):
  #print('pixels',pixels, 'column',column, 'length',length, 'colour',colour)
  top = int((8-length+1) / 2)
  bottom = top + length
  bright = (64 + length*27) / 256
  clm_colour = (int(colour[0]*bright), int(colour[1]*bright), int(colour[2]*bright))
  #print('top',top, 'bottom',bottom, 'bright',bright, 'clm_colour',clm_colour)
  for row in range(1, top):
    w_bright = ((255-(((row-1)*2+1)*27))/256)
    pixels[row*8 + column] = (int(white[0]*w_bright), int(white[1]*w_bright), int(white[2]*w_bright))
  for row in range(top, bottom):
    pixels[row*8 + column] = clm_colour
  for row in range(bottom, 8):
    pixels[row*8 + column] = black


""" Display the visible parts of a maze_part

Maze part is an array of 3 by 4 booleans.

   0 1 2	

3  X X X         G
2  X 0 0   RR   GG
1  X 0 X   RRB  GG
0  0 * X   RRBRRGG
           RRB  GG
           RR   GG
 		             G

"""
def display(s, maze_part):
  pixels = []
  pixels = [black] * 64
  
  mp = maze_part
  cl = red
  
  if mp[0][0]:
    set_column(pixels, 0, 7, blue)
  else:
    set_column(pixels, 0, 5, red)
  if mp[2][0]:
    set_column(pixels, 6, 7, green)
  else:
    set_column(pixels, 6, 5, red)
  if mp[1][1] > 0:
    if mp[1][1] == 2: 
      cl = yellow
    for col in range(1,6):
      set_column(pixels, col, 5, cl)
  else:
    if mp[0][1]:
      set_column(pixels, 1, 5, blue)
    else:
      set_column(pixels, 1, 3, red)
    if mp[2][1]:
      set_column(pixels, 5, 5, green)
    else:
      set_column(pixels, 5, 3, red)
    if mp[1][2] > 0:
      if mp[1][2] == 2: 
        cl = yellow
      for col in range(2,5):
        set_column(pixels, col, 3, cl)
    else:
      if mp[0][2]:
        set_column(pixels, 2, 3, blue)
      else:
        set_column(pixels, 2, 1, red)
      if mp[2][2]:
        set_column(pixels, 4, 3, green)
      else:
        set_column(pixels, 4, 1, red)
      if mp[1][3] > 0:
        if mp[1][3] == 2: 
          cl = yellow
        set_column(pixels, 3, 1, cl)
      else:
        set_column(pixels, 3, 1, turquoise)
  #print(pixels)
   
  # display the pixels  
  s.set_pixels(pixels)

def display_3d(s):
  maze_part = []
  #list(compass.keys()).index(dir)
  #print('dir', dir)
  if dir == 'north':
    r1, r2, rs = 0, -4, -1
    c1, c2, cs = -1, 2, 1
  elif dir == 'east':
    r1, r2, rs = -1, 2, 1
    c1, c2, cs = 0, 4, 1
  elif dir == 'south':
    r1, r2, rs = 0, 4, 1
    c1, c2, cs = 1, -2, -1
  elif dir == 'west':
    r1, r2, rs = 1, -2, -1
    c1, c2, cs = 0, -4, -1

  if rs == cs:
    #print('rows', (pos[0]+r1, pos[0]+r2))
    for r in range(pos[0]+r1, pos[0]+r2, rs):
      #print('maze', maze[r][pos[1]+c1:pos[0]+c2])
      if cs == 1:
        maze_part.append([m for m in maze[r][pos[1]+c1:pos[1]+c2]])
      else:
        #maze_part.append(reversed([m for m in maze[r][pos[1]+c2:pos[1]+c1]]))
        smp = []
        for c in range(pos[1]+c1, pos[1]+c2, cs):
          smp.extend([maze[r][c]])
        maze_part.append(smp)
  else:
    #print('columns', (pos[1]+c1, pos[1]+c2))
    for c in range(pos[1]+c1, pos[1]+c2, cs):
      #print('pos[0]',pos[0], 'r1',r1, 'r2',r2, 'c',c)
      #print(pos[0]+r1, pos[0]+r2, rs)
      #print('maze', maze[pos[0]+r1:pos[0]+r2][c])
      smp = []
      for r in range(pos[0]+r1, pos[0]+r2, rs):
        smp.extend([maze[r][c]])
      maze_part.append(smp)
  
  #print('maze part', maze_part)
  #print(maze_part[0])
  #print(maze_part[1])
  #print(maze_part[2])
  display(s, maze_part)


def forward(event):
  global pos, dir, escaped
  if event.action != ACTION_RELEASED:
    #print('pos',pos, 'dir',dir)
    try:
      #print('compass dir', compass[dir])
      newpos = [p + d for p, d in zip(pos, compass[dir])]
      #print('newpos', newpos, 'wayout', wayout)
      if (newpos[0] == wayout[0]) and (newpos[1] == wayout[1]):
        print('escaped')
        escaped = True;
        return
      #print('maze at newpos',maze[newpos[0]][newpos[1]])
      if not maze[newpos[0]][newpos[1]]:
        pos = newpos
    except Exception as e:
      print(e)
    #print('new: ', 'pos',pos, 'dir',dir)
  
def back(event):
  global pos, dir
  if event.action != ACTION_RELEASED:
    #print('pos',pos, 'dir',dir)
    try:
      #print(compass[dir][0], compass[dir][1])
      newpos = [p - d for p, d in zip(pos, compass[dir])]
      #newpos = [pos[0] - compass[dir][0], pos[1] - compass[dir][1]]
      if not maze[newpos[0]][newpos[1]]:
        pos = newpos
    except Exception as e:
      print(e)
    #print('new: ', 'pos',pos, 'dir',dir)
  
def left(event):
  global pos, dir
  if event.action != ACTION_RELEASED:
    #print('pos',pos, 'dir',dir)
    try:
      l = list(compass.keys())
      i = l.index(dir)
      if i == 0:
        left = l[len(l)-1]
      else:
        left = l[i-1]
    except Exception as e:
      print(e)
    dir = left
    #print('new: ', 'pos',pos, 'dir',dir)
  
def right(event):
  global pos, dir
  if event.action != ACTION_RELEASED:
    #print('pos',pos, 'dir',dir)
    try:
      l = list(compass.keys())
      i = l.index(dir)
      if i == len(l)-1:
        right = l[0]
      else:
        right = l[i+1]
    except Exception as e:
      print(e)
    dir = right
    #print('new: ', 'pos',pos, 'dir',dir)

def mode_change(event):
  """ Switch modes """
  global mode
  if event.action != ACTION_RELEASED:
    mode = 1-mode

def display_after_action(event):
  if event.action != ACTION_RELEASED:
    if mode==0:
      display_plan(s)
    elif mode==1:
      s.rotation = 0
      display_3d(s)
  

def test_3d_move():
  global mode
  s.clear()

  s.stick.direction_up = forward
  s.stick.direction_down = back
  s.stick.direction_left = left
  s.stick.direction_right = right
  s.stick.direction_middle = mode_change
  s.stick.direction_any = display_after_action

  mode = 1 #3d  
  spf = 1
  if mode==0:
    display_plan(s)
  elif mode==1:
    display_3d(s)
  while not escaped:
    #print('pos',pos, 'dir',dir)
    time.sleep(spf)
  if mode==0:
    s.set_pixel(0, 7, green)
  time.sleep(spf)
  rex_end()  

def test_plan_move():
  s = SenseHat()
  s.clear()

  s.stick.direction_up = forward
  s.stick.direction_down = back
  s.stick.direction_left = left
  s.stick.direction_right = right
  
  mode = 0 # plan
  spf = 1
  while not escaped:
    #print('pos',pos, 'dir',dir)
    if mode==0:
      display_plan(s)
    elif mode==1:
      display_3d(s)
    time.sleep(spf)
  if mode==0:
    s.set_pixel(0, 7, green)
  
  
def test_plan():
  s = SenseHat()
  s.clear()
  
  display_plan(s)

def test_moves():
  s = SenseHat()
  s.clear()
  
  s.stick.direction_up = forward
  s.stick.direction_down = back
  s.stick.direction_left = left
  s.stick.direction_right = right
  
  pause()



"""
3  X X X         G
2  X 0 0   RR   GG
1  X 0 X   RRB  GG
0  0 * X   RRBRRGG
"""
def test_fixed():
  s = SenseHat()

  spf = 1
  while 1:
    """ma = [[0, 0, 0, 1], 
          [1, 0, 0, 0], 
          [1, 1, 1, 1]]
    """
    m0 = [[1, 0, 1, 1], 
          [0, 0, 0, 0], 
          [0, 1, 1, 0]]
    m1 = [[0, 1, 1, 1], 
          [0, 0, 0, 1], 
          [1, 1, 0, 1]]
    m2 = [[1, 1, 1, 1], 
          [0, 0, 1, 0], 
          [1, 0, 1, 1]]
    m3 = [[1, 1, 1, 1], 
          [0, 1, 0, 0], 
          [0, 1, 1, 1]]
    
    display(m0)
    time.sleep(spf)
    exit()
    
    display(m1)
    time.sleep(spf)
    
    display(m2)
    time.sleep(spf)

    display(m3)
    time.sleep(spf)

    display(m2)
    time.sleep(spf)
    
    display(m1)
    time.sleep(spf)

#test_fixed()
#test_moves()
#test_plan_move()
#intro()
test_3d_move()
