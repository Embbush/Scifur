from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from .models import Researcher
from .serializers import ResearcherSerializer, UserSerializer
from django.db.models.functions import Lower
from django.db.models.expressions import Func
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

class Unaccent(Func):
    function = "unaccent"
    template = "%(function)s(%(expressions)s)"

class ResearcherViewSet(viewsets.ModelViewSet):
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["expertise", "institution"]

    def get_queryset(self):
        return Researcher.objects.annotate(
            expertise_lower=Unaccent(Lower("expertise")),
            institution_lower=Unaccent(Lower("institution"))
        )

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Créer un utilisateur et mettre à jour son profil chercheur sans recréer l'objet."""

        # Afficher les données reçues dans la requête
        print("\n📥 Données reçues :", request.data)  # Debug

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            print("\n❌ Erreur de validation :", serializer.errors)  # Debug
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        print(f"\n✅ Utilisateur {user.username} créé avec succès (ID: {user.id})")  # Confirmer la création de l'utilisateur

        researcher_data = request.data.get("researcher", None)
        if researcher_data:
            print("\n🔍 Données pour le chercheur :", researcher_data)  # Afficher les données du chercheur

            # Remove potential user key to avoid conflicts
            researcher_data = {k: v for k, v in researcher_data.items() if k != "user"}

            # Cherche si un chercheur existe pour cet utilisateur ou le crée avec les données fournies
            researcher, created = Researcher.objects.get_or_create(
                user=user, defaults=researcher_data
            )

            # Si le chercheur existe déjà, on le met à jour
            if not created:
                print("\n🔄 Mise à jour du chercheur existant")
                for key, value in researcher_data.items():
                    setattr(researcher, key, value)
                researcher.save()
                print("\n✅ Chercheur mis à jour :", researcher)

            else:
                print("\n✅ Nouveau chercheur créé pour l'utilisateur :", researcher)

        else:
            print("\n⚠️ Aucune donnée 'researcher' reçue.")  # Debug si pas de données de chercheur

        return Response(serializer.data, status=status.HTTP_201_CREATED)
