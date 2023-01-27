from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Recipe:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.instructions = db_data['instructions']
        self.date_cooked = db_data['date_cooked']
        self.under_30 = db_data['under_30']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.creator = None
    
    @staticmethod
    def validate_recipe(recipe):
        is_valid=True
        if len(recipe['name'])<3:
            flash("Name must be longer than 2 characters", "recipe")
            is_valid=False
        if len(recipe['description'])<3:
            flash("Description must be longer than 2 characters", "recipe")
            is_valid=False
        if len(recipe['instructions'])<3:
            flash("Instructions must be longer than 2 characters", "recipe")
            is_valid=False
        if not recipe['date_cooked']:
            flash("Date is required", "recipe")
            is_valid=False
        if not recipe.get('under_30'):
            flash("Does your recipe take less than 30 minutes?", "recipe")
            is_valid=False
        return is_valid
    
    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (user_id, name, description, instructions, date_cooked, under_30)\
            VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(date_cooked)s, %(under_30)s);"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def get_all_recipes_with_creator(cls):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id ORDER BY recipes.created_at DESC;"
        results = connectToMySQL('recipes_schema').query_db(query)
        all_recipes = []
        for row in results:
            one_recipe = cls(row)
            creator_info ={
                'id': row['user_id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            creator = user.User(creator_info)
            one_recipe.creator = creator
            all_recipes.append(one_recipe)
        return all_recipes

    @classmethod
    def get_one_recipe_with_creator(cls, data):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        result = connectToMySQL('recipes_schema').query_db(query, data)
        one_recipe=cls(result[0])
        creator_info ={
            'id': result[0]['user_id'],
            'first_name': result[0]['first_name'],
            'last_name': result[0]['last_name'],
            'email': result[0]['email'],
            'password': result[0]['password'],
            'created_at': result[0]['users.created_at'],
            'updated_at': result[0]['users.updated_at']
        }
        creator = user.User(creator_info)
        one_recipe.creator = creator
        return one_recipe

    @classmethod
    def edit_recipe(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description= %(description)s, instructions= %(instructions)s, \
            date_cooked= %(date_cooked)s, under_30= %(under_30)s WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes_schema').query_db(query, data)