from pathlib import Path

data_folder = Path("./data/")
formulae_json = data_folder / "simple_formulae.json"

import pygame, math, json
from pygame.locals import *
from my_gui import Gui

pygame.init()

surf_width = 1280       #initial window size
surf_height = 720
num_pendula = 2
FPS = [60]              #this is a list because we need to reference it later (modify from somewhere else)
g = [0.8]
halt_motion = False     #motion is halted when mouse is clicked
gui_open = False        #not able to interact with the system when ==true
restart_game = [False]  #restart when importang change is made
trail_length = [100]
PDE_method = [3]        #0:none, 1:euler, 2:RK_2_I, 3:RK_4_I


DISPLAYSURF = pygame.display.set_mode((surf_width, surf_height))
pygame.display.set_caption('pendulum proj.py')


class Pendulum(object):
    def __init__(self, x, y, length, fi):
        self.length = length
        self.fi = fi    #in radians
        self.mass = 5
        self.pivot = [x, y]
        self.bob = [self.pivot[0]+self.length*math.sin(self.fi), self.pivot[1]+self.length*math.cos(self.fi)]
        self.vel = 0
        self.acc = 0
        self.following_mouse = False
        self.update_trail = [False]
        self.trail_coords = [[0 for col in range(2)] for row in range(trail_length[0])]

    def draw(self, DISPLAYSURF, acceleration):
        pygame.draw.line(DISPLAYSURF, (211,211,211), (self.pivot[0], self.pivot[1]), (self.bob[0], self.bob[1]), 2)
        pygame.draw.circle(DISPLAYSURF, (230,190,230), (int(self.bob[0]), int(self.bob[1])), 13)    #last arg == size
        self.update(DISPLAYSURF, acceleration)

        if self.update_trail[0]:
            self.trail_coords = [[0 for col in range(2)] for row in range(trail_length[0])]
            self.update_trail[0] = False

    def update(self, DISPLAYSURF, acceleration):
        #--update dd0, d0 & 0--
        self.acc = 0 if halt_motion else acceleration
        self.vel = 0 if halt_motion else self.vel + self.acc
        self.fi += self.vel
        self.bob = [self.pivot[0]+self.length*math.sin(self.fi), self.pivot[1]+self.length*math.cos(self.fi)]
        # if self.fi<-0.5*math.pi or self.fi > 1.5*math.pi:
        #   self.fi = (self.fi+0.5*math.pi) % (2*math.pi) - 0.5*math.pi
        
    def follow_mouse(self, vector):
        self.following_mouse = True
        mouse_v = vector[:]
        v_mag = math.sqrt(mouse_v[0]**2+mouse_v[1]**2)
        sin_fi = mouse_v[0]/v_mag
        fi = math.asin(sin_fi)
        if (mouse_v[1]<0):
            fi += 2*(math.pi/2-fi)
        self.fi = fi


#--Only 5 colors because max pendulum size is 5. this can be automated 
#but CPU can't handle many pendula (derived from euler-lagrange) at once. so we choose colors ourselves--
trail_colors = [(255,0,127),(42,75,124),(255,111,97),(107,91,149),(155,27,48)]

