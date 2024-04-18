from .models import Tikit
from rest_framework import serializers



class TikitSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Tikit
        fields = ('__all__')

    def validate(self, attrs):
        attrs['user'] = self.context.get('request').user
        return attrs
