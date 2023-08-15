# Copyright [C] 2023 P.O Cream(浅),XiaoXuan and all contributors
# All right Reserved

#     Distributed under GPL license
#     See copy at https://opensource.org/licenses/GPL-3.0

import time                    
import os
import sys
import random
import pygame
import tkinter as tk
from PIL import *
from tkinter.ttk import Combobox
import tkinter.messagebox as tk_mb

update_info = """FreeWorld Pygame-创世 2.0.1 更新内容
1.地形
·在正常模式下加入新二级地形——树
·优化了全部算法，修改了过多重复性代码，缩减了代码
·在超平坦模式下加入新二级地形——山
·超平坦模式改为无二级地形，正常模式改为陡峭模式，原超平坦模式加入山后变为正常模式
·加入陡峭模式——原正常模式"""

class TerrainGeneration(object):
    def __init__(self):
        self.map_width = 100
        self.sky_height = 30
        self.grass_block_height = 1
        self.soil_block_height = 3
        self.ground_height = 36
        self.map_height = 70
        self.grass_probability = 0
        self.common_tree_probability = 8
        self.yellow_tree_probability = 0
        self.purple_tree_probability = 0
        self.mountain_probability = 18
        self.leave_probability = 4
        self.tree_height = [5,7]
        self.terrain_high = 0
    
    # @copyright Copyright [C] Xiaoxuan 2023
    def fill(self,change_value,*coordinate):
        for i in coordinate:
            self.map[i[0]-1][i[1]-1] = change_value
            
    def fill2(self,height,x,y,change_value):
        for i in range(height):
            self.map[x][y] = change_value;x -= 1
    
    def tree_generation(self,i):
        self.terrain_high = self.map_height - 1
        self.tree_height_number = random.randint(self.tree_height[0],self.tree_height[1])
        while self.map[self.terrain_high][i] != "0":self.terrain_high -= 1
        self.fill2(self.tree_height_number,self.terrain_high,i,"5")
        self.fill("4",(self.terrain_high-self.tree_height_number+1,i+1))
        if random.randint(0,1) == 0:self.fill("4",(self.terrain_high-self.tree_height_number,i+1))
        self.fill("4",(self.terrain_high-self.tree_height_number+1,i),(self.terrain_high-self.tree_height_number+1,i+2))
        self.fill("4",(self.terrain_high-self.tree_height_number+2,i),(self.terrain_high-self.tree_height_number+2,i+2))
        if random.randint(0,1) == 0:self.fill("4",(self.terrain_high-self.tree_height_number+3,i))
        if random.randint(0,1) == 0:self.fill("4",(self.terrain_high-self.tree_height_number+3,i+2))
        if random.randint(0,1) == 0:self.fill("4",(self.terrain_high-self.tree_height_number+2,i+3))
        if random.randint(0,1) == 0:self.fill("4",(self.terrain_high-self.tree_height_number+2,i-1))
    
    def mountain_generation(self,i):
        self.terrain_high = self.map_height - 1
        while self.map[self.terrain_high][i] != "0":self.terrain_high -= 1
        self.mountain_init_height = 4
        self.minus = -1
        for j in range(random.randint(4,7)):
            self.fill2(self.mountain_init_height,self.terrain_high,i+self.minus,"2")
            self.mountain_init_height += random.randint(-2,2)
            self.minus += 1
        
    def terrain_generation(self,type):
        if type == 1:
            self.map = [["0" for i in range(self.map_width)] for j in range(self.sky_height)] + \
                       [["3" for i in range(self.map_width)] for j in range(self.grass_block_height)] + \
                       [["1" for i in range(self.map_width)] for j in range(self.soil_block_height)] + \
                       [["2" for i in range(self.map_width)] for j in range(self.ground_height)]
        elif type == 2:
            self.map = [["0" for i in range(self.map_width)] for j in range(self.sky_height)] + \
                       [["3" for i in range(self.map_width)] for j in range(self.grass_block_height)] + \
                       [["1" for i in range(self.map_width)] for j in range(self.soil_block_height)] + \
                       [["2" for i in range(self.map_width)] for j in range(self.ground_height)]
            for i in range(self.map_width):
                if i > 6 and i < self.map_width - 6:
                    plant_mountain = random.randint(0,self.mountain_probability)
                    if plant_mountain == 0 and self.map[self.terrain_high][i-1] != "5" and self.map[self.terrain_high][i-2] != "5":
                        self.mountain_generation(i)
            for i in range(self.map_width):
                if i > 3 and i < self.map_width - 3:
                    plant_tree = random.randint(0,self.common_tree_probability)
                    if plant_tree == 0 and self.map[self.terrain_high][i-1] != "5" and self.map[self.terrain_high][i-2] != "5":
                        self.tree_generation(i)
        elif type == 3:
            self.map = [["0" for i in range(self.map_width)] for j in range(self.map_height)]
            self.init_ground = 50
            for i in range(self.map_width):
                self.fill2(self.init_ground,self.map_height-1,i,"2")
                self.fill("1",(70-self.init_ground+1,i+1),(70-self.init_ground+2,i+1))
                self.fill("3",(70-self.init_ground,i+1))
                addition = random.randint(0,4)
                number = random.randint(1,2)
                if addition == 1:
                    if self.init_ground < self.map_height - self.tree_height[1] - 4:self.init_ground += number
                if addition == 2:
                    if self.init_ground > 2:self.init_ground -= number
            for i in range(self.map_width):
                if i > 3 and i < self.map_width - 1:
                    plant_tree = random.randint(0,self.common_tree_probability)
                    if plant_tree == 0 and self.map[self.terrain_high][i-1] != "5" and self.map[self.terrain_high][i-2] != "5":
                        self.tree_generation(i)
                
    def print_generation(self):
        for i in range(self.map_height):
            for j in range(self.map_width):
                if self.map[i][j] == "0":print("\033[48;2;50;233;223m\033[30m  ",end="")
                if self.map[i][j] == "2":print("\033[48;2;192;192;192m  ",end="")
                if self.map[i][j] == "5":print("\033[48;2;128;128;16m▒▒",end="")
                if self.map[i][j] == "3":print("\033[48;5;52m\033[38;5;118m▀▀",end="")
                if self.map[i][j] == "1":print("\033[48;5;52m  ",end="")
                if self.map[i][j] == "4":print("\033[48;2;64;192;32m  ",end="")
            print();time.sleep(0.3)
        print("\033[m")
