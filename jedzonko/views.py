from datetime import datetime
import random
from django.shortcuts import render
from django.views import View
from jedzonko.models import *


class IndexView(View):

    def get(self, request):
        # ctx = {"actual_date": datetime.now()}
        lenght = Recipe.objects.all().__len__()
        lenght += 6
        choice = random.randint(6, lenght)
        recipe1 = Recipe.objects.filter(id=choice)
        choice = random.randint(6, lenght)
        recipe2 = Recipe.objects.filter(id=choice)
        choice = random.randint(6, lenght)
        recipe3 = Recipe.objects.filter(id=choice)
        return render(request, "index.html",
                      {"recipe1": recipe1,
                      "recipe2": recipe2,
                      "recipe3": recipe3}
                      )

class Dashboard(View):
    def get(self, request):
        plan_count = Plan.objects.count()
        recipes_count = Recipe.objects.count()
        return render(request, "dashboard.html", {"plan_count": plan_count,
                                                  "recipes_count": recipes_count})

class RecipeView(View):
    def get(self, request):
        return render(request, "app-recipes.html")

class RecipeAdd(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        ingredients = request.POST.get("ingredients")
        preparation_time = request.POST.get("preparation_time")
        if name and description and ingredients and preparation_time:
            Recipe.objects.create(name=name,
                                  description=description,
                                  preparation_time=preparation_time,
                                  ingredients=ingredients,
                                  created=datetime.datetime.utcnow(),
                                  updated=datetime.datetime.utcnow())
        return render(request, "app-add-recipe.html")