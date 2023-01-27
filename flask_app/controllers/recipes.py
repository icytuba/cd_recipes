from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import recipe
from flask import flash

@app.route('/recipes')
def show_all_recipes():
    if session['user_id']:
        return render_template('all_recipes.html', all_recipes = recipe.Recipe.get_all_recipes_with_creator())
    else:
        return redirect('/')

@app.route('/recipes/new')
def create_recipe():
    if session['user_id']:
        return render_template('create_recipe.html')
    else:
        return redirect('/')

@app.route('/process/recipe', methods=['POST'])
def process_recipe():
    print(request.form.get('under_30'))
    if not recipe.Recipe.validate_recipe(request.form):
        session['name'] = request.form['name']
        session['description'] = request.form['description']
        session['instructions'] = request.form['instructions']
        session['date_cooked'] = request.form['date_cooked']
        return redirect('/recipes/new')
    data={
        'user_id': session['user_id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'under_30': request.form['under_30'],
    }
    recipe.Recipe.create_recipe(data)
    session['name'] = ""
    session['description'] = ""
    session['instructions'] = ""
    session['date_cooked'] = ""
    return redirect('/recipes')

@app.route('/recipes/show_one/<int:recipe_id>')
def show_one_recipe(recipe_id):
    data={'id': recipe_id}
    return render_template('show_one_recipe.html', recipe = recipe.Recipe.get_one_recipe_with_creator(data))

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    data={'id': recipe_id}
    return render_template('edit_recipe.html', recipe = recipe.Recipe.get_one_recipe_with_creator(data))

@app.route('/process/edit/<int:recipe_id>', methods=['POST'])
def process_edit(recipe_id):
    if not recipe.Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{recipe_id}')
    data={
        'id': recipe_id,
        'name': request.form['name'],
        'description': request.form['description'],
        'instructions': request.form['instructions'],
        'date_cooked': request.form['date_cooked'],
        'under_30': request.form['under_30'],
    }
    recipe.Recipe.edit_recipe(data)
    return redirect('/recipes')


@app.route('/recipes/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    data={
        'id': recipe_id
    }
    recipe.Recipe.delete_recipe(data)
    return redirect('/recipes')
