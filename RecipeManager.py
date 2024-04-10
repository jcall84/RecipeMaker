# Recipe Creator and Manager - Create a recipe application with ingredients
# and a put them in a recipe manager program that organizes them into categories like deserts,
# main courses or by ingredients like chicken, beef, soups, pies etc.


import sqlite3


class RecipeManagerDB:
    def __init__(self, db_name="recipes.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Creates the necessary tables if they don't already exist."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                instructions TEXT NOT NULL
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredients (
                id INTEGER PRIMARY KEY,
                recipe_id INTEGER,
                name TEXT NOT NULL,
                quantity TEXT NOT NULL,
                FOREIGN KEY (recipe_id) REFERENCES recipes (id)
            )
        """)
        self.conn.commit()

    def add_recipe(self, name, category, instructions, ingredients):
        """Adds a new recipe and its ingredients to the database."""
        self.cursor.execute("""
            INSERT INTO recipes (name, category, instructions) VALUES (?, ?, ?)
        """, (name, category, instructions))
        recipe_id = self.cursor.lastrowid
        for ingredient in ingredients:
            self.cursor.execute("""
                INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)
            """, (recipe_id, ingredient['name'], ingredient['quantity']))
        self.conn.commit()

    def get_recipe_by_id(self, recipe_id):
        """Fetches a recipe and its ingredients by ID."""
        self.cursor.execute("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        recipe = self.cursor.fetchone()
        self.cursor.execute("SELECT name, quantity FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        ingredients = self.cursor.fetchall()
        return {"recipe": recipe, "ingredients": ingredients}

    def update_recipe(self, recipe_id, name=None, category=None, instructions=None):
        """Updates recipe details based on provided information."""
        updates = []
        params = []
        if name:
            updates.append("name = ?")
            params.append(name)
        if category:
            updates.append("category = ?")
            params.append(category)
        if instructions:
            updates.append("instructions = ?")
            params.append(instructions)
        params.append(recipe_id)
        self.cursor.execute(f"UPDATE recipes SET {', '.join(updates)} WHERE id = ?", params)
        self.conn.commit()

    def delete_recipe(self, recipe_id):
        """Deletes a recipe and its associated ingredients."""
        self.cursor.execute("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        self.cursor.execute("DELETE FROM recipes WHERE id = ?", (recipe_id,))
        self.conn.commit()

    def list_recipes_by_category(self, category):
        """Lists all recipes within a specific category."""
        self.cursor.execute("SELECT * FROM recipes WHERE category = ?", (category,))
        return self.cursor.fetchall()

    def list_all_recipes_with_ingredients(self):
        """Lists all recipes and their ingredients from the database."""
        self.cursor.execute("""
        SELECT r.id, r.name, r.category, r.instructions, i.name, i.quantity
        FROM recipes r
        LEFT JOIN ingredients i ON r.id = i.recipe_id
        ORDER BY r.id
        """)
        rows = self.cursor.fetchall()

        recipes = {}
        for row in rows:
            recipe_id, name, category, instructions, ingredient_name, ingredient_quantity = row
            if recipe_id not in recipes:
                recipes[recipe_id] = {
                    "name": name,
                    "category": category,
                    "instructions": instructions,
                    "ingredients": []
                }
            if ingredient_name:  # Check if there are any ingredients for the recipe
                recipes[recipe_id]["ingredients"].append(f"{ingredient_name}: {ingredient_quantity}")

        # Convert the dictionary to a list of recipes for easier use
        return list(recipes.values())

    def close(self):
        """Closes the database connection."""
        self.conn.close()
