import DB


class RecipeManager(DB.DB):
    def __init__(self, db_name="recipes.db"):
        super().__init__(db_name)
        self.create_tables()

    def create_tables(self):
        """Creates the tables 'categories', 'recipes', and 'ingredients' if they don't already exist."""
        self.execute_script("""
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL UNIQUE
            )
        """)
        self.execute_script("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                category_id INTEGER,
                instructions TEXT NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        """)
        self.execute_script("""
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
        self.execute_script("""
            INSERT OR IGNORE INTO categories (name) VALUES (?)
        """, (category,))
        self.execute_script("""
            SELECT id FROM categories WHERE name = ?
        """, (category,))
        category_id = self.cursor.fetchone()[0]
        self.execute_script("""
            INSERT INTO recipes (name, category_id, instructions) VALUES (?, ?, ?)
        """, (name, category_id, instructions))
        recipe_id = self.cursor.lastrowid
        for ingredient in ingredients:
            self.execute_script("""
                INSERT INTO ingredients (recipe_id, name, quantity) VALUES (?, ?, ?)
            """, (recipe_id, ingredient['name'], ingredient['quantity']))
        self.conn.commit()

    def get_recipe_by_id(self, recipe_id):
        """Fetches a recipe and its ingredients by ID."""
        self.execute_script("SELECT * FROM recipes WHERE id = ?", (recipe_id,))
        recipe = self.cursor.fetchone()
        self.execute_script("SELECT name, quantity FROM ingredients WHERE recipe_id = ?", (recipe_id,))
        ingredients = self.cursor.fetchall()
        return {"recipe": recipe, "ingredients": ingredients}

    def get_recipe_by_ingredient(self, ingredient):
        """Fetches a recipe by ingredient. Case-insensitive search."""
        self.execute_script("""
            SELECT r.* FROM recipes r
            JOIN ingredients i ON r.id = i.recipe_id
            WHERE LOWER(i.name) = LOWER(?) 
        """, (ingredient,))
        return self.cursor.fetchall()

    def update_recipe(self, recipe_id, name=None, category=None, instructions=None):
        """Updates recipe details based on user-provided details."""
        updates = []
        params = []
        if name:
            updates.append("name = ?")
            params.append(name)
        if category:
            try:
                self.execute_script("SELECT category FROM recipes")
                updates.append("category = ?")
                params.append(category)
            except Exception as e:
                print("The 'category' column does not exist in the 'recipes' table.")
        if instructions:
            updates.append("instructions = ?")
            params.append(instructions)
        params.append(recipe_id)
        if updates:
            self.execute_script(f"UPDATE recipes SET {', '.join(updates)} WHERE id = ?", params)
            self.conn.commit()
            print("Recipe updated successfully!")
        else:
            print("No updates provided.")

    def list_all_categories(self):
        """Lists all categories in the database."""
        self.execute_script("SELECT name FROM categories")
        return [row[0] for row in self.cursor.fetchall()]

    def delete_recipe(self, recipe_id):
        """Deletes a recipe and its associated ingredients."""
        # Check if recipe exists
        if self.execute_script("SELECT * FROM recipes WHERE id = ?", (recipe_id,)) == []:
            print("Recipe not found.")
            return
        else:
            self.execute_script("DELETE FROM ingredients WHERE recipe_id = ?", (recipe_id,))
            self.execute_script("DELETE FROM recipes WHERE id = ?", (recipe_id,))
            self.conn.commit()
            print("Recipe deleted successfully!")

    def list_recipes_by_category(self, category):
        """Lists all recipes within a specific category."""
        self.execute_script("""
            SELECT r.* FROM recipes r
            JOIN categories c ON r.category_id = c.id
            WHERE LOWER(c.name) = LOWER(?)
        """, (category,))
        return self.cursor.fetchall()

    def list_all_recipes_with_ingredients(self):
        """Lists all recipes and their ingredients from the database."""
        self.cursor.execute("""
        SELECT r.id, r.name, c.name as category, r.instructions, i.name, i.quantity
        FROM recipes r
        LEFT JOIN ingredients i ON r.id = i.recipe_id
        JOIN categories c ON r.category_id = c.id
        ORDER BY r.id
        """)
        rows = self.cursor.fetchall()

        recipes = {}
        for row in rows:
            recipe_id, name, category, instructions, ingredient_name, ingredient_quantity = row
            if recipe_id not in recipes:
                recipes[recipe_id] = {
                    "name": name,
                    "id": recipe_id,
                    "category": category,
                    "instructions": instructions,
                    "ingredients": []
                }
            if ingredient_name:  # Check if there are any ingredients for the recipe
                recipes[recipe_id]["ingredients"].append(f"{ingredient_name}: {ingredient_quantity}")

        # Convert the dictionary to a list of recipes for easier use
        return list(recipes.values())

    def reset_database(self):
        """Resets the database to its initial state."""
        self.execute_script("DROP TABLE IF EXISTS recipes")
        self.execute_script("DROP TABLE IF EXISTS ingredients")
        self.execute_script("DROP TABLE IF EXISTS categories")
        self.create_tables()
        print("Database reset successfully.")

