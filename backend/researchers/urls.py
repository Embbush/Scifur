from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResearcherViewSet, UserViewSet

# Créer un routeur pour générer automatiquement les URLs de l’API
router = DefaultRouter()
router.register(r"researchers", ResearcherViewSet, basename="researcher")
router.register(r"users", UserViewSet)  # 👈 Ajout de la route pour les utilisateurs


urlpatterns = [
    path("", include(router.urls)),  # Inclure les routes API générées
]
