import argparse

from pulp import *

from db_utils import execute_sql


class InvalidCaloriesAndMacrosError(Exception):
    pass


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
        
        
def generate_one_day_menu(calories, protein, carbs, fat, index_range = [0, 2100]):
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
    
    Raises:
        InvalidCaloriesAndMacrosError: If function validate_calories_and_macronutrients not return True
    """
    
    if validate_calories_and_macronutrients(calories, protein, carbs, fat) != True:
        raise InvalidCaloriesAndMacrosError("Somethings wrong with you macronutrients...count your macronutrients one more time")
   
    meals_dict = {}
    for x in execute_sql(f'SELECT * from recipies WHERE id > {index_range[0]} and id < {index_range[1]}'):
        meals_dict[x[1]] = {'calories': x[2], 'protein': x[3], 'carbs': x[5], 'fat': x[4]}
    menu = {}
    daily_meals_list = []
    daily_calories = 0
    daily_protein = 0
    daily_fat = 0
    daily_carbs = 0
    
    
    #Minimalize number of meals
    prob = LpProblem('Meal', LpMinimize)
    
    #Create a dictionary named meals, which will contain the referenced variables
    meals = LpVariable.dicts('Meal',[(meal, i) for meal,i in enumerate(meals_dict)], lowBound=0, cat=LpInteger)

    #The objective funtion
    prob += lpSum([meals_dict[meal] for meal in meals_dict])
    
    #Constrains
    prob += lpSum([meals_dict[meal]['calories'] * meals[(i, meal)] for i, meal in enumerate(meals_dict)]) == calories
    prob += lpSum([meals_dict[meal]['protein'] * meals[(i, meal)] for i, meal in enumerate(meals_dict)]) >= protein
    prob += lpSum([meals_dict[meal]['fat'] * meals[(i, meal)] for i, meal in enumerate(meals_dict)]) == fat
    prob += lpSum([meals_dict[meal]['carbs'] * meals[(i, meal)] for i, meal in enumerate(meals_dict)]) == carbs
    
    
    prob.solve()
    
    for i, meal in enumerate(meals_dict):
        if meals[(i, meal)].varValue == 1:
            menu[meal] = meals_dict[meal]
    
    for key, value in menu.items():
        daily_meals_list.append(f"{key} \n Calories: {value['calories']} kcal, Protein: {value['protein']}g, Fat: {value['fat']}g, Carbs: {value['carbs']}g \n")
        daily_calories += value['calories']
        daily_protein += value['protein']
        daily_fat += value['fat']
        daily_carbs += value['carbs']
    

    daily_result_string =  f"Total daily Calories: {daily_calories}, Total daily proteins: {daily_protein}g, Total daily fat: {daily_fat}g, Total daily carbs: {carbs}g \n"
    
    for n in daily_meals_list:
        daily_result_string += f"\n {n}"
    return  daily_result_string


def generate_menus_for_a_few_days(calories, protein, carbs, fat, days):
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
        string: menu
    
    Raises:
        InvalidCaloriesAndMacrosError: If function validate_calories_and_macronutrients not return True
    """
    number_of_meals_at_base = execute_sql("SELECT COUNT(*) FROM recipies")[0][0]
    step = number_of_meals_at_base // days
    range_list = []
    for i in range(days):
        if len(range_list) == 0:
            range_list.append([0, step])
        range_list.append([range_list[-1][1], range_list[-1][1]+step])
    result_string = ""
    for i in range(1, days + 1):
        result_string += f"Day {i} {generate_one_day_menu(calories, protein, carbs, fat, range_list[i-1])}" 
    return result_string

def parse_args():
    """
    Parse command-line arguments for creating a menu.

    Returns:
        Parsed command-line arguments
        
    Raises:
        ArgumentError: if command-line arguments are not provided correctly.
    
    """
    parser = argparse.ArgumentParser(description="Creating a menu")
    parser.add_argument('calories', metavar='calories', type=int, help="Your daily calories requirements")
    parser.add_argument('protein', metavar='protein', type=int, help="Your daily protein requirements")
    parser.add_argument('carbs', metavar='carbs', type=int, help="Your daily carbs requirements")
    parser.add_argument('fat', metavar='fat', type=int, help="Your daily fat requirements")
    parser.add_argument('days', metavar='days', type=int, help="How many days it should be created")
    return parser.parse_args()

def main():
    args = parse_args()
    result = generate_menus_for_a_few_days(args.calories, args.protein, args.carbs, args.fat, args.days)
    print(result)
    
        
        
if __name__ == "__main__":
    main()
    # print(generate_day_menu(3999, 166, 584, 111))
    # print(generate_days_menu(3999, 166, 584, 111, 5))