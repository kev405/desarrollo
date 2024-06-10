from ..models import CustomWorkManagement
from ..serializers import CustomWorkManagementSerializer
from rest_framework import generics

#instacias nuevas funciones

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from ..models import CustomWorkManagement, CustomJobManagement
from ..serializers import CustomJobManagementSerializer


#Nuevas funciones


# Nueva función para obtener todas las tareas de una obra

#Obetener todas las tareas de una obra
@api_view(['GET'])
def tasks_by_work_management(request, obra_id):
    try:
        tareas = CustomJobManagement.objects.filter(obra_id=obra_id)
        serializer = CustomJobManagementSerializer(tareas, many=True)
        return Response(serializer.data)
    except CustomWorkManagement.DoesNotExist:
        return JsonResponse({'error': 'La obra no existe.'}, status=404)
    except CustomJobManagement.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron tareas para la obra especificada.'}, status=404)

#obetener tareas aceptadas 

@api_view(['GET'])
def accepted_tasks_by_work_management(request, obra_id):
    try:
        tareas = CustomJobManagement.objects.filter(obra_id=obra_id, estado='aceptada')
        serializer = CustomJobManagementSerializer(tareas, many=True)
        return Response(serializer.data)
    except CustomWorkManagement.DoesNotExist:
        return JsonResponse({'error': 'La obra no existe.'}, status=404)
    except CustomJobManagement.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron tareas aceptadas para la obra especificada.'}, status=404)
    

# Obtener porcentaje de tareas aceptadas
@api_view(['GET'])
def percentage_accepted_tasks_by_work_management(request, obra_id):
    try:
        total_tareas = CustomJobManagement.objects.filter(obra_id=obra_id).count()
        tareas_aceptadas = CustomJobManagement.objects.filter(obra_id=obra_id, estado='aceptada').count()
        
        if total_tareas == 0:
            return JsonResponse({'error': 'No se encontraron tareas para la obra especificada.'}, status=404)

        porcentaje_aceptadas = (tareas_aceptadas / total_tareas) * 100
        return JsonResponse({'porcentaje_aceptadas': porcentaje_aceptadas})
    except CustomWorkManagement.DoesNotExist:
        return JsonResponse({'error': 'La obra no existe.'}, status=404)
    except CustomJobManagement.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron tareas para la obra especificada.'}, status=404)

# Clases genéricas
class WorkManagementList(generics.ListCreateAPIView):
    queryset = CustomWorkManagement.objects.all()
    serializer_class = CustomWorkManagementSerializer

class WorkManagementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomWorkManagement.objects.all()
    serializer_class = CustomWorkManagementSerializer
