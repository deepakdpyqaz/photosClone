from django.shortcuts import render
from .models import Picture
from .serializers import PictureSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def getall(request):
    pictures = Picture.objects.filter(user=request.user).all()
    picture_serializer = PictureSerializer(pictures,many=True)
    return Response(picture_serializer.data,status=200)

@api_view(["POST"])
@permission_classes((IsAuthenticated,))
def upload(request):
    try:
        picture_file = request.FILES['picture']
        picture = Picture(user=request.user,picture=picture_file)
        picture.save()
        return Response({"status":"success"},status=201)
    except Exception as e:
        return Response({"status":"fail","message":str(e)},status=500)


@api_view(["DELETE"])
def delete(request,id):
    try:
        picture = Picture.objects.filter(id=id).first()
        if not picture:
            return Response({"status":"fail","message":"picture not found"},status=400)
        picture.delete()
        return Response({"status":"success"},status=200)
    except Exception as e:
        return Response({"status":"fail","message":str(e)},status=500)