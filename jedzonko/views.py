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
        return render(request, "dashboard.html")

class RecipeView(View):
    def get(self, request):
        return render(request, "app-recipes.html")