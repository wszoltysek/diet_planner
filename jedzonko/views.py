from datetime import datetime

from django.shortcuts import render
from django.views import View
from jedzonko.models import *


class IndexView(View):

    def get(self, request):
        ctx = {"actual_date": datetime.now()}
        return render(request, "index.html", ctx)

class Dashboard(View):
    def get(self, request):
        plan_count = Plan.objects.count("id")
        return render(request, "dashboard.html", {"plan_count": plan_count})

class RecipeView(View):
    def get(self, request):
        return render(request, "app-recipes.html")