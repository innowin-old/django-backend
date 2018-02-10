from rest_framework.serializers import ModelSerializer

from .models import Form, Group, Element, FormGroup, FormGroupElement, Data


# Create Serializers Here
class FormSerializer(ModelSerializer):
    class Meta:
        model = Form
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ElementSerializer(ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'


class FormGroupSerializer(ModelSerializer):
    class Meta:
        model = FormGroup
        fields = '__all__'


class FormGroupElementSerializer(ModelSerializer):
    class Meta:
        model = FormGroupElement
        fields = '__all__'


class DataSerializer(ModelSerializer):
    class Meta:
        model = Data
        fields = '__all__'
