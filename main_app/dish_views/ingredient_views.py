from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import Http404
from main_app.forms import IngredientForm
from main_app.models import *
import json


def ingredient(request):
    ingredients = Ingredient.objects.all()
    return render(request, "food/ingredients.html", {"list_items": ingredients})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_ingredient(request):
    if request.method == 'GET':
        form = IngredientForm()
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            d = Ingredient(name=form.cleaned_data["name"], price=form.cleaned_data["price"])
            d.save()
        return redirect('/ingredient')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def add_ingredient_to_default(request):
    if request.method == 'GET':
        form = IngredientForm()
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            d = Ingredient(name=form.cleaned_data["name"], price=form.cleaned_data["price"])
            d.save()
            file_name = "default_db.json"
            with open(file_name, 'r', encoding='utf-8') as file:
                db = json.load(file)
                ingredients_data = db['ingredients']
                ingredients_data.append({"name": form.cleaned_data["name"],
                                         "price": int(form.cleaned_data["price"])})
            with open(file_name, 'w', encoding='utf-8') as file:
                json.dump(db, file)
        return redirect('/ingredient')


def ingredient_id(request, ing_id):
    ing = Ingredient.objects.filter(id=ing_id)
    if not ing:
        raise Http404
    return render(request, "food/ingredient_id_get.html", {"item": ing.get(id=ing_id)})


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def ingredient_id_delete(request, ing_id):
    ing = Ingredient.objects.filter(id=ing_id)
    if not ing:
        raise Http404
    ing.delete()
    return redirect('/ingredient')


@user_passes_test(lambda u: u.is_superuser, login_url='/accounts/superuser_required')
def ingredient_id_update(request, ing_id):
    if request.method == 'GET':
        ing = Ingredient.objects.filter(id=ing_id)
        if not ing:
            raise Http404
        item = ing.get(id=ing_id)
        data = {'name': item.name,
                'price': item.price}
        form = IngredientForm(data)
        args = {"form": form}
        return render(request, "food/new_ingredient_form.html", args)
    elif request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ing = Ingredient.objects.filter(id=ing_id)
            if ing:
                ing.update(name=form.cleaned_data["name"])
                ing.update(price=form.cleaned_data["price"])
                # this probably makes 3 changes to the db
            else:
                d = Ingredient(name=form.cleaned_data["name"], price=form.cleaned_data["price"])
                d.save()

        return redirect('/ingredient')