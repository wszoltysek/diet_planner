from datetime import datetime
import random
from django.shortcuts import render, render_to_response, redirect
from django.core.paginator import Paginator

from django.db.models import F
from django.shortcuts import render
from django.views import View
from jedzonko.models import *
from django.contrib import messages


class IndexView(View):

    def get(self, request):
        recipes = Recipe.objects.all()
        list_recipes = list(recipes)
        random.shuffle(list_recipes)
        recipe1 = Recipe.objects.filter(id=list_recipes[0].id)
        recipe2 = Recipe.objects.filter(id=list_recipes[1].id)
        recipe3 = Recipe.objects.filter(id=list_recipes[2].id)

        plans = Plan.objects.all().order_by("-created")
        newest_plan = plans.first()
        plan_days = RecipePlan.objects.filter(plan_id=newest_plan.id).order_by("order")

        return render(request, "index.html", {
            "recipe1": recipe1,
            "recipe2": recipe2,
            "recipe3": recipe3,
            "newest_plan": newest_plan,
            "plan_days": plan_days
        })


class Dashboard(View):
    def get(self, request):
        plan_count = Plan.objects.count()
        recipes_count = Recipe.objects.count()
        return render(request, "dashboard.html", {"plan_count": plan_count,
                                                  "recipes_count": recipes_count})


class RecipeView(View):
    def get(self, request):
        recipes_list = Recipe.objects.all().order_by(F("votes").desc(), F("created").desc())
        paginator = Paginator(recipes_list, 25)
        page = request.GET.get('page')
        recipes = paginator.get_page(page)
        ctx = {"recipes": recipes}
        return render(request, "app-recipes.html", ctx)

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
        else:
            error_message = messages.info(request, "Nie podano wszystkich danych")
            return redirect("/recipe/add/", {"error_message": error_message})

class RecipeDetails(View):
    def get(self, request, id):
        recipe = Recipe.objects.get(pk=id)
        return render(request, "app-recipe-details.html", {"recipe": recipe})


# ZADANIE 5.2:
class PlansList(View):
    def get(self, request):
        plan_list = Plan.objects.all().order_by("name")
        paginator = Paginator(plan_list, 25)
        page = request.GET.get('page')
        plans = paginator.get_page(page)
        ctx = {"plans": plans}
        return render(request, "app-schedules.html", ctx)

class PlanAddRecipe(View):
    def get(self, request):
        return render(request, "empty_page.html")


class PlanAdd(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        created = datetime.datetime.now()
        if name and description and created:
            Plan.objects.create(name=name,
                                description=description,
                                created=created)
        return render(request, "app-add-schedules.html")
