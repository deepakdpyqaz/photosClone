from django.urls import path
from .import views

urlpatterns=[
    path("",views.getall,name="picture_getall"),
    path("upload",views.upload,name="picture_upload"),
    path("<int:id>",views.delete,name="picture_delete")
]