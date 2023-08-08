# Copyright [C] 2023 P.O Cream(浅),XiaoXuan and all contributors
# All right Reserved

#     Distributed under GPL license
#     See copy at https://opensource.org/licenses/GPL-3.0
# FreeWorld Pygame 2.0 is the rebuild version of FreeWorld
# It is based on Pygame and Tkinter

import time                    
import os
import sys
import random
import pygame
import tkinter as tk
from PIL import *
from tkinter.ttk import Combobox
import tkinter.messagebox as tk_mb

update_info = """FreeWorld Pygame-创世 更新内容
1.代码
·   重构了全部代码并删除了注释
·   规范了命名：
    -·所有类名使用驼峰命名法
    -·所有函数名和变量名全小写，词之间使用_隔开
2.地形
·   重构了整个地形生成模块并放入类TerrainGeneration中
·   加入了两种模式：超平坦模式&正常模式
3.UI
·   使用tkinter作为开头配置选择的UI
·   使用pygame作为游戏主题的UI

如您所见，我们对整个游戏进行重构，接下来这个版本与FreeWorld终端会分开更新
即两个版本没有任何关系，我们期待FreeWorld Pygame的下一次更新！"""

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
        self.leave_probability = 4
        self.tree_height = [5,7]
    
    # @copyright Copyright [C] Xiaoxuan 2023
    def fill(self,change_value,*coordinate):
        for i in coordinate:
            self.map[i[0]-1][i[1]-1] = change_value
            
    def fill2(self,height,x,y,change_value):
        for i in range(height):
            self.map[x][y] = change_value
            x -= 1
    
    def plant_tree(self):
        for i in range(self.map_width):
            if i > 1 and i < self.map_width - 3:
                plant_tree = random.randint(0,self.common_tree_probability)
                if plant_tree == 0 and self.map[29][i-1] != "5" and self.map[29][i-2] != "5":
                    tree_height = random.randint(self.tree_height[0],self.tree_height[1])
                    self.fill2(tree_height,self.sky_height-1,i,"5")
                    tree_leave = random.randint(0,self.leave_probability)
                    if tree_leave == 0:
                        self.fill(
                            "4",
                            (29-tree_height+1,i+1),(29-tree_height,i+1),(29-tree_height+-1,i+1),
                            (29-tree_height+1,i),(29-tree_height+1,i+2),
                            (29-tree_height+1,i+3),(29-tree_height+1,i-1),
                            (29-tree_height,i+2),(29-tree_height,i)
                            )
                    if tree_leave == 1:
                        self.fill(
                            "4",
                            (29-tree_height+1,i+1),(29-tree_height,i+1),(29-tree_height-1,i+1),
                            (29-tree_height+1,i),(29-tree_height+1,i+2),
                            (29-tree_height+1,i+3),(29-tree_height+2,i+2),
                            (29-tree_height,i+2),(29-tree_height,i)
                            )
                    if tree_leave == 2:
                        self.fill(
                            "4",
                            (29-tree_height+1,i+1),(29-tree_height,i+1),(29-tree_height-1,i+1),
                            (29-tree_height+1,i),(29-tree_height+1,i+2),
                            (29-tree_height+1,i+3),(29-tree_height+2,i),
                            (29-tree_height,i+2),(29-tree_height,i)
                            )
                    if tree_leave == 3:
                        self.fill(
                            "4",
                            (29-tree_height+1,i+1),(29-tree_height,i+1),(29-tree_height-1,i+1),
                            (29-tree_height+1,i),(29-tree_height+1,i+2),
                            (29-tree_height+1,i+3),(29-tree_height+2,i),(29-tree_height+2,i+2),
                            (29-tree_height,i+2),(29-tree_height,i)
                            )
                    if tree_leave == 4:
                        self.fill(
                            "4",
                            (29-tree_height+1,i+1),(29-tree_height,i+1),(29-tree_height+-1,i+1),
                            (29-tree_height+1,i),(29-tree_height+1,i+2),
                            (29-tree_height+1,i+3),(29-tree_height+1,i-1),
                            (29-tree_height,i+2),(29-tree_height,i),
                            (29-tree_height,i+2),(29-tree_height-1,i+2)
                            )
    def terrain_generation(self,type):
        if type == 1:
            self.map = [["0" for i in range(self.map_width)] for j in range(self.sky_height)] + \
                       [["3" for i in range(self.map_width)] for j in range(self.grass_block_height)] + \
                       [["1" for i in range(self.map_width)] for j in range(self.soil_block_height)] + \
                       [["2" for i in range(self.map_width)] for j in range(self.ground_height)]
            self.plant_tree()
                
        else:
            self.map = [["0" for i in range(self.map_width)] for j in range(self.map_height)]
            self.init_ground = 50
            for i in range(self.map_width):
                self.fill2(self.init_ground,self.map_height-1,i,"2")
                self.fill("1",(70-self.init_ground+1,i+1),(70-self.init_ground+2,i+1))
                self.fill("3",(70-self.init_ground,i+1))
                addition = random.randint(0,4)
                number = random.randint(1,2)
                if addition == 1:
                    if self.init_ground < self.map_height-2:
                        self.init_ground += number
                if addition == 2:
                    if self.init_ground > 2:
                        self.init_ground -= number
                
    def print_generation(self):
        for i in range(self.map_height):
            for j in range(self.map_width):
                if self.map[i][j] == "0":print("\033[48;2;50;233;223m\033[30m  ",end="")
                if self.map[i][j] == "2":print("\033[48;2;64;192;32m  ",end="")
                if self.map[i][j] == "5":print("\033[48;2;128;128;16m▒▒",end="")
                if self.map[i][j] == "3":print("\033[48;5;52m\033[38;5;118m▀▀",end="")
                if self.map[i][j] == "1":print("\033[48;5;52m  ",end="")
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
        
        self.soil_block = pygame.image.load("土方块.png")
        self.stone_block = pygame.image.load("石方块.png")
        self.grass_block = pygame.image.load("草方块.png")
        self.leave_block = pygame.image.load("树叶方块.png")
        self.wood_block = pygame.image.load("木方块.png")
        self.sand_block = pygame.image.load("沙子方块.png")
        self.lava_block = pygame.image.load("岩浆方块.png")
        self.water_block = pygame.image.load("水方块.png")
        self.grass = pygame.image.load("草.png")
        self.no_block = pygame.image.load("无方块.png")
        self.player_generation_surface = pygame.image.load("地形生成封面.png")
        self.terrain_generation_surface = pygame.image.load("玩家生成封面.png")
        
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
        
        self.player_rect = pygame.rect()
        
    def pygame_run(self):
        while True:
            for i in self.key_list:
                if i == 1:self.offset_around += 0.3
                if i == 2:self.offset_around -= 0.3
                if i == 3:
                    for i in range(5):
                        self.offset_jump += 0.3
                    for i in range(5):
                        self.offset_jump -= 0.3
                
            if int(self.offset_around) == 1:
                self.offset_around = 0
                self.x -= 1
            elif int(self.offset_around) == -1:
                self.offset_around = 0
                self.x += 1
            elif int(self.offset_jump) == 1:
                self.offset_jump = 0
                self.y -= 1
            elif int(self.offset_jump) == -1:
                self.offset_jump = 0
                self.y += 1
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:pygame.quit();sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.key_list.append(1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.key_list.append(2)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.key_list.append(3)
                    # elif event.key == pygame.K_o:
                    #     ...
                    
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.key_list.remove(1)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.key_list.remove(2)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.key_list.remove(3)
                 
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
            "正常模式（推荐）" : 2
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
        self.terrain_type_combobox = Combobox(self.windows,values=["正常模式（推荐）", "超平坦模式"],textvariable = self.terrain_type_text,state="readonly")
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
        self.windows.iconphoto(True,tk.PhotoImage(file='游戏图标.png'))
        
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
