import RecipeManager

class InteractiveMenu:
    """Interactive menu for the Recipe Manager."""
    def __init__(self):
        """Initialize the Recipe Manager."""
        self.manager = RecipeManager.RecipeManager()

    def display_menu(self):
        """Display the menu options."""
        print("""
        *************************
        Recipe Manager Menu
            1. Add Recipe
            2. Update Recipe
            3. Delete Recipe
            4. List Recipe by ID
            5. List Recipes by Category
            6. List Recipes by Ingredient
            7. List All Recipes
            8. List All Categories
            9. Populate Database from File
            10. Reset/Initialize Database 
            11. Exit
        *************************
        """)

    def add_recipe(self):
        """Add a new recipe to the DB."""
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
        print(f"Recipe {name} added successfully!")

    def update_recipe(self):
        """Update an existing recipe in the DB. Can update various fields or none at all."""
        recipe_id = int(input("Enter recipe ID to update: "))
        name = input("Enter new name (leave blank to keep current): ")
        category = input("Enter new category (leave blank to keep current): ")
        instructions = input("Enter new instructions (leave blank to keep current): ")
        self.manager.update_recipe(recipe_id, name, category, instructions)
        print("Recipe updated successfully!")

    def delete_recipe(self):
        """Delete a recipe from the DB, referencing the recipe ID."""
        recipe_id = int(input("Enter recipe ID to delete: "))
        self.manager.delete_recipe(recipe_id)

    def list_recipe_by_id(self):
        """List a recipe by its ID."""
        recipe_id = int(input("Enter recipe ID to list: "))
        recipe = self.manager.get_recipe_by_id(recipe_id)
        if recipe:
            print(f"Recipe: {recipe['recipe'][1]}")
            print("Ingredients:")
            for ingredient in recipe['ingredients']:
                print(f"  - {ingredient[0]}: {ingredient[1]}")
            print(f"Instructions: {recipe['recipe'][3]}")
        else:
            print(f"No recipe found with ID {recipe_id}.")

    def list_recipes_by_category(self):
        """List all recipes in a specific category."""
        print("Categories:", self.manager.list_all_categories())
        category = input("Enter category to list: ")
        recipes = self.manager.list_recipes_by_category(category)
        if recipes:
            for recipe in recipes:
                print(f"{recipe[0]}: {recipe[1]}")
        else:
            print(f"No recipes found in the category {category}.")

    def list_recipes_by_ingredient(self):
        """List all recipes that contain a specific ingredient."""
        ingredient = input("Enter ingredient to list: ")
        recipes = self.manager.get_recipe_by_ingredient(ingredient)
        if recipes:
            for recipe in recipes:
                print(f"{recipe[0]}: {recipe[1]}")
        else:
            print(f"No recipes found that contain the ingredient {ingredient}.")

    def list_all_recipes(self):
        """List all recipes in the DB, including output of ingredients, instructions, recipe ID, and category."""
        recipes = self.manager.list_all_recipes_with_ingredients()
        if recipes:
            for recipe in recipes:
                print(f"\n{recipe['name']} (ID: {recipe['id']}, Category: {recipe['category']})")
                for ingredient in recipe['ingredients']:
                    print(f"  - {ingredient}")
                print(f"Instructions: {recipe['instructions']}")
        else:
            print("No recipes found.")

    def populate_database_from_file(self, filename):
        """Populates the database with recipes, categories, ingredients from a file."""
        try: # Handle exceptions in opening the file.
            with open(filename, "r") as file:
                for line in file:
                    data = line.strip().split("|")
                    name, category, instructions, *ingredients = data # This is a way to unpack the list by using the asterisk
                    ingredients = ingredients[0].split(",")
                    ingredients = [{'name': ingredient.split(":")[0].strip(), 'quantity': ingredient.split(":")[1].strip()} for ingredient in ingredients]
                    self.manager.add_recipe(name, category, instructions, ingredients)
            print("Database populated successfully!")
        except FileNotFoundError:
            print(f"File {filename} not found.")

    def list_all_categories(self):
        """List all categories in the DB."""
        categories = self.manager.list_all_categories()
        print("Categories:")
        for category in categories:
            print(category)

    def run(self):
        """Run the interactive menu."""
        while True:
            self.display_menu()
            choice = input("Enter choice: ")
            if choice == '1':
                self.add_recipe()
            elif choice == '2':
                self.update_recipe()
            elif choice == '3':
                self.delete_recipe()
            elif choice == '4':
                self.list_recipe_by_id()
            elif choice == '5':
                self.list_recipes_by_category()
            elif choice == '6':
                self.list_recipes_by_ingredient()
            elif choice == '7':
                self.list_all_recipes()
            elif choice == '8':
                self.list_all_categories()
            elif choice == '9':
                self.populate_database_from_file(input("Enter filename: "))  # e.g. recipes.txt
            elif choice == '10':
                self.manager.reset_database()
            elif choice == '11':
                self.manager.close_db()
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    menu = InteractiveMenu()
    menu.run()

