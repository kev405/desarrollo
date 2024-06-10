#general
from django.http import JsonResponse
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser
from rest_framework import status
from ..models import CustomUser
from ..serializers import CustomUserSerializer
#genericas
from rest_framework import generics
#login librerias para el login
from rest_framework.response import Response
# from django.contrib.auth.hashers import check_password
# from django.contrib.auth import authenticate, login
# from rest_framework.authtoken.models import Token

# @api_view(['GET'])

# def user_get_peon(request):
#     if request.method == 'GET':
#         users = CustomUser.role("peon")
#         serializer = CustomUserSerializer(users, many=True)
#         return JsonResponse(serializer.data, safe=False)

# @api_view(['POST'])
# def user_create(request):
#     if request.method == 'POST':
#         serializer = CustomUserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['DELETE'])
# def user_delete(request, pk):
#     try:
#         user = CustomUser.objects.get(pk=pk)
#     except CustomUser.DoesNotExist:
#         return JsonResponse({'error': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'DELETE':
#         user.delete()
#         return JsonResponse({'message': 'El usuario fue eliminado satisfactoriamente.'}, status=status.HTTP_204_NO_CONTENT)
    

# @api_view(['PUT'])
# def user_update(request, pk):
#     try:
#         user = CustomUser.objects.get
#     except CustomUser.DoesNotExist:
#         return JsonResponse({'error': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PUT':
#         serializer = CustomUserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# def user_login(request):
#     if request.method == 'POST':
#         email = request.data.get('email')
#         password = request.data.get('password')
#         print(email)
#         print(password)
        
#         user = authenticate(email=email, password=password)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             serializer = CustomUserSerializer(user)
#             return Response({'token': token.key, 'user': serializer.data})
#         else:
#             return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)



#Obtener gerentes
@api_view(['GET'])
def user_get_gerente(request):
    try:
        gerentes = CustomUser.objects.filter(role='gerente')
        serializer = CustomUserSerializer(gerentes, many=True)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron usuarios con el rol de "gerente".'}, status=status.HTTP_404_NOT_FOUND)


#Obtener ayudantes_alabañil
@api_view(['GET'])
def user_get_ayudantes(request):
    try:
        gerentes = CustomUser.objects.filter(role='ayudante_albanil')
        serializer = CustomUserSerializer(gerentes, many=True)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron usuarios con el rol de "gerente".'}, status=status.HTTP_404_NOT_FOUND)

#Obtener director_obra 
@api_view(['GET'])
def user_get_directores(request):
    try:
        gerentes = CustomUser.objects.filter(role='director_obra')
        serializer = CustomUserSerializer(gerentes, many=True)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron usuarios con el rol de "gerente".'}, status=status.HTTP_404_NOT_FOUND)

#Obtener capataz
@api_view(['GET'])
def user_get_capataces(request):
    try:
        gerentes = CustomUser.objects.filter(role='capataz_obra')
        serializer = CustomUserSerializer(gerentes, many=True)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron usuarios con el rol de "gerente".'}, status=status.HTTP_404_NOT_FOUND)

#Obtener peones
@api_view(['GET'])
def user_get_peones(request):
    try:
        gerentes = CustomUser.objects.filter(role='peon')
        serializer = CustomUserSerializer(gerentes, many=True)
        return Response(serializer.data)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'No se encontraron usuarios con el rol de "gerente".'}, status=status.HTTP_404_NOT_FOUND)
    
#Pone un estado de "No activo al usuario en lugar de eliminarlo"
@api_view(['PUT'])
def user_deactivate(request, pk):
    try:
        user = CustomUser.objects.get(pk=pk)  # Se corrige la línea para obtener el usuario por su clave primaria (pk)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'El usuario no existe.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        user.is_active = False  # Se desactiva el usuario
        user.save()  # Se guardan los cambios en la base de datos

        serializer = CustomUserSerializer(user)  # Se serializa el usuario actualizado
        return JsonResponse(serializer.data)

@api_view(['POST'])
@parser_classes([JSONParser])
def user_login(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.get(email=email, password=password)
  
        if user is not None:
            return Response({
                'user': {
                    'email': user.email,
                    'name': user.name,
                    'phone': user.phone,
                    'role': user.role,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff
                },
                'success': True,
            })
        else:
            return Response({
                'success': False,
            })

#Clases genericas 
class UserList(generics.ListCreateAPIView): 
    queryset = CustomUser.objects.all() 
    serializer_class = CustomUserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView): 
    queryset = CustomUser.objects.all() 
    serializer_class = CustomUserSerializer
