# Recipe Manager

This repository contains a Python project that manages recipes. It uses a SQLite database to store and retrieve recipes.

## Contents

The main files in this repository are:

- `DB.py`: This file contains the `DB` class, which is responsible for managing the database connection and executing SQL queries.
- `RecipeManager.py`: This file contains the `RecipeManager` class, which inherits from the `DB` class and provides methods for managing recipes.
- `InteractiveMenu.py`: This is the main file that should be run to test the implementation.

## How to Run

1. Clone the repository (OR download the zip file and extract the contents)
```
git clone https://github.com/jcall84/RecipeMaker.git
```
2. Navigate to the project directory
```
cd recipe-manager
```
3. Run the `InteractiveMenu.py` file
```
python InteractiveMenu.py
```

## Expected Outputs

When you run the `InteractiveMenu.py` file, it will interact with the SQLite database to manage recipes. You can add, update, delete, and retrieve recipes. The output will depend on the specific operations you perform.
```
