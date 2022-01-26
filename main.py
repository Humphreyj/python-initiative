import time
import random
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from characters import characters


class Tracker:
  def __init__(self):
    self.characters = characters
    self.combatants = [*characters]
    self.new_mod = None
    self.mods = [-5,-4,-3,-2,-1,0,1,2,3,4,5,6,7,8,9,10,11,12]

    def toggle_active(i):
      self.combatants[i]['active'] = not self.combatants[i]['active']
      self.combatants[i]['result'] = 0
      create_character_frames(self.combatants)
      
    def get_new_mod(selection):
      self.new_mod = selection
    
    def reset_combatants():
      for i in range(len(self.combatants)): 
        frame_name = "frame_"+self.combatants[i]['name']
        self.left_column.children[frame_name].destroy()
        
      self.combatants = characters
      create_character_frames(self.combatants)

    self.root = tk.Tk()
    self.root.geometry('600x600')
    self.root.title('Trackerbot v1')

    self.toolbar = tk.Frame(self.root).grid(row=0,column=0)
    b = tk.Button(self.toolbar, text="Reset", width=6, command= reset_combatants)
    b.grid(row=0,column=0)

    self.left_column = tk.Frame(self.root, width=300,borderwidth=5)
    self.left_column.grid(row=1, column=0,sticky=tk.NW)

    
    self.mid = tk.Frame(self.root, width=50,height=250, bg='grey')
    self.mid.grid(row=1,column=1)

    self.right_column = tk.Frame(self.root, width=200)
    self.right_column.grid(row=1, column=2,sticky=tk.NE)
    
    header_right = tk.Label(self.right_column, text='Turn Order')
    header_right.grid(row=0, column=0,sticky=tk.N)
    title = tk.Label(self.root,text='Trackerbot v1')
    title.grid(row=0, column=0,sticky=tk.NE)

    #button
    roll_button = tk.Button(self.root, text="Roll it!", command=lambda: roll_dice(self.combatants,20))
    roll_button.grid(row=len(self.combatants)+1, column=0,sticky=tk.S)
    #button

    new_char_name = ttk.Entry(self.root,textvariable=tk.StringVar())
    new_char_name.grid(row=len(self.combatants)+2, column=0,sticky=tk.S)
    placeholder_mod = tk.StringVar(self.root)
    placeholder_mod.set("Modifier")
    mod_select = tk.OptionMenu(self.root,placeholder_mod,*self.mods,command=get_new_mod)
    mod_select.grid(row=len(self.combatants)+3, column=0,sticky=tk.S)
    #button
    add_new_char_button = tk.Button(self.root, text="Add New Character", command=lambda: add_new_combatant(new_char_name.get(), self.new_mod))
    add_new_char_button.grid(row=len(characters)+4, column=0,sticky=tk.S)
    #button

    

    def create_character_frames(characters):
      buttons = []
      delete_buttons = []
      for i in range(len(characters)):
        
        current_character = characters[i]
        frame_name = 'frame_' + current_character['name']
        char_frame = tk.Frame(self.left_column, name=frame_name)
        
        tk.Label(char_frame, text="Name").grid(row=0,column=0)
        tk.Label(char_frame, text=current_character['name']).grid(row=1,column=0)
        tk.Label(char_frame, text="Modifier").grid(row=0,column=1)
        tk.Label(char_frame, text=current_character['modifier']).grid(row=1,column=1)
        tk.Label(char_frame, text="Result").grid(row=0,column=2)
        tk.Label(char_frame, text="Active").grid(row=0,column=3)
        result_value = tk.Label(char_frame, text=current_character['result'], name='result_value')
        #button
        buttons.append(tk.Button(char_frame, text=str(current_character['active']), command=lambda c=i: toggle_active(c)))
        delete_buttons.append(tk.Button(char_frame, text="Delete", command=lambda c=i: delete_character(c,char_frame)))
        #button
        
        result_value.grid(row=1,column=2)
      
        buttons[i].grid(row=1, column=3)
        delete_buttons[i].grid(row=1, column=4)
        char_frame.grid(row=i+1, column=0)

    create_character_frames(self.combatants)
    def update_character_frames(characters):
      for i in range(len(characters)):
        current_character = characters[i]
        frame_name = 'frame_' + current_character['name']
        
        self.left_column.children[frame_name].children['result_value']['text'] = current_character['result']

    def delete_character(i,char_frame):
      del self.combatants[i]
      char_frame.destroy()
      create_character_frames(self.combatants)
    
    def add_new_combatant(name,mod):
      new_combatant = {
        id: len(characters),
        "name": name,
        "modifier": mod,
        "result": 0,
        "active": True
      }
      self.combatants.append(new_combatant)
      create_character_frames(self.combatants)
    
    def update_turn_order(initiative):
      for i in range(len(initiative)):
        if initiative[i]['active']:
      
          tk.Label(self.right_column,text=initiative[i]['name'], name= "result" + initiative[i]['name']).grid(row=i+1, column=0)

    def roll_dice(characters, sides):
      for character in characters:
        if character['active']:
          modifier = character['modifier']
          roll = random.randint(1,sides)
          result = roll + int(modifier)
          character['result'] = result
      update_character_frames(self.combatants)
      
      initiative = sorted(self.combatants, key = lambda i: i['result'], reverse=True)
      update_turn_order(initiative)
    self.root.mainloop()
Tracker()

 
  

  
