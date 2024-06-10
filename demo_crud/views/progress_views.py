from ..models import CustomProgressManagement
from ..serializers import CustomProgressManagementSerializer
from rest_framework import generics

# Clases genéricas
class ProgressManagementList(generics.ListCreateAPIView):
    queryset = CustomProgressManagement.objects.all()
    serializer_class = CustomProgressManagementSerializer

class ProgressManagementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomProgressManagement.objects.all()
    serializer_class = CustomProgressManagementSerializer
