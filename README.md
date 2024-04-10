# Recipe Manager

Recipe Manager is a python project that can store, retrieve, update, and delete recipes, using an SQLite database.

## Repo Contents

The main files in this repository are:

- `DB.py`: This file contains the `DB` class, which is responsible for managing the database connection and running the SQL queries.
- `RecipeManager.py`: This file contains the `RecipeManager` class, which inherits from the `DB` class and provides the requisite methods for managing recipes.
- `InteractiveMenu.py`: This is the main file that should be run to test the implementation. It provides the user with an interactive menu for managing the database of recipes, `recipes.db`.
- `recipes.txt`: This is a text file that can be used to populate the DB with an assortment of recipes. Recipes are delimited with a `|` character, and the ingredients fields are separated by a `:` character. The fields are as follows: Recipe Name, Category, Description, Ingredients. For example:
    - Spaghetti and Meatballs|Dinner|Simmer meatballs in marinara sauce, serve over cooked pasta.|Pasta: 400g, Ground Beef: 500g, Bread Crumbs: 1/2 cup, Egg: 1, Tomato Sauce: 2 cups


## How to Run

1. Clone the repository (OR download the zip file and extract the contents)
```
git clone https://github.com/jcall84/RecipeMaker.git
```
2. Navigate to the project directory
```
cd RecipeMaker-main
```
3. Run the `InteractiveMenu.py` file (using Python 3)
```
python InteractiveMenu.py
```

## Expected Outputs

When you run the `InteractiveMenu.py` file, it will interact with the SQLite database to manage recipes. You can add, update, delete, and retrieve recipes. 

*Sample run:*
```
python InteractiveMenu.py 

        Recipe Manager Menu
        1. Add Recipe
        2. Update Recipe
        3. Delete Recipe
        4. List Recipes by Category
        5. List Recipes by Ingredient
        6. List All Recipes
        7. List All Categories
        8. Populate Database from File
        9. Reset/Initialize Database
        0. Exit
        
Enter your choice: 
```
