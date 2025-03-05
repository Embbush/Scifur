from rest_framework import serializers
from .models import Researcher
from django.contrib.auth.models import User  # 👈 Ajout pour gérer les utilisateurs

# 🔹 Serializer pour les chercheurs
class ResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Researcher
        fields = "__all__"  # Convertir tous les champs du modèle en JSON

# 🔹 Serializer pour les utilisateurs
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user  # 👈 Ajout du retour de l'utilisateur créé
