from django.db.models.query_utils import Q
import graphene
from graphene_django import DjangoObjectType
# from graphql import GraphqlException

from .models import Track,Like
from users.schema import UserType


class TrackType(DjangoObjectType):
    class Meta:
        model=Track


class LikeType(DjangoObjectType):
    class Meta:
        model=Like
                
        
class Query(graphene.ObjectType):
    tracks=graphene.List(TrackType,search=graphene.String())
    likes=graphene.List(LikeType)
    
    def resolve_tracks(self,info,search=None):
        if search:
            filter=( Q(title__icontains=search) | Q(description__icontains=search) | Q(url__icontains=search) )
            return Track.objects.filter(filter)
        
        return Track.objects.all()
    
    def resolve_likes(self,info):
        return Like.objects.all()
    
    
class CreateTrack(graphene.Mutation):
    track=graphene.Field(TrackType)
    
    class Arguments:
        title=graphene.String()
        description=graphene.String()
        url=graphene.String()
        
    # def mutate(self,info,**kwargs):
        # kwargs.get('title')
    def mutate(self,info,title,description,url):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("login or die")
            # raise Exception("login or die")
        
        track=Track(title=title,description=description,url=url,posted_by=user)
        track.save()
        return CreateTrack(track=track)
    
  
class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)
    
    class Arguments:
        track_id=graphene.Int(required=True)
        title=graphene.String()
        description=graphene.String()
        url=graphene.String()
    
    def mutate(self,info,track_id,title,url,description):
        user=info.context.user
        track=Track.objects.get(id=track_id)
        
        if track.posted_by != user:            
            raise Exception("not same author that posted ")
            # raise Exception("not same author that posted ")
        
        track.title=title
        track.description=description
        track.save()
        
        return UpdateTrack(track=track)

class DeleteTrack(graphene.Mutation):
    track_id=graphene.Int()
    
    class Arguments:
        track_id=graphene.Int(required=True)
        
    def mutate(self,info,track_id):
        user=info.context.user
        track=Track.objects.get(id=track_id)
        
        if track.posted_by != user:
            raise Exception("not same author that posted ")
            # raise Exception("not same author that posted ")
    
        track.delete()
        return DeleteTrack(track_id=track_id)
    
    
class CreateLike(graphene.Mutation):
    user=graphene.Field(UserType)
    track=graphene.Field(TrackType)
    
    class Arguments:
        track_id=graphene.Int(required=True)
        
    def mutate(self,info,track_id):
        user=info.context.user
            
        if user.is_anonymous:
            raise Exception("login!!!!!!!!!!!!!!!!")
            # raise Exception("LOGIN LOGIN")
            
        track=Track.objects.get(id=track_id)
        if not track:
            raise Exception("that trackid is nowhere")
            # raise Exception("that trackid is nowhere")
            
        Like.objects.create(user=user,track=track)
            
        return CreateLike(user=user,track=track)
    
    
class Mutation(graphene.ObjectType):
    create_track=CreateTrack.Field()
    update_track=UpdateTrack.Field()
    delete_track=DeleteTrack.Field()
    create_like=CreateLike.Field()
     


# {
#   tracks{
#     id
#     title
#     likes{
#       id
#     }
#   }
# }

# {
#   likes{
#     id
#     user{
#       username
#     }
#     track{
#       title
#     }
#   }
# }      
        
#  mutation{
#   createLike(trackId:1){
#     track{
#       id 
#     }
#   }
# }       
        
#  mutation{
#   deleteTrack(trackId:4)
# 	{
#     trackId
# 	}
# }


#  mutation{
#   updateTrack(trackId:4,title:"updated track",description:"dd4",url:"www.xxx.com")
# 	{
#     track{
#     	id
#     	title
#     	description
#   	}
# 	}
# }


#  mutation{
#   createTrack(title:"t4",description:"d4",url:"www.xxx.com")
# 	{
#     track{
#     	id
#     	title
#     	description
#   	}
# 	}
# }

# Authorization
# JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFhYSIsImV4cCI6MTYzNjI4NzE0OSwib3JpZ0lhdCI6MTYzNjI4Njg0OX0.uQ_CvUSZscXgWiyi1OI5mo-wZYWm8rwIww6cTzBwPew