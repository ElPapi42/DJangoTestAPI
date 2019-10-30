import graphene
from graphene_django.types import DjangoObjectType, ObjectType
from django.contrib.auth.models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User

class Query(ObjectType):
    user = graphene.Field(UserType, id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, **kwargs):
        id = kwargs.get("id")

        if(id != None):
            return User.objects.get(pk=id)

        return None

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

schema = graphene.Schema(query=Query)