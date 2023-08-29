# Create a button to add recipes
btn_add_recipe = customtkinter.CTkButton(master=frame, text='Add Recipe', command=add_recipe,fg_color="#0C62D7")
btn_add_recipe.pack(padx=10,pady=10)