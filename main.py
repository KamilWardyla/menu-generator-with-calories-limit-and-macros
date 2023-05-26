import os
from dotenv import load_dotenv
from psycopg2 import ProgrammingError, connect
from pulp import *

load_dotenv()
user = os.environ["DB_USER"]
host = os.environ["HOST"]
password = os.environ["PASSWORD"]
db = os.environ["DB"]


class ValidateError(Exception):
    pass

def execute_sql(sql_code, *args):
    """
        Executes SQL code with the provided arguments and returns the results.

        Parameters:
            sql_code (str): The SQL code to be executed.
            *args: Variable number of arguments to be passed as parameters to the SQL code.

        Returns:
            list or str: The results of the SQL query as a list of tuples, or an error message as a string if an exception occurs.

        Raises:
            ProgrammingError: If an error occurs during the execution of the SQL code.

    """
    with connect(host=host, user=user, password=password, database=db) as conn:
        with conn.cursor() as cur:
            cur.execute(sql_code, args)
            try:
                results = cur.fetchall()
                return results
            except ProgrammingError as e:
                return f"Error {e}"


def validate_calories_and_macronutrients(calories, protein_grams, carbs_grams, fat_grams):
    """
    Validates if the total calorie count matches the calculated calories from the given macronutrient values.

    Parameters:
        calories (int): The total calorie count.
        protein_grams (float): The amount of protein in grams.
        carbs_grams (float): The amount of carbohydrates in grams.
        fat_grams (float): The amount of fat in grams.

    Returns:
        bool: True if the calculated calories match the provided total calorie count, otherwise raise ValidateError.

    """
    protein_kcal = protein_grams*4
    carbs_kcal = carbs_grams * 4
    fat_kcal = fat_grams * 9
    
    if calories == sum([protein_kcal, carbs_kcal, fat_kcal]):
        return True
    else:
        return False
        
        
def generate_day_menu(calories, protein, carbs, fat):
    """
    Validate data and if validator returns True generate daily menu
                  else: return validate_error
    
    Parameters:
        calories (int): The total calorie count.
        protein_grams (float): The amount of protein in grams.
        carbs_grams (float): The amount of carbohydrates in grams.
        fat_grams (float): The amount of fat in grams.

    Returns:
        string: daily menu or validate_error
    """
    
    if validate_calories_and_macronutrients(calories, protein, carbs, fat) != True:
        raise ValidateError("Somethings wrong with you macronutrients...count your macronutrients one more time")
   
    meals_dict = {}
    for x in execute_sql('SELECT * from recipies LIMIT 2100'):
        meals_dict[x[1]] = {'calories': x[2], 'protein': x[3], 'carbs': x[5], 'fat': x[4]}
    
    menu = {}
    daily_meals_list = []
    daily_calories = 0
    daily_protein = 0
    daily_fat = 0
    daily_carbs = 0
    
    
    prob = LpProblem('Meal', LpMaximize)
    
    
    meals = LpVariable.dicts('Meal', meals_dict, lowBound=0, cat=LpBinary)
    print(meals)
    
    
    prob += lpSum([meals_dict[meal] for meal in meals_dict])
    
    prob += lpSum([meals_dict[meal]['calories'] * meals[meal] for meal in meals_dict]) == calories
    prob += lpSum([meals_dict[meal]['protein'] * meals[meal] for meal in meals_dict]) >= protein
    prob += lpSum([meals_dict[meal]['fat'] * meals[meal] for meal in meals_dict]) == fat
    prob += lpSum([meals_dict[meal]['carbs'] * meals[meal] for meal in meals_dict]) == carbs
    
    prob.solve()
    
    for meal in meals_dict:
        if meals[meal].varValue == 1:
            menu[meal] = meals_dict[meal]
    
    for key, value in menu.items():
        daily_meals_list.append(f"{key} \n Calories: {value['calories']}kcal, Protein: {value['protein']}g, Fat: {value['fat']}g, Carbs: {value['carbs']}g \n")
        daily_calories += value['calories']
        daily_protein += value['protein']
        daily_fat += value['fat']
        daily_carbs += value['carbs']
    

    daily_result_string =  f"Total daily Calories: {daily_calories}, Total daily proteins: {daily_protein}g, Total daily fat: {daily_fat}g, Total daily carbs: {carbs}g \n"
    
    for n in daily_meals_list:
        daily_result_string += f"\n {n}"
    return  daily_result_string

def generate_days_menu(days, calories, protein, carbs, fat):
    """
    Validate data and if validator returns True generate menu
                  else: return validate_error
    
    Parameters:
        days (int): number of days for which the menu will be prepared
        calories (int): The total calorie count.
        protein_grams (float): The amount of protein in grams.
        carbs_grams (float): The amount of carbohydrates in grams.
        fat_grams (float): The amount of fat in grams.

    Returns:
        string: menu or ValidateError
    """
    result_string = ""
    for i in range(1, days + 1):
        daily_menu = generate_day_menu(calories, protein, carbs, fat)
        result_string += f"Day {i} {daily_menu}" 
    return result_string

if __name__ == "__main__":
    print(generate_days_menu(3, 2000, 70, 250, 80))