total_energy = 0
counter = 0
def main():
    global pl,accs,g,FPS,num_pendula,trail_length,DISPLAYSURF,surf_width,surf_height,PDE_method
    pl = []     #list of all active pendula
    accs = []   #list of accelerations for each
    for i in range(num_pendula):
        accs.append(0)
        if i == 0: pl.append(Pendulum(surf_width//2, 0.208*surf_height, 250, math.pi/2))  #(length, fi)   default values for the first pendulum
        else: pl.append(Pendulum(pl[i-1].bob[0], pl[i-1].bob[1], 100, 0))

    #--initial conditions--
    if num_pendula == 2: pl[0].mass = 10
    if num_pendula == 3 or num_pendula == 4: 
        pl[1].length = 170
        pl[2].length = 125

    fpsClock = pygame.time.Clock()
    finalstr = read_formula()
    Equations = [finalstr[finalstr.find(EQ_str[i])+len(EQ_str[i]):finalstr.find(EQ_str[i+1])] for i in range(num_pendula)]  #reading from str
    w_i = [pl[i].vel for i in range(num_pendula)]   #initial conditions for PDE-s
    game_gui = Gui(pl,num_pendula,g,FPS,trail_length,PDE_method)

    run = True
    while run: # main game loop
        DISPLAYSURF.fill((0,0,0))
        mx, my = pygame.mouse.get_pos()

        global counter, total_energy, halt_motion, gui_open

        pot_energy = 0
        kin_energy = 0
        
        if PDE_method[0] != 0:
            if halt_motion:
                w_i = [pl[i].vel for i in range(num_pendula)]
            else:
                if PDE_method[0] == 1: w_f = euler(w_i,Equations)
                if PDE_method[0] == 2: w_f = RK_2_I(w_i,Equations)
                if PDE_method[0] == 3: w_f = RK_4_I(w_i,Equations)
                accs=[w_f[i]-w_i[i] for i in range(num_pendula)]
                w_i = w_f[:]

        #--draw gui if active--
        game_gui.draw(pygame,DISPLAYSURF,gui_open)
        for i in range(num_pendula):
            #--draw pendula--apply formulas to angular acceleration equations
            if PDE_method[0] == 0: accs[i] = eval(Equations[i])

            #--follow mouse--
            if halt_motion:
                if(pl[i].following_mouse):
                    pl[i].follow_mouse([mx-pl[i].pivot[0], my-pl[i].pivot[1]])
                pl[i].trail_coords = [[0 for col in range(2)] for row in range(trail_length[0])]
            #--draw trails--
            else:
                pl[i].following_mouse = False
                pl[i].trail_coords[0] = pl[i].bob
                for j in range(len(pl[i].trail_coords)-1):
                    pl[i].trail_coords[-j-1] = pl[i].trail_coords[-2-j]
                    if pl[i].trail_coords[j][0] != 0 and pl[i].trail_coords[j+1][0] != 0:
                        pygame.draw.line(DISPLAYSURF, trail_colors[i], (int(pl[i].trail_coords[j][0]), int(pl[i].trail_coords[j][1])),(int(pl[i].trail_coords[j+1][0]),int(pl[i].trail_coords[j+1][1])), 3)



        for event in pygame.event.get():
            if event.type == QUIT:  #close the process
                pygame.quit()
                sys.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not gui_open:
                    if not halt_motion:     #making sure the func() is only called once
                        pl[min_value_index(pl, mx, my)].following_mouse = True
                    halt_motion = True
            if event.type == pygame.MOUSEBUTTONUP:
                halt_motion = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    gui_open = not gui_open
            if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
                DISPLAYSURF = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                surf_width = event.w
                surf_height = event.h
                game_gui.restart_game = True

        for i in range(len(pl)):
            pl[-i-1].draw(DISPLAYSURF, accs[-i-1])
            if i != 0:      #update pendulas' origin (except for the first one)
                pl[i].pivot = pl[i-1].bob


        pygame.display.update()
        fpsClock.tick(FPS[0])

        if game_gui.restart_game:
            game_gui.restart_game = False
            run = False
            num_pendula = game_gui.num_pendula

    main()

#--initializing dfi to reference it below
dfi = [0 for i in range(num_pendula)]

def euler(w0_arr, Eq_arr):
    global dfi
    dfi = w0_arr
    wf_arr = [w0_arr[i]+eval(Eq_arr[i]) for i in range(num_pendula)]        #y0 = y1 + h * y'
    return wf_arr


#--In the RK methods, our functions don't have time as a variable-- thus we let: dw0/dt=C ==> w0=C*t
def RK_2_I(w0_arr, Eq_arr):
    global dfi
    dfi=w0_arr
    k1 = [eval(Eq_arr[i]) for i in range(num_pendula)]      #k1=h*y'
    dfi = [w0_arr[i]+0.5*k1[i] for i in range(num_pendula)]
    k2 = [eval(Eq_arr[i]) for i in range(num_pendula)]
    return [w0_arr[i]+k2[i] for i in range(num_pendula)]


def RK_4_I(w0_arr, Eq_arr):
    global dfi
    dfi = w0_arr[:]
    try:
        k1 = [eval(Eq_arr[i]) for i in range(num_pendula)]
        dfi = [w0_arr[i]+0.5*k1[i] for i in range(num_pendula)]
        k2 = [eval(Eq_arr[i]) for i in range(num_pendula)]
        dfi = [w0_arr[i]+0.5*k2[i] for i in range(num_pendula)]
        k3 = [eval(Eq_arr[i]) for i in range(num_pendula)]
        dfi = [w0_arr[i]+k3[i] for i in range(num_pendula)]
        k4 = [eval(Eq_arr[i]) for i in range(num_pendula)]
        return [w0_arr[i]+(1/6)*(k1[i]+2*k2[i]+2*k3[i]+k4[i]) for i in range(num_pendula)]
    except:
        return w0_arr   #TODO: FIND a logical solution for NAN error in trails (float NaN != int ERROR)

#*WARNING*: keys (to be replaced items) can be overwritten
#This dictionary could have been avoided by naming variables the same way. it's only used once after choosing N (pendula)
#MANUALLY doing this (for now, until i think of how to automate)
#Note to self: left this unchanged. since might need to modify things in Matlab
EQ_str = ["EQ0", ",EQ1", ",EQ2", ",EQ3", ",EQ4", ",EQ5"]
replace_me_dict = {
    " " : "",
    "\"" : "",
    "g":"g[0]",
    "cos" : "math.cos",
    "sin" : "math.sin",
    "m1" : "pl[0].mass",
    "m2" : "pl[1].mass",
    "m3" : "pl[2].mass",
    "m4" : "pl[3].mass",
    "m5" : "pl[4].mass",
    "dfi1" : "dfi[0]",
    "dfi2" : "dfi[1]",
    "dfi3" : "dfi[2]",
    "dfi4" : "dfi[3]",
    "dfi5" : "dfi[4]",
    "fi1" : "pl[0].fi",
    "fi2" : "pl[1].fi",
    "fi3" : "pl[2].fi",
    "fi4" : "pl[3].fi",
    "fi5" : "pl[4].fi",
    "l1" : "pl[0].length",
    "l2" : "pl[1].length",
    "l3" : "pl[2].length",
    "l4" : "pl[3].length",
    "l5" : "pl[4].length",
    "pow" : "math.pow",
}

#CAREFUL: this method requires use of an ordered dictionary
def replace_text(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

#READ formulas from json
def read_formula():
    with open(formulae_json, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    formula = lines[num_pendula-1]
    return replace_text(formula, replace_me_dict)

#--used to find closest joint to mouse position--
def min_value_index(arr, mx, my):
    min = 0
    min_dist = 2000
    for i in range(len(arr)):
        dist_v = [mx-arr[i].bob[0], my-arr[i].bob[1]]
        mag_dist_v = v_mag(dist_v)
        if mag_dist_v < min_dist:
            min_dist = mag_dist_v
            min=i
    return min 

def v_mag(vector):
    return math.sqrt(vector[0]**2+vector[1]**2)
main()