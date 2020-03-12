from datetime import datetime
import random
from django.shortcuts import render, render_to_response, redirect, reverse
from django.core.paginator import Paginator

from django.db.models import F
from django.shortcuts import render
from django.views import View
from jedzonko.models import *
from django.contrib import messages
from django.http import Http404


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
        # Making slug object
        page = Page.objects.filter(slug="contact")
        about = Page.objects.filter(slug="about")
        return render(request, "index.html", {
            "recipe1": recipe1,
            "recipe2": recipe2,
            "recipe3": recipe3,
            "newest_plan": newest_plan,
            "plan_days": plan_days,
            "page": page,
            "about": about
        })


class Dashboard(View):
    def get(self, request):
        plan_count = Plan.objects.count()
        recipes_count = Recipe.objects.count()
        plan = Plan.objects.last()
        day_name = DayName.objects.count()
        rp_dict = {}
        for day in range(1, day_name + 1):
            qs = plan.recipeplan_set.filter(day_name_id=day)
            if qs.count() != 0:
                rp_dict[plan.recipeplan_set.filter(day_name=day)[0].day_name.name] = qs[::-1]
        return render(request, "dashboard.html", {"plan_count": plan_count,
                                                  "recipes_count": recipes_count,
                                                  "plan": plan,
                                                  "rp_dict": rp_dict})


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

    def post(self, request, id):
        recipe_id = request.POST.get("recipe_id")
        like = request.POST.get("like")
        if like == "like":
            recipe = Recipe.objects.get(id=recipe_id)
            recipe.votes += 1
            recipe.save()
            return redirect(f'/recipe/{recipe_id}')
        else:
            recipe = Recipe.objects.get(id=recipe_id)
            recipe.votes -= 1
            recipe.save()
            return redirect(f'/recipe/{recipe_id}')


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
        recipes = Recipe.objects.all()
        plans = Plan.objects.all()
        days = DayName.objects.all()
        return render(request, "app-schedules-meal-recipe.html",
                      {"recipes": recipes,
                       "plans": plans,
                       "days": days})

    def post(self, request):
        plan = Plan.objects.get(name=request.POST.get('plan'))
        meal_name = request.POST.get('meal_name')
        order = request.POST.get('order')
        day_name = DayName.objects.get(name=request.POST.get('day_name'))
        recipe = Recipe.objects.get(name=request.POST.get('recipe'))
        if plan and meal_name and order and day_name and recipe:
            recipe_plan = RecipePlan.objects.create(
                meal_name=meal_name,
                recipe=recipe,
                plan=plan,
                order=order,
                day_name=day_name
            )
            message = messages.info(request, "Pomyślnie dodano przepis")
            return redirect("/plan/add-recipe/", {"message": message})
        else:
            message = messages.info(request, "Nie podano wszystkich danych")
            return redirect("/plan/add-recipe/", {"message": message})


class PlanAdd(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        created = datetime.datetime.now()
        if name and description and created:
            new_plan = Plan.objects.create(name=name,
                                           description=description,
                                           created=created)
            return redirect(f'/plan/{new_plan.id}')
        else:
            error_message = messages.info(request, "Nie podano wszystkich danych")
            return redirect("/plan/add/", {"error_message": error_message})


class PLanDetails(View):
    def get(self, request, id):
        plan = Plan.objects.get(pk=id)
        day_name = DayName.objects.count()
        # Adding query_set to dictionary, key is day_name
        mn_dict = {}
        for day in range(1, day_name + 1):
            qs = plan.recipeplan_set.filter(day_name=day)
            if qs.count() != 0:
                mn_dict[plan.recipeplan_set.filter(day_name=day)[0].day_name.name] = qs[::-1]
        return render(request, "app-details-schedules.html",
                      {"plan": plan,
                       "mn_dict": mn_dict})


class ContactSlug(View):
    def get(self, request):
        page = Page.objects.all()
        contact_slug = page.filter(slug="contact")[0]
        return render(request, "contact_slug.html", {"contact_slug": contact_slug})


class AboutSlug(View):
    def get(self, request):
        page = Page.objects.all()
        about_slug = page.filter(slug="about")[0]
        return render(request, "about_slug.html", {"about_slug": about_slug})


class ModifyRecipe(View):

    def get(self, request, id):
        recipe = Recipe.objects.filter(id=id)
        return render(request, 'app-edit-recipe.html', {"recipe": recipe})

    def post(self, request, id):
        recipe_name = request.POST.get('recipe_name')
        recipe_description = request.POST.get('recipe_description')
        recipe_preparation_time = request.POST.get('recipe_preparation_time')
        recipe_ingredients = request.POST.get('recipe_ingredients')
        if recipe_name and recipe_description and recipe_ingredients and recipe_preparation_time:
            new_recipe = Recipe.objects.create(name=recipe_name,
                                               description=recipe_description,
                                               preparation_time=recipe_preparation_time,
                                               ingredients=recipe_ingredients,
                                               created=datetime.datetime.now(),
                                               updated=datetime.datetime.now()
                                               )

            return redirect('/recipe/list/')
        else:
            message = messages.info(request, "Nie podano wszystkich danych")
            return redirect(f"/recipe/modify/{id}", {"message": message})
