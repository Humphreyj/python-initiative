import time
import random
import tkinter as tk
from tkinter import SUNKEN, ttk
from tkinter.messagebox import showinfo
from characters import characters


class Tracker:
    def __init__(self):
        self.combatants = [*characters]
        self.new_mod = 0
        self.mods = [-8, -7, -6, -5, -4, -3, -2, -1,
                     0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.initiative = []

        def create_character_frames(characters):

            buttons = []
            delete_buttons = []
            
            for i in range(len(characters)):
                current_character = characters[i]
                frame_name = 'frame_' + current_character['name']
                char_frame = tk.Frame(self.left_column, name=frame_name)

                tk.Label(char_frame, text="Name").grid(row=0, column=0)
                tk.Label(char_frame, text=current_character['name']).grid(
                    row=1, column=0)
                tk.Label(char_frame, text="Modifier").grid(row=0, column=1)
                tk.Label(char_frame, text=current_character['modifier']).grid(
                    row=1, column=1)
                tk.Label(char_frame, text="Result").grid(row=0, column=2)
                tk.Label(char_frame, text="Active").grid(row=0, column=3)
                result_value = tk.Label(
                    char_frame, text=current_character['result'], name='result_value')
                # button
                buttons.append(tk.Button(char_frame, text=str(
                    current_character['active']), command=lambda c=i: toggle_active(c)))
                delete_buttons.append(tk.Button(
                    char_frame, text="Delete", command=lambda c=i: delete_character(c,frame_name)))
                # button

                result_value.grid(row=1, column=2)

                buttons[i].grid(row=1, column=3)
                delete_buttons[i].grid(row=1, column=4)
                char_frame.grid(row=i+1, column=0)

        def remove_from_initiative(search_term, list):
            list_copy = list.copy()
            for i, character in enumerate(list_copy): 
                if character['name'] == search_term:
                    frame_name = "frame_" + character['name']
                    self.right_column.children[frame_name].destroy()
                    del list_copy[i]
                    self.initiative = [*list_copy]

            update_turn_order([*self.initiative])

        def toggle_active(i):
            self.combatants[i]['active'] = not self.combatants[i]['active']
            self.combatants[i]['result'] = 0
            create_character_frames(self.combatants)

        def get_new_mod(selection):
            self.new_mod = selection

        def reset_combatants():
            for i in range(len(self.combatants)):
                self.combatants[i]['result'] = 0
                frame_name = "frame_"+self.combatants[i]['name']

                if frame_name in self.left_column.children:
                    self.left_column.children[frame_name].destroy()
                if frame_name in self.right_column.children:
                    self.right_column.children[frame_name].destroy()
            self.initiative = []
            self.combatants = [*characters]
            self.right_column.after(
                100, create_character_frames(self.combatants))
            

        self.root = tk.Tk()
        self.root.geometry('600x600')
        self.root.title('Trackerbot v1')

        #toolbar
        self.toolbar = tk.Frame(self.root, bd=1, relief=SUNKEN).grid(row=0, column=0)
        #reset characters button                        
        reset_button = tk.Button(
            self.toolbar, text="Reset Characters", bg='grey', command=reset_combatants)
        reset_button.grid(row=0, column=1, sticky=tk.NW)
        #reset characters button

        #edit characters button
        reset_button = tk.Button(
            self.toolbar, text="Edit Characters", bg='grey', command=reset_combatants)
        reset_button.grid(row=0, column=0, sticky=tk.W)
        #edit characters button
        #toolbar

        self.left_column = tk.Frame(self.root, bd=2, relief=SUNKEN)
        self.left_column.grid(row=1, column=0, sticky=tk.NW, padx=10, pady=10)

        self.right_column = tk.Frame(self.root, height=400)
        self.right_column.grid(row=1, column=1, sticky=tk.NE, padx=10, pady=10)

        header_right = tk.Label(self.right_column, text='Turn Order')
        header_right.grid(row=0, column=0, sticky=tk.W)

        # roll button
        roll_button = tk.Button(
            self.root, text="Roll it!", command=lambda: roll_dice(self.combatants, 20))
        roll_button.grid(row=len(self.combatants)+1, column=0, sticky=tk.S)
        # roll button

        #add new character
        self.add_character_menu = tk.Frame(self.root, bd=1, relief=SUNKEN, width=300,padx=10, pady=10)
        self.add_character_menu.grid(row=len(self.combatants)+2, column=0)
        tk.Label(self.add_character_menu,
                 text="New Character Name").grid(row=0, column=0)
        self.new_char_name = ttk.Entry(
            self.add_character_menu, textvariable=tk.StringVar())
        self.new_char_name.grid(row=1, column=0, sticky=tk.W)
        placeholder_mod = tk.StringVar(self.root)
        placeholder_mod.set(0)
        tk.Label(self.add_character_menu, text="Dex Mod").grid(row=0, column=1)
        mod_select = tk.OptionMenu(
            self.add_character_menu, placeholder_mod, *self.mods, command=get_new_mod)
        mod_select.grid(row=1, column=1)

        # add character button
        add_new_char_button = tk.Button(self.add_character_menu, text="Add Character",
                                        command=lambda: add_new_combatant(self.new_char_name.get(), self.new_mod))
        add_new_char_button.grid(row=2, column=0, sticky=tk.S)
        # add character button
        #add new character


        create_character_frames(self.combatants)

        def update_character_frames(characters):
            for character in characters:
                try:
                    frame_name = 'frame_' + character['name']

                    self.left_column.children[frame_name].children['result_value']['text'] = character['result']
                except:
                    print('No frame exists')

        def delete_character(i,frame_name):
            try:
                
                self.left_column.children[frame_name].destroy()
                del self.combatants[i]
                if frame_name in self.right_column.children:
                    self.right_column.children[frame_name].destroy()
                create_character_frames([*self.combatants])
            except:
                print('Something broke when deleting character.')
            
        def add_new_combatant(name, mod):
            new_combatant = {
                id: len(characters),
                "name": name,
                "modifier": mod,
                "result": 0,
                "active": True
            }
            if name:
                self.combatants.append(new_combatant)
                self.new_char_name.delete(0, "end")
                create_character_frames(self.combatants)
            else:
                self.new_char_name.insert(0,"You need to enter a name")
                # time.sleep(1.5)
                self.new_char_name.after(1500,self.new_char_name.delete(0, "end"))

        def update_turn_order(initiative):
            remove_buttons = []
            for i in range(len(initiative)):
                current_character = initiative[i]
                frame_name = 'frame_' + current_character['name']
                char_frame = tk.Frame(
                    self.right_column, name=frame_name, width=300, bd=1, relief=SUNKEN)
                remove_buttons.append(tk.Button(char_frame, text="Delete", command=lambda c=i: remove_from_initiative(
                    initiative[c]['name'], initiative)))
                if current_character['active']:
                    char_frame.grid(row=i+1, column=0, padx=5,
                                    pady=5, sticky=tk.W)
                    tk.Label(char_frame, text=current_character['name'], name="result" +
                             current_character['name']).grid(row=0, column=0, sticky=tk.W)
                    remove_buttons[i].grid(row=0, column=1, sticky=tk.E)

        def roll_dice(characters, sides):
            for character in characters:
                if character['active']:
                    modifier = character['modifier']
                    roll = random.randint(1, sides)
                    result = roll + int(modifier)

                    character['result'] = result
            update_character_frames(self.combatants)

            self.initiative = sorted(
                self.combatants, key=lambda i: i['result'], reverse=True)
            last = {
                "name": 0,
                "result": 0,
                "modifier": 0
            }
            initiative_copy = self.initiative.copy()
            for i, item in enumerate(initiative_copy):
                
                if last['result'] == self.initiative[i]["result"]:
                    # print('There is a tie between ' +
                    #     last['name'] + ' and ' + self.initiative[i]['name'])
                    last_result = random.randint(
                        1, sides) + last['modifier']
                    time.sleep(0.25)
                    current_result = random.randint(
                        1, sides) + self.initiative[i]['modifier']
                    # print(last['name'], last_result, item['name'],
                    #     current_result)
                    
                    if last_result > current_result:
                        print(last['name'] + " (last) wins the tie")
                        try:
                            initiative_copy[i+1], initiative_copy[i] = initiative_copy[i+1], initiative_copy[i]
                        except Exception as e:
                            print("problem swapping homies when last wins." + "\n" +str(e))
                            
                    else:
                        print(self.initiative[i]['name'] + " wins the tie")
                        try:
                             initiative_copy[i-1], initiative_copy[i] = initiative_copy[i], initiative_copy[i-1]
                        except Exception as e:
                            print('There was a problem swapping homies.'+ "\n" + str(e))
                else:
                    last = item
            self.initiative = initiative_copy
            update_turn_order(self.initiative)
        self.root.mainloop()


Tracker()
