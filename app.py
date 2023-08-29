import sqlite3
from tkinter import Tk, Label, Entry, Text, Button, Listbox, Scrollbar, Toplevel, ttk
import customtkinter


# Create a connection to the database
conn = sqlite3.connect('recipes.db')
cursor = conn.cursor()

# Create the recipes table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS recipes (
        recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recipe_name TEXT,
        ingredients TEXT,
        instructions TEXT
    )
''')
conn.commit()

def add_recipe():
    recipe_name = entry_recipe_name.get()
    ingredients = text_ingredients.get("1.0", "end-1c")
    instructions = text_instructions.get("1.0", "end-1c")

    # Call the backend function to add the recipe
    cursor.execute('''
        INSERT INTO recipes (recipe_name, ingredients, instructions)
        VALUES (?, ?, ?)
    ''', (recipe_name, ingredients, instructions))
    conn.commit()

    # Clear the entry fields and text areas
    entry_recipe_name.delete(0, 'end')
    text_ingredients.delete("1.0", "end")
    text_instructions.delete("1.0", "end")

    # Refresh the recipe list
    refresh_recipe_list()


def delete_recipe():
    selected_recipe = recipe_listbox.get(recipe_listbox.curselection())
    recipe_id = selected_recipe.split(':')[0]
    cursor.execute('''
        DELETE FROM recipes WHERE recipe_id = ?
    ''', (recipe_id,))
    conn.commit()

    # Refresh the recipe list
    refresh_recipe_list()

def get_recipes():
    cursor.execute('''
        SELECT recipe_id, recipe_name FROM recipes
    ''')
    return cursor.fetchall()

def view_recipe(event):
    selected_recipe = recipe_listbox.get(recipe_listbox.curselection())

    recipe_id = selected_recipe.split(':')[0]
    cursor.execute('''
        SELECT * FROM recipes WHERE recipe_id = ?
    ''', (recipe_id,))
    recipe = cursor.fetchone()

    recipe_name = recipe[1]
    ingredients = recipe[2]
    instructions = recipe[3]

    # Open a new window to view the recipe
    view_window = Toplevel(window)
    view_window.title('View Recipe')
    view_window.geometry('450x450')

    # Style the view window
    view_window.configure(bg='#f0f0f0')

    lbl_recipe_name = Label(view_window, text='Recipe Name:', bg='#f0f0f0', font=('Arial', 12, 'bold'))
    lbl_recipe_name.pack()
    lbl_recipe_name_value = Label(view_window, text=recipe_name, bg='#f0f0f0', font=('Arial', 12))
    lbl_recipe_name_value.pack()

    lbl_ingredients = Label(view_window, text='Ingredients:', bg='#f0f0f0', font=('Arial', 12, 'bold'))
    lbl_ingredients.pack()
    text_ingredients_value = Text(view_window, height=6, width=30, bg='#ffffff', relief='flat', font=('Arial', 11))
    text_ingredients_value.insert("end", ingredients)
    text_ingredients_value.pack()

    lbl_instructions = Label(view_window, text='Instructions:', bg='#f0f0f0', font=('Arial', 12, 'bold'))
    lbl_instructions.pack()
    text_instructions_value = Text(view_window, height=10, width=30, bg='#ffffff', relief='flat', font=('Arial', 11))
    text_instructions_value.insert("end", instructions)
    text_instructions_value.pack()

def refresh_recipe_list():
    recipe_listbox.delete(0, 'end')
    recipes = get_recipes()
    for recipe in recipes:
        recipe_listbox.insert('end', f'{recipe[0]}: {recipe[1]}')
button_mode=True
def switch_theme():
    current_theme = customtkinter.get_appearance_mode()
    if current_theme == "dark" and button_mode:
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")
        button_mode = False
    else:
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        button_mode=True

    

# Create the main window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
window = customtkinter.CTk()
window.title('Recipe Organizer')
window.configure(bg='#f0f0f0')
window.geometry("500x800")


switch_1 = customtkinter.CTkSwitch(window,command=switch_theme,text='Switch Theme')
switch_1.pack(pady=10, padx=10)

frame = customtkinter.CTkFrame(master = window)
frame.pack(pady = 20,padx=20,fill = "y",expand=True)

 


# Create labels and entry fields for recipe details
lbl_recipe_name = customtkinter.CTkLabel(master=frame, text='Recipe Name:', fg_color="transparent")
lbl_recipe_name.pack()
entry_recipe_name = customtkinter.CTkEntry(master=frame,fg_color="transparent")
entry_recipe_name.pack()



# Create a label and text area for ingredients
lbl_ingredients = customtkinter.CTkLabel(master=frame, text='Ingredients:',fg_color="transparent")
lbl_ingredients.pack()
text_ingredients = customtkinter.CTkTextbox(master=frame, height=100, width=300,fg_color="transparent",border_color="grey",border_spacing=5,border_width=1)
text_ingredients.pack(padx=5,pady=10)


# Create a label and text area for instructions
lbl_instructions = customtkinter.CTkLabel(master=frame, text='Instructions:' )
lbl_instructions.pack()
text_instructions = customtkinter.CTkTextbox(master=frame,height=300, width=300,border_color="grey",border_width=1)
text_instructions.pack(padx=10,pady=10)


# Create a listbox to display recipes
lbl_listbox = customtkinter.CTkLabel(master = frame,text = 'SAVED RECIPES:',anchor = 'w')
lbl_listbox.pack(pady=10)
recipe_listbox = Listbox(master=frame, width=40,bg="#3A3B3C",fg="white")
recipe_listbox.pack(side="left", fill="y")

# Create a scrollbar for the listbox
scrollbar = customtkinter.CTkScrollbar(master=frame)
scrollbar.pack(side="right", fill="y")

# Connect the scrollbar to the listbox
recipe_listbox.config(yscrollcommand=scrollbar.set)
scrollbar.configure(command=recipe_listbox.yview)

# Bind the listbox to the view_recipe function
recipe_listbox.bind('<<ListboxSelect>>', view_recipe)

# Refresh the recipe list
refresh_recipe_list()


# Create a button to add recipes
btn_add_recipe = customtkinter.CTkButton(master=frame, text='Add Recipe', command=add_recipe,fg_color="#0C62D7")
btn_add_recipe.pack(padx=10,pady=10)



btn_delete_recipe = customtkinter.CTkButton(master=frame,text='Delete Recipe', command=delete_recipe,fg_color="red")
btn_delete_recipe.pack(padx=10,pady=10)




# Start the main event loop
window.mainloop()
