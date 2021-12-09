import graphene
import tracks.schema
import users.schema
import graphql_jwt #https://github.com/flavors/django-graphql-jwt

 
class Query(users.schema.Query,   tracks.schema.Query,   graphene.ObjectType):
    pass


class Mutation(users.schema.Mutation,tracks.schema.Mutation,
               graphene.ObjectType
               ):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()

schema=graphene.Schema(query=Query,mutation=Mutation)
    

# mutation{
#   createTrack(title:"t3",description:"d3",url:"www.xxx.com")
# 	{
#     track{
#     	id
#     	title
#     	description
#   	}
# 	}
# }