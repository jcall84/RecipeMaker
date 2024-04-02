import tkinter as tk

from RecipeManager.RecipeMaker.RecipeManagerDB import RecipeManagerDB
from RecipeManagerUI import RecipeManagerUI

class Main:
    def __init__(self):
        self.recipe_db = RecipeManagerDB()

    def run_demo(self):
        print("Starting Recipe Manager Demo...\n")

        # Add some recipes
        print("Adding recipes...")
        self.recipe_db.add_recipe(
            name="Chocolate Cake",
            category="Dessert",
            instructions="Mix ingredients, bake for 45 minutes at 350 degrees.",
            ingredients=[{"name": "flour", "quantity": "2 cups"}, {"name": "sugar", "quantity": "1 cup"}, {"name": "cocoa powder", "quantity": "1/2 cup"}]
        )
        self.recipe_db.add_recipe(
            name="Beef Stew",
            category="Main Course",
            instructions="Brown beef, add vegetables and simmer for 4 hours.",
            ingredients=[{"name": "beef", "quantity": "1 lb"}, {"name": "carrots", "quantity": "3"}, {"name": "potatoes", "quantity": "2"}]
        )

        # List all Dessert recipes
        print("\nListing all Dessert recipes...")
        desserts = self.recipe_db.list_recipes_by_category("Dessert")
        for dessert in desserts:
            print(dessert)

        # Fetch and display a recipe by ID
        print("\nFetching the Chocolate Cake recipe by ID...")
        chocolate_cake = self.recipe_db.get_recipe_by_id(1)  # Assuming Chocolate Cake has ID 1
        print(chocolate_cake)

        # Update the Beef Stew recipe
        print("\nUpdating the Beef Stew recipe...")
        self.recipe_db.update_recipe(2, name="Hearty Beef Stew")  # Assuming Beef Stew has ID 2

        # Fetch and display the updated Beef Stew recipe
        print("\nFetching the updated Beef Stew recipe by ID...")
        beef_stew = self.recipe_db.get_recipe_by_id(2)  # Assuming Beef Stew has ID 2
        print(beef_stew)

        # Delete a recipe
        print("\nDeleting the Chocolate Cake recipe...")
        self.recipe_db.delete_recipe(1)  # Assuming Chocolate Cake has ID 1

        # List all recipes to confirm deletion
        print("\nListing all recipes to confirm deletion...")
        all_recipes = self.recipe_db.list_recipes_by_category("Dessert") + self.recipe_db.list_recipes_by_category("Main Course")
        for recipe in all_recipes:
            print(recipe)

        print("\nDemo complete.")


if __name__ == "__main__":
    demo = Main()
    demo.run_demo()

    root = tk.Tk()
    app = RecipeManagerUI(root)
    root.mainloop()
