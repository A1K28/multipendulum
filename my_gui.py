#TODO: Optimize - possibly rewrite the code. for now keep it turned off while in a simulation unless modifying
#NOTE: This code was written for testing purposes only and by no means is the final product
#NOTE: my_gui.py shall be rewritten


class Gui(object):
	def __init__(self,pl,num_pendula,g,FPS,trail_length,PDE_method):
		self.text_color = (255,255,255)
		self.pos = [50,50]
		self.text = "Press \'m\' to open menu"
		self.old_mouse_pos = []
		self.pl = pl 	#referencing. not copying
		self.num_pendula = num_pendula
		self.FPS = FPS
		self.g = g
		self.restart_game = False
		self.trail_length = trail_length
		self.PDE_method = PDE_method

		self.pendula_setter_slider = Slider([10,40],[1,5],self.num_pendula,str("N"))
		self.grav_slider = Slider([10,35+30],[0.00,2],g[0],str("gravity"))
		self.FPS_slider = Slider([10,35+30*2],[1,120],FPS[0],str("time step ^-1 (FPS)"))
		self.sliders = [[0], [0]]		#[[l1,li2..],[m1,m2..]]
		# for i in range(self.num_pendula):
		self.sliders[0] = [Slider([10,35+(i+3)*30],[80,250],pl[i].length, str("length - " + str(i+1))) for i in range(self.num_pendula)]
		self.sliders[1] = [Slider([10,self.sliders[0][-1].pos[1]+(i+1)*30],[1,10],pl[i].mass, str("mass - " + str(i+1))) for i in range(self.num_pendula)]
		self.trail_slider = Slider([10,self.sliders[1][-1].pos[1]+30],[2,1500],trail_length[0],str("trail length"))

		self.pde_color = [[255,255,255] for i in range(4)]
		self.pde_color[self.PDE_method[0]] = [255,0,127]
		self.PDE_0 = Button(self.pde_color[0],10,self.trail_slider.pos[1]+30*2,50,50,"None")
		self.PDE_1 = Button(self.pde_color[1],50+15,self.trail_slider.pos[1]+30*2,50,50,"Euler")
		self.PDE_2 = Button(self.pde_color[2],10,self.trail_slider.pos[1]+30*4,50,50,"RK2_I")
		self.PDE_3 = Button(self.pde_color[3],50+15,self.trail_slider.pos[1]+30*4,50,50,"RK4_I")
		self.PDE_list = [self.PDE_0,self.PDE_1,self.PDE_2,self.PDE_3]

	def draw(self, pygame, DISPLAYSURF, gui_open):
		mx, my = pygame.mouse.get_pos()

		font = pygame.font.Font("data/COMIC.TTF", 12)
		menu_text = font.render(self.text, 1, self.text_color)
		DISPLAYSURF.blit(menu_text, (5,5))

		PDE_text = font.render("PDE methods:", 1, self.text_color)
		# DISPLAYSURF.blit(PDE_text, (10,self.trail_slider.pos[1]+30,))



		self.update(pygame, DISPLAYSURF, gui_open,mx,my,PDE_text)

	def update(self, pygame, DISPLAYSURF, gui_open,mx,my,PDE_text):
		if gui_open: 
			self.text = "Press \'m\' to close menu"
			self.pendula_setter_slider.draw(pygame,DISPLAYSURF,mx,my)
			self.grav_slider.draw(pygame,DISPLAYSURF,mx,my)
			self.FPS_slider.draw(pygame,DISPLAYSURF,mx,my)
			self.trail_slider.draw(pygame,DISPLAYSURF,mx,my)

			for i in range(len(self.PDE_list)):
				self.PDE_list[i].draw(pygame,DISPLAYSURF)
				self.PDE_list[i].is_pressed((mx,my),pygame)
				if self.PDE_list[i].active:
					self.PDE_method[0] = i
					self.restart_game = True

			for i in range(self.num_pendula):
				self.sliders[0][i].draw(pygame,DISPLAYSURF,mx,my)
				self.sliders[1][i].draw(pygame,DISPLAYSURF,mx,my)
			self.text_color = (255,255,255)

			DISPLAYSURF.blit(PDE_text, (10,self.trail_slider.pos[1]+30))

			self.update_value()
			self.update_pendula()
		else: 
			self.text = "Press \'m\' to open menu"

			#--fade menu_text to black from white
			if not self.has_mouse_moved([mx,my]):
				if self.text_color[0]>0: self.text_color = [self.text_color[i]-1 for i in range(3)]		#conditional comprehension results in error for some reason
			else: 
				self.text_color = (255,255,255)

	def has_mouse_moved(self,pos):
		if self.old_mouse_pos == pos:
			return False
		else:
			self.old_mouse_pos = pos[:]
			return True

	#mapping values from one dimension to another
	def update_value(self):
		self.FPS[0] = (self.FPS_slider.button.x-self.FPS_slider.slider_pos[0])/(self.FPS_slider.slider_length)*(self.FPS_slider.minmax[1]-self.FPS_slider.minmax[0])+self.FPS_slider.minmax[0]
		self.FPS_slider.value = str(round(self.FPS[0]))

		old_value = self.trail_slider.value
		self.trail_length[0] = round((self.trail_slider.button.x-self.trail_slider.slider_pos[0])/(self.trail_slider.slider_length)*(self.trail_slider.minmax[1]-self.trail_slider.minmax[0])+self.trail_slider.minmax[0])
		self.trail_slider.value = str(self.trail_length[0])

		self.g[0] = (self.grav_slider.button.x-self.grav_slider.slider_pos[0])/(self.grav_slider.slider_length)*(self.grav_slider.minmax[1]-self.grav_slider.minmax[0])+self.grav_slider.minmax[0]
		self.grav_slider.value = str(round(self.g[0],2))
		for i in range(self.num_pendula):
			self.pl[i].length = (self.sliders[0][i].button.x-self.sliders[0][i].slider_pos[0])/(self.sliders[0][i].slider_length)*(self.sliders[0][i].minmax[1]-self.sliders[0][i].minmax[0])+self.sliders[0][i].minmax[0]
			self.sliders[0][i].value = str(round(self.pl[i].length,2))
			self.pl[i].mass = (self.sliders[1][i].button.x-self.sliders[1][i].slider_pos[0])/(self.sliders[0][i].slider_length)*(self.sliders[1][i].minmax[1]-self.sliders[1][i].minmax[0])+self.sliders[1][i].minmax[0]
			self.sliders[1][i].value = str(round(self.pl[i].mass,2))

			if old_value != self.trail_slider.value:
				self.pl[i].update_trail[0] = True
				self.trail_slider.value = str(self.trail_length[0])

	def update_pendula(self):
		old_pendula_num = self.num_pendula
		self.num_pendula = round((self.pendula_setter_slider.button.x-self.pendula_setter_slider.slider_pos[0])/(self.pendula_setter_slider.slider_length)*(self.pendula_setter_slider.minmax[1]-self.pendula_setter_slider.minmax[0])+self.pendula_setter_slider.minmax[0])
		if (self.num_pendula != old_pendula_num):
			self.restart_game = True
		else:
			self.pendula_setter_slider.value = str(self.num_pendula)


