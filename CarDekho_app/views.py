from django.shortcuts import render
from .models import carlist, Showroomlist, Review
from django.http import JsonResponse, HttpResponse
import json
from .api_file.serializers import CarSerializer,ShowroomSerializer, ReviewSerializers
from .api_file.permissions import AdminOrReadOnlyPermission, ReviewUserReadOnlypermission
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser,DjangoModelPermissions
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
# Create your views here.

# def car_list_view(request):
#     cars = carlist.objects.all()
#     data  =  {
#         'cars' : list(cars.values()),
#     }
#     data_json = json.dumps(data)
#     return HttpResponse(data_json, content_type='application/json') 
#     # return JsonResponse(data)

# def car_detail_view(request, pk):
#     car = carlist.objects.get(pk=pk)
#     data = {
#         'name' : car.name,
#         'description' : car.description,
#         'active' : car.active,
#     }
#     return JsonResponse(data)

class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializers
    
    def get_queryset(self): 
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        cars  = carlist.objects.get(pk = pk)
        useredit  = self.request.user
        Review_queryset = Review.objects.filter(car  = cars,apiuser = useredit)
        if Review_queryset.exists():
            raise ValidationError("You have already reviewed this car")
        serializer.save(car=cars,apiuser=useredit)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        



class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(car=pk)









class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
# class ReviewDetail(generics.ListAPIView):
# class ReviewDetail(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    # permission_classes = [AdminOrReadOnlyPermission]
    permission_classes = [ReviewUserReadOnlypermission]
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [DjangoModelPermissions]
  
  
    """review detail view
    list : list all review
    update : update a review
    destroy : delete a review

    Returns:
        _type_: _description_
    """
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializers

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)
    
        
    """review list view
        list : list all review
        
        create : create a review

        Returns:
            Response: json response of review
    """



# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializers    
#     authentication_classes = [SessionAuthentication]
#     permission_classes = [DjangoModelPermissions]
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

    """showroom viewset
    list : list all showroom
    retrieve : get a showroom by id
    create : create a showroom
    update : update a showroom
    destroy : delete a showroom

    Returns:
        _type_: _description_
    """

    
    
class Showroom_Viewset(viewsets.ModelViewSet):
    queryset = Showroomlist.objects.all()
    serializer_class = ShowroomSerializer  


    """read only model viewset for showroom
    list : list all showroom
    retrieve : get a showroom by id

    Returns:
        Response: json response of showroom
    """

# class Showroom_Viewset(viewsets.ReadOnlyModelViewSet):
#     queryset = Showroomlist.objects.all()
#     serializer_class = ShowroomSerializer
    
    
    """
    viewset for showroom
    list : list all showroom
    retrieve : get a showroom by id
    create : create a showroom
    update : update a showroom
    destroy : delete a showroom
    Returns:
        Response: json response of showroom
    """
# class Showroom_Viewset(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Showroomlist.objects.all()
#         serializer = ShowroomSerializer(queryset, many=True,context={'request': request})
#         return Response(serializer.data)
#     def retrieve(self, request, pk=None):
#         queryset = Showroomlist.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = ShowroomSerializer(user,context={'request': request})
#         return Response(serializer.data) 
#     def create(self, request):
#         serializer = ShowroomSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def update(self, request, pk=None):
#         queryset = Showroomlist.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         serializer = ShowroomSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     def destroy(self, request, pk=None):
#         queryset = Showroomlist.objects.all()
#         user = get_object_or_404(queryset, pk=pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
    

    
class Showroom_view(APIView):

    # authentication_classes = [BasicAuthentication]
    #permission_classes = [IsAuthenticated]
    #permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminUser]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        showroom = Showroomlist.objects.all()
        serializer = ShowroomSerializer(showroom, many=True,context = {'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ShowroomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)
        return Response(serializer.errors, status=400)

class Showroom_Details(APIView):
    def get(self, request,pk):
        try:
            showroom = Showroomlist.objects.get(pk=pk)
        except Showroomlist.DoesNotExist:
            return Response({'Error':'showroom not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ShowroomSerializer(showroom)
        return Response(serializer.data)
    def put(self,request,pk):
        try:
            showroom = Showroomlist.objects.get(pk=pk)
        except Showroomlist.DoesNotExist:
            return Response({'Error':'showroom not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = ShowroomSerializer(showroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    def delete(self,request,pk):       
        try:
            showroom = Showroomlist.objects.get(pk=pk)
        except Showroomlist.DoesNotExist:
            return Response({'Error':'showroom not found'},status=status.HTTP_404_NOT_FOUND)
        showroom.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET', 'POST'])
def car_list_view(request):
    if request.method  == 'GET':
          cars = carlist.objects.all()
          serializer = CarSerializer(cars,many=True)
          return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors)

@api_view(['GET','PUT','DELETE'])
def car_detail_view(request, pk):
    if request.method == 'GET':
        try:
          car = carlist.objects.get(pk=pk)
        except:
            return Response({'Error':'car not found'},status=status.HTTP_404_NOT_FOUND)
        serializer = CarSerializer(car)
        return Response(serializer.data)
    if request.method == 'PUT':
        car = carlist.objects.get(pk=pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    if request.method == 'DELETE':
        car = carlist.objects.get(pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)