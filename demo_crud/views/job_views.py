from ..models import CustomJobManagement
from ..serializers import CustomJobManagementSerializer
from rest_framework import generics
from rest_framework.decorators import api_view
from django.http import JsonResponse

#Retorna tareas asignadas a una obra especifica
@api_view(['GET'])
def tasks_by_work_management(request, obra_id):
    try:
        tareas = CustomJobManagement.objects.filter(obra_id=obra_id)
        serializer = CustomJobManagementSerializer(tareas, many=True)
        return JsonResponse(serializer.data, safe=False)
    except CustomJobManagement.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron tareas para la obra especificada.'}, status=404)
    
# Clases genéricas
class JobManagementList(generics.ListCreateAPIView):
    queryset = CustomJobManagement.objects.all()
    serializer_class = CustomJobManagementSerializer

class JobManagementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomJobManagement.objects.all()
    serializer_class = CustomJobManagementSerializer
