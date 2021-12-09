from django.contrib.auth import get_user_model


import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model=get_user_model()

class Query(graphene.ObjectType):
    user=graphene.Field(UserType,id=graphene.Int(required=True))
    me=graphene.Field(UserType)    
    
    def resolve_user(self,info,id):
        return get_user_model().objects.get(id=id)
    
    def resolve_me(self,info):
        user=info.context.user
        if user.is_anonymous:
            raise Exception ("not logged in")
        return user
    
        
class CreateUser(graphene.Mutation):
    user=graphene.Field(UserType)
    
    class Arguments:
        username=graphene.String(required=True)
        password=graphene.String(required=True)
        email=graphene.String(required=True)
        
    def mutate(self,info,username,password,email):
        user=get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)
        
class Mutation(graphene.ObjectType):
    create_user=CreateUser.Field()
    
# mutation($username:String!,$email:String!,$password:String!)
# {  
# 	createUser(username:$username, email:$email,password:$password)
# 	{
#       user{
#       username
#       email		
#     }
# 	}
# }

# {
#   "username":"hhh",
#   "password":"hhh",
#   "email":"x@x.com"
  
# }
    
    
# Authorization
# JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFhYSIsImV4cCI6MTYzNjI4NzE0OSwib3JpZ0lhdCI6MTYzNjI4Njg0OX0.uQ_CvUSZscXgWiyi1OI5mo-wZYWm8rwIww6cTzBwPew    
    
# mutation{
#   tokenAuth(username:"aaa",password:"aaa"){
#     token
#   }
# }

# {
#   me{
#     id
#   }
# }

# {
#   user(id:2){
#     id
#     username
#     password
#   }
# }

        
        
# mutation{
#   createUser(username:"aab",password:"aaa",email:"x1@x.com")
# 	{
#     user{
#     	id
#     	username
#     	password
#       email
#   	}
# 	}
# }
