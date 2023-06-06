# Menu Generator with calories limit

This script generates a daily menu based on the given calorie and macronutrient requirements. It uses linear programming optimization to select meals from a database of recipes that meet the specified criteria.

## Getting Started
To run this application, you will need to:
1. Clone the respository:
    ```
    git clone https://github.com/KamilWardyla/menu-generator-with-calories-limit-and-macros.git
    ```
2. Execute the command:
    ```
    pip install .
    ```
3. Create your database in PostgreSQL
4. Configure your own dontenv file with:
    ```
    DB_USER = your_username
    HOST = your_host
    PASSWORD = your_password
    DB = your_dbname
   PORT = your_port
    ```
5. Download recipies from:
https://www.kaggle.com/datasets/hugodarwood/epirecipes?resource=download

6. Run the first setup script to migrate data to the database:
    ```
    python migrate_data_to_database.py
    ```
## Usage
To generate a menu, run the script with the following command:
```
python main.py calories protein carbs fat days
```
Replace **calories**, **protein**, **carbs**, **fat**, and **days** with the desired values. The script will generate a menu for the specified number of days based on the given calorie and macronutrient requirements.

Example usage:
```
python main.py 2048 133 307 32 5
```
This command will genereate a menu for 5 days with a daily calorie requirement of 2048, protein requirement of 133 grams, carbohydrates 307 grams and fat requirement of 32 grams.