class Slider(object):
	def __init__(self,pos,minmax,value,text=""):
		self.pos = pos[:]
		self.slider_pos = pos[:]
		self.minmax = minmax[:]
		self.value = str(value)
		self.slider_length = 70
		self.text = text
		self.button = Button((255,255,255),float(self.value),self.pos[1]+2-25/2,10,25)
		self.text_color = (255,255,255)
		self.offset = 15

	def draw(self,pygame,DISPLAYSURF,mx,my):
		font = pygame.font.Font("data/COMIC.TTF", 12)
		
		text = font.render(self.text, 1, self.text_color)
		DISPLAYSURF.blit(text, (self.pos[0],self.pos[1]-10))

		value = font.render(self.value, 1, (255,0,127))
		DISPLAYSURF.blit(value, (self.slider_pos[0]+self.slider_length+self.offset,self.slider_pos[1]-10))
		
		self.check_slider_pos_valid(text)

		pygame.draw.line(DISPLAYSURF,(255,255,255),(self.slider_pos[0],self.slider_pos[1]),(self.slider_pos[0]+self.slider_length,self.slider_pos[1]),4)
		self.update(pygame,DISPLAYSURF,mx,my,text)

	def update(self,pygame,DISPLAYSURF,mx,my,text):
		self.check_button_pos_valid(text)
		mouse_pressed = pygame.mouse.get_pressed()[0]

		#--move slider button horizontally--
		if self.in_contact([mx,my],text):
			self.button.color = (255,0,127)
			if mouse_pressed:
				self.button.x = mx
				if mx < self.slider_pos[0]:
					self.button.x = self.slider_pos[0]
				elif mx > self.slider_pos[0]+self.slider_length:
					self.button.x = self.slider_pos[0]+self.slider_length
		else:
			self.button.x = (float(self.value)-self.minmax[0])/(self.minmax[1]-self.minmax[0])*self.slider_length+self.slider_pos[0]
			self.button.color = (255,255,255)

		#--draw moving button--
		self.button.draw(pygame,DISPLAYSURF)

	def in_contact(self,pos,text):
		if pos[0]>=self.slider_pos[0]-self.offset and pos[0]<=self.slider_pos[0]+self.slider_length+self.offset:
			if pos[1]<=self.slider_pos[1]+2.5+25/2 and pos[1]>=self.slider_pos[1]+2.5-25/2:
				return True
		return False

	def check_button_pos_valid(self,text):
		if self.button.x < self.slider_pos[0]:
			self.button.x = self.slider_pos[0]
		elif self.button.x > self.slider_pos[0]+self.slider_length:
			self.button.x = self.slider_pos[0]+self.slider_length

	def check_slider_pos_valid(self,text):
		if self.slider_pos[0] != self.pos[0]+text.get_width()+self.offset:
			self.slider_pos[0] = self.pos[0]+text.get_width()+self.offset



class Button(object):
	def __init__(self, color, x,y,width,height, text=''):
		self.color = color
		self.initial_color = color
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.active = False

	def draw(self,pygame,win,outline=None):
		#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
			
		pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
		mx, my = pygame.mouse.get_pos()

		if self.in_contact((mx,my)):
			self.color = (255,0,127)
		else:
			self.color = self.initial_color

		if self.text != '':
			font = pygame.font.Font('data/COMIC.TTF', 10)
			text = font.render(self.text, 1, (0,0,0))
			win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

	def in_contact(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
		return False

	def is_pressed(self,pos,pygame):
		if self.in_contact(pos):
			if pygame.mouse.get_pressed()[0]:
				self.active = True