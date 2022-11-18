from rest_framework.serializers import Serializer, ModelSerializer
from sample.models import Sample


class SampleSerializer(ModelSerializer):
    class Meta:
        model = Sample
        fields = ['name', 'sample_txt', 'sample_id']
