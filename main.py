import time
import random
import tkinter as tk
from tkinter.messagebox import showinfo
from characters import characters


def toggle_active(i):

  characters[i]['active'] = not characters[i]['active']
  characters[i]['result'] = 0
  
  print(characters[i])
  create_character_frames(characters)

def delete_character(i,char_frame):
  
  del characters[i]
  char_frame.destroy()
  create_character_frames(characters)
buttons = []
delete_buttons = []
def create_character_frames(characters):
  for i in range(len(characters)):
    current_character = characters[i]
    frame_name = 'frame_' + current_character['name']
    char_frame = tk.Frame(left_column, name=frame_name)
    
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
    
def update_character_frames(characters):
  for i in range(len(characters)):
    current_character = characters[i]
    frame_name = 'frame_' + current_character['name']
    
    left_column.children[frame_name].children['result_value']['text'] = current_character['result']
  # print(left_column.winfo_children()[0].winfo_children()[-1])
def update_turn_order(initiative):
  for i in range(len(initiative)):
    if initiative[i]['active']:
   
      tk.Label(turn_order,text=initiative[i]['name'], name= "result" + initiative[i]['name']).grid(row=i+1, column=0)

def roll_dice(characters, sides):
  for character in characters:
    if character['active']:
      modifier = character['modifier']
      roll = random.randint(1,sides)
      result = roll + int(modifier)
      character['result'] = result
  # create_character_frame(characters)
  update_character_frames(characters)
  
  initiative = sorted(characters, key = lambda i: i['result'], reverse=True)
  update_turn_order(initiative)
  
  
  
  


# create the root window
root = tk.Tk()
root.geometry('500x500')
root.title('Trackerbot v1')

left_column = tk.Frame(root)
left_column.grid(row=0, column=1,sticky=tk.NW)
turn_order = tk.Frame(root)
turn_order.grid(row=0, column=2,sticky=tk.NE)
tk.Label(turn_order, text="Turn Order").grid(row=0, column=0)


#button
roll_button = tk.Button(root, text="Roll it!", command=lambda: roll_dice(characters,20))
#button

create_character_frames(characters)



mods = (1,2,3,4,5,6,7,8,9,10,11,12)

var = tk.StringVar(value=dir(tk))
var.set(mods)


# lb.grid(row=1, column = 0)

roll_button.grid(row=len(characters)+1, column=1,sticky=tk.S)
# lb.bind('<<ListboxSelect>>', clickEvent)




root.mainloop()
