from django.contrib import admin
from django.urls import path

from jedzonko.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('recipe/list/', RecipeView.as_view()),
    path('main/', Dashboard.as_view()),
    path('recipe/add/', RecipeAdd.as_view()),
    path('plan/list/', PlansList.as_view()),
    path('plan/add-recipe/', PlanAddRecipe.as_view()),
    path('plan/add/', PlanAdd.as_view()),
    path('recipe/<int:id>/', RecipeDetails.as_view()),
    path('plan/<int:id>/', PlanDetails.as_view())
]