_TerrainGeneration = TerrainGeneration()

class CommandParse(object):
    def __init__(self):
        self.order = ""
        
    def command_move(self,x,y):
        return x,y
        
    def command_parse(self,order):
        order = order.split(" ")
        if order[0] == "move":
            try:return self.command_move(order[1],order[2])
            except:tk_mb.showinfo("FreeWorld Pygame 2 提示","move指令有误！")
    
class MainPygameInterface(object):
    def __init__(self):
        pygame.init()
        self.screen_width = 900
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
        pygame.display.set_caption("FreeWorld Pygame 2 游戏主界面")
        self.icon_surface = pygame.image.load("游戏图标.png")
        pygame.display.set_icon(self.icon_surface)
        
        self.soil_block = pygame.image.load(r"./方块图片/土方块.png")
        self.stone_block = pygame.image.load(r"./方块图片/石方块.png")
        self.grass_block = pygame.image.load(r"./方块图片/草方块.png")
        self.leave_block = pygame.image.load(r"./方块图片/树叶方块.png")
        self.wood_block = pygame.image.load(r"./方块图片/木方块.png")
        self.sand_block = pygame.image.load(r"./方块图片/沙子方块.png")
        self.lava_block = pygame.image.load(r"./方块图片/岩浆方块.png")
        self.water_block = pygame.image.load(r"./方块图片/水方块.png")
        self.grass = pygame.image.load(r"./方块图片/草.png")
        self.no_block = pygame.image.load(r"./方块图片/无方块.png")
        self.player_generation_surface = pygame.image.load(r"./生成图片/地形生成封面.png")
        self.terrain_generation_surface = pygame.image.load(r"./生成图片/玩家生成封面.png")
        
        # self.game_name = _TypeInterface.game_name
        # self.player_name = _TypeInterface.player_name
        
        self.number_picturn_dict = {
            "0" : self.no_block,
            "1" : self.soil_block, 
            "2" : self.stone_block, 
            "3" : self.grass_block, 
            "4" : self.leave_block, 
            "5" : self.wood_block, 
            "6" : self.sand_block, 
            "7" : self.lava_block, 
            "8" : self.water_block, 
            "9" : self.grass 
        }
        
        self.game_version = [2,0,0] 
        self.no_collision = ["0","4","5"]
        
        self.x = 50
        self.y = _TerrainGeneration.map_height - 1
        while _TerrainGeneration.map[self.y][self.x] not in self.no_collision:self.y -= 1 
        self.hungry = 100 
        self.life = 100 
        self.thirsty = 100
        self.oxygen = 100
        self.offset_around = 0 
        self.offset_jump = 0 
        self.key_list = []
        
    def pygame_run(self):
        while True:
            for i in self.key_list:
                if i == 1:self.offset_around += 0.2
                if i == 2:self.offset_around -= 0.2
                if i == 3:self.offset_jump += 0.3
                if i == 4:self.offset_jump -= 0.3
                
            if int(self.offset_around) == 1:self.offset_around = 0;self.x -= 1
            elif int(self.offset_around) == -1:self.offset_around = 0;self.x += 1
            elif int(self.offset_jump) == 1:self.offset_jump = 0;self.y -= 1
            elif int(self.offset_jump) == -1:self.offset_jump = 0;self.y += 1
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:pygame.quit();sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.key_list.append(1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.key_list.append(2)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.key_list.append(3)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.key_list.append(4)
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.key_list.remove(1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.key_list.remove(2)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.key_list.remove(3)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.key_list.remove(4)
                        
            x = -100;addition1 = -3
            for i in range(int(self.screen_height/100+4)):
                y = -100;addition2 = -3
                for j in range(int(self.screen_width/100+2)):
                    try:
                        if self.y < 3 and self.y > self.map_height+2:
                            self.screen.blit(self.number_picturn_dict["0"],(x+self.offset_around*100,y+self.offset_jump*100))
                        else:self.screen.blit(self.number_picturn_dict[_TerrainGeneration.map[self.y+addition2][self.x+addition1]],(x+self.offset_around*100,y+self.offset_jump*100))
                    except:self.screen.blit(self.number_picturn_dict["0"],(x+self.offset_around*100,y+self.offset_jump*100))
                    y += 100;addition2 += 1
                x += 100;addition1 += 1
                    
            pygame.display.flip()
                
class GameUpdateInterface(object):
    def __init__(self):
        self.name = "GameUpdateInterface"
        self.windows = tk.Tk()
        self.windows.title("FreeWorld Mygame 2 更新内容")
        self.windows.resizable(False,False)
        self.windows.geometry("460x270+0+0")
        self.GameUpdateInterface_photo = tk.PhotoImage(file="游戏图标.png")
        
        self.GameUpdateInterface_lable = tk.Label(self.windows,text=update_info)
        self.GameUpdateInterface_lable.pack()

    def tk_run(self):self.windows.mainloop()

class TypeInterface(object):
    def __init__(self):
        self.name = "TypeInterface"
        self.windows = tk.Tk()
        self.windows.title("FreeWorld Pygame 2 游戏设置")
        self.windows.resizable(False,False)
        self.TypeInterface_photo = tk.PhotoImage(file="游戏图标.png")
        
        self.number_type_dict = {
            "超平坦模式" : 1,
            "正常模式（推荐）" : 2,
            "陡峭模式" : 3,
        }
        
        self.number_game_dict = {
            "玩家模式（推荐）" : 1,
            "信任者模式" : 2,
            "测试模式" : 3
        }
        
        self.terrain_type_text = tk.StringVar()
        self.game_type_text = tk.StringVar()
        self.player_name_label = tk.Label(self.windows,text="设置玩家名称：")
        self.player_name_label.pack()
        self.player_name_entry = tk.Entry(self.windows)
        self.player_name_entry.insert(0, "请输入：")
        self.player_name_entry.pack()
        
        self.game_name_label = tk.Label(self.windows,text="设置游戏名称：")
        self.game_name_label.pack()
        self.game_name_entry = tk.Entry(self.windows)
        self.game_name_entry.insert(0, "请输入：")
        self.game_name_entry.pack()
        
        self.terrain_type_label = tk.Label(self.windows,text="设置地形：")
        self.terrain_type_label.pack()
        self.terrain_type_combobox = Combobox(self.windows,values=["正常模式（推荐）", "超平坦模式","陡峭模式"],textvariable = self.terrain_type_text,state="readonly")
        self.terrain_type_combobox.pack()
        
        self.game_type_label = tk.Label(self.windows,text="设置游戏类型：")
        self.game_type_label.pack()
        self.game_type_combobox = Combobox(self.windows,values=["玩家模式（推荐）", "信任者模式", "测试模式"],textvariable = self.game_type_text,state="readonly")
        self.game_type_combobox.pack()
        
        self.finish_button = tk.Button(self.windows,text="完成设置",command=self.finish_button_command)
        self.finish_button.pack()

    def finish_button_command(self):
        if self.terrain_type_text.get() == "":tk_mb.showinfo("FreeWorld Pygame 2 提示","地形类型不得为空")
        elif self.game_type_text.get() == "":tk_mb.showinfo("FreeWorld Pygame 2 提示","游戏类型不得为空")
        else:
            self.player_name = self.player_name_entry.get()
            self.world_name = self.game_name_entry.get()
            _TerrainGeneration.terrain_generation(self.number_type_dict[self.terrain_type_text.get()])
            _MainPygameInterface = MainPygameInterface()
            self.windows.destroy()
            _MainPygameInterface.pygame_run()
        
    def tk_run(self):self.windows.mainloop()
        
class ChooseInterface(object):
    def __init__(self):
        self.name = "ChooseInterface"
        self.windows = tk.Tk()
        self.windows.title("FreeWorld Pygame 2 游戏选项")
        self.windows.geometry("1000x746+0+0")
        self.windows.resizable(False,False)
        self.ChooseInterface_photo = tk.PhotoImage(file="游戏封面.png")
        self.ChooseInterface_image = tk.Label(self.windows,image=self.ChooseInterface_photo)
        self.ChooseInterface_image.grid(row=0,column=0)
        self.windows.iconphoto(True,tk.PhotoImage(file="游戏图标.png"))
        
        self.begin_button = tk.Button(self.windows,text="开始冒险吧",height=2,width=13,font=("44"),command=self.begin_button_command)
        self.update_button = tk.Button(self.windows,text="游戏更新内容",height=2,width=13,font=("18"),command=self.update_button_command)
        self.begin_button.place(x=438,y=330)
        self.update_button.place(x=438,y=430)

    def begin_button_command(self):
        self.windows.destroy()
        _TypeInterface = TypeInterface()
        _TypeInterface.tk_run()

    def update_button_command(self):
        _GameUpdateInterface = GameUpdateInterface()
        _GameUpdateInterface.tk_run()

    def tk_run(self):self.windows.mainloop()

_ChooseInterface = ChooseInterface()
_ChooseInterface.tk_run()       
