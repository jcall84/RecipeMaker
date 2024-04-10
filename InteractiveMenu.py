import sqlite3
import RecipeManager
class InteractiveMenu:
    def __init__(self):
        self.manager = RecipeManager.RecipeManager()

    def display_menu(self):
        print("""
        Recipe Manager Menu
        1. Add Recipe
        2. Update Recipe
        3. Delete Recipe
        4. List Recipes by Category
        5. List Recipes by Ingredient
        6. List All Recipes
        7. List All Categories
        0. Exit
        """)

    def add_recipe(self):
        name = input("Enter recipe name: ")
        category = input("Enter recipe category: ")
        instructions = input("Enter instructions: ")
        ingredients_count = int(input("How many ingredients? "))
        ingredients = []
        for _ in range(ingredients_count):
            ingredient_name = input("Enter ingredient name: ")
            quantity = input("Enter quantity: ")
            ingredients.append({'name': ingredient_name, 'quantity': quantity})
        self.manager.add_recipe(name, category, instructions, ingredients)
        print("Recipe added successfully!")

    def update_recipe(self):
        recipe_id = int(input("Enter recipe ID to update: "))
        name = input("Enter new name (leave blank to keep current): ")
        category = input("Enter new category (leave blank to keep current): ")
        instructions = input("Enter new instructions (leave blank to keep current): ")
        self.manager.update_recipe(recipe_id, name, category, instructions)
        print("Recipe updated successfully!")

    def delete_recipe(self):
        recipe_id = int(input("Enter recipe ID to delete: "))
        self.manager.delete_recipe(recipe_id)
        print("Recipe deleted successfully!")

    def list_recipes_by_category(self):
        category = input("Enter category to list: ")
        recipes = self.manager.list_recipes_by_category(category)
        if recipes:
            for recipe in recipes:
                print(f"{recipe[0]}: {recipe[1]} - {recipe[2]}")
        else:
            print("No recipes found in this category.")

    def list_recipes_by_ingredient(self):
        ingredient = input("Enter ingredient to list: ")
        recipes = self.manager.get_recipe_by_ingredient(ingredient)
        if recipes:
            for recipe in recipes:
                print(f"{recipe[0]}: {recipe[1]} - {recipe[2]}")
        else:
            print("No recipes found with this ingredient.")

    def list_all_recipes(self):
        recipes = self.manager.list_all_recipes_with_ingredients()
        if recipes:
            for recipe in recipes:
                print(f"\n{recipe['name']} (ID: {recipe['id']}, Category: {recipe['category']}):")
                for ingredient in recipe['ingredients']:
                    print(f"  - {ingredient}")
                print(f"Instructions: {recipe['instructions']}")
        else:
            print("No recipes found.")

    def list_all_categories(self):
        categories = self.manager.list_all_categories()
        print("Categories:")
        for category in categories:
            print(category)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.add_recipe()
            elif choice == '2':
                self.update_recipe()
            elif choice == '3':
                self.delete_recipe()
            elif choice == '4':
                self.list_recipes_by_category()
            elif choice == '5':
                self.list_recipes_by_ingredient()
            elif choice == '6':
                self.list_all_recipes()
            elif choice == '7':
                self.list_all_categories()
            elif choice == '0':
                self.manager.close()
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    menu = InteractiveMenu()
    menu.run()

