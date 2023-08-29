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

def edit_recipe():
    selected_recipe = recipe_listbox.get(recipe_listbox.curselection())
    recipe_id = selected_recipe.split(':')[0]
    cursor.execute('''
        SELECT * FROM recipes WHERE recipe_id = ?
    ''', (recipe_id,))
    recipe = cursor.fetchone()

    recipe_name = recipe[1]
    ingredients = recipe[2]
    instructions = recipe[3]

    # Open a new window to edit the recipe
    edit_window = Toplevel(window)
    edit_window.title('Edit Recipe')
    edit_window.geometry('450x450')

    # Style the edit window
    edit_window.configure(bg='#f0f0f0')

    lbl_recipe_name = Label(edit_window, text='Recipe Name:', bg='#f0f0f0', font=('Arial', 12, 'bold'))
    lbl_recipe_name.pack()
    entry_recipe_name = Entry(edit_window, font=('Arial', 12))
    entry_recipe_name.insert(0, recipe_name)
    entry_recipe_name.pack()

    lbl_ingredients = Label(edit_window, text='Ingredients:', bg='#f0f0f0', font=('Arial', 12, 'bold'))
    lbl_ingredients.pack()
    text_ingredients_value = Text(edit_window, height=6, width=30, bg='#ffffff', relief='flat', font=('Arial', 11))
    text_ingredients_value.insert("end", ingredients)
    text_ingredients_value.pack()

    lbl_instructions = Label(edit_window, text='Instructions:', bg='#f0f0f0', font=('Arial', 12, 'bold'))
    lbl_instructions.pack()
    text_instructions_value = Text(edit_window, height=10, width=30, bg='#ffffff', relief='flat', font=('Arial', 11))
    text_instructions_value.insert("end", instructions)
    text_instructions_value.pack()

    def save_changes():
        new_recipe_name = entry_recipe_name.get()
        new_ingredients = text_ingredients_value.get("1.0", "end-1c")
        new_instructions = text_instructions_value.get("1.0", "end-1c")

        cursor.execute('''
            UPDATE recipes SET recipe_name = ?, ingredients = ?, instructions = ? WHERE recipe_id = ?
        ''', (new_recipe_name, new_ingredients, new_instructions, recipe_id))
        conn.commit()

        edit_window.destroy()

        # Refresh the recipe list
        refresh_recipe_list()

    save_button = Button(edit_window, text="Save Changes", command=save_changes)
    save_button.pack()

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

button_mode = True
def switch_theme():
    global button_mode
    current_theme = customtkinter.get_appearance_mode()
    if current_theme == "dark" and button_mode:
        customtkinter.set_appearance_mode("light")
        customtkinter.set_default_color_theme("green")
        button_mode = False
    else:
        customtkinter.set_appearance_mode("dark")
        customtkinter.set_default_color_theme("blue")
        button_mode = True

# Create the main window
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")
window = customtkinter.CTk()
window.title('Recipe Organizer')
window.configure(bg='#f0f0f0')
window.geometry("500x800")

switch_1 = customtkinter.CTkSwitch(window, command=switch_theme, text='Switch Theme')
switch_1.pack(pady=10, padx=10)
