from rest_framework import serializers
from ..models import carlist,Showroomlist, Review



# def alphanumberic(value):
#     if not str(value).isalnum():
#         raise serializers.ValidationError("Only aplhanumeric characters are allowed")

class ReviewSerializers(serializers.ModelSerializer):
    apiuser  = serializers.StringRelatedField(read_only = True)
    class Meta:
        model = Review
        exclude = ('car',) # exclude specific field
        # fields = '__all__' # all fields
        # fields = ['id', 'rating', 'comments', 'car'] # specific fields
        # exclude = ['car'] # exclude specific field
        # read_only_fields = ['car'] # make field read only
        # extra_kwargs = {'car': {'read_only': True}} # make field read only
        # extra_kwargs = {'car': {'required': False}} # make field optional


class CarSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField() # custom field
    reviews = ReviewSerializers(many=True, read_only=True) # nested serializer
    # id = serializers.IntegerField(read_only=True)
    # name = serializers.CharField()
    # description = serializers.CharField()
    # active = serializers.BooleanField(read_only=True)
    # chassisnumber = serializers.CharField(validators=[alphanumberic])
    # price = serializers.DecimalField(max_digits=9, decimal_places=2)

    # def create(self, validated_data):
    #     return carlist.objects.create(**validated_data)
    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get('name', instance.name)
    #     instance.description = validated_data.get('description', instance.description)
    #     instance.active = validated_data.get('active', instance.active)
    #     instance.chassisnumber = validated_data.get('chassisnumber', instance.chassisnumber)
    #     instance.price = validated_data.get('price', instance.price)
    #     instance.save()
    #     return instance
    class Meta:
        model = carlist
      #  fields = ['id', 'name', 'description', 'active', 'chassisnumber', 'price']
        #  fields = ['name']
        fields = '__all__' # all fields
       
    def get_discounted_price(self, object): # custom field
        if object.price is None:
          return None  # or some default value, like 0.0
        discountedprice   = object.price - 5000
        
        return discountedprice

    def validate_price(self, value): # field level validation
        if value <= 20000.00:
            raise serializers.ValidationError("Price must be greater than 20000.00")
        return value
    
    def validate(self, data): # object level validation
        if data['name'] == data['description']:
            raise serializers.ValidationError("Name and description should not be same")
        return data
    
class ShowroomSerializer(serializers.ModelSerializer):
    # cars = CarSerializer(many=True, read_only=True) # nested serializer
    # cars = serializers.StringRelatedField(many=True) # nested serializer
    # cars = serializers.PrimaryKeyRelatedField(many=True, read_only = True) # nested serializer
    cars  = serializers.HyperlinkedRelatedField(many=True, view_name='car_detail', read_only=True) # nested serializer
    class Meta:
        model = Showroomlist
        fields = '__all__' # all fields
        # fields = ['name'] # specific fields
        # exclude = ['location'] # exclude specific field
        # read_only_fields = ['location'] # make field read only
        # extra_kwargs = {'location': {'read_only': True}} # make field read only
        # extra_kwargs = {'location': {'required': False}} # make field optional

