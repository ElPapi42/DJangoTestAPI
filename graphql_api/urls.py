from django.urls import path
from graphene_django.views import GraphQLView

urlpatterns = [
    path(
        route='graphql/', 
        view=GraphQLView.as_view(graphiql=True)
    ),
]