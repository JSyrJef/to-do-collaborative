from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.shortcuts import get_object_or_404 
from .models import Task
from .serializers import TaskSerializer, UserSerializer, CollaboratorSerializer

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsOwnerOrCollaborator(permissions.BasePermission):
    """
    Permite acceso al propietario o a colaboradores
    """
    def has_object_permission(self, request, view, obj):
        # Verificar si el usuario es propietario
        if obj.user == request.user:
            return True
        
        # Verificar si el usuario es colaborador (solo lectura para métodos seguros)
        if request.method in permissions.SAFE_METHODS and request.user in obj.collaborators.all():
            return True
        
        return False

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCollaborator]
    
    def get_queryset(self):
        user = self.request.user
        # Obtener tareas propias o en las que es colaborador
        own_tasks = Task.objects.filter(user=user)
        collaborative_tasks = Task.objects.filter(collaborators=user)
        queryset = own_tasks.union(collaborative_tasks)
        
        # Filtrar por estado si se proporciona
        status_param = self.request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def add_collaborator(self, request, pk=None):
        task = self.get_object()
        
        # Solo el propietario puede añadir colaboradores
        if task.user != request.user:
            return Response({"detail": "Solo el propietario puede añadir colaboradores"}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = CollaboratorSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                # No añadir al propietario como colaborador
                if user == request.user:
                    return Response({"detail": "No puedes añadirte a ti mismo como colaborador"}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                # No añadir colaboradores duplicados
                if user in task.collaborators.all():
                    return Response({"detail": "El usuario ya es colaborador"}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                    
                task.collaborators.add(user)
                return Response({"detail": f"Usuario {username} añadido como colaborador"})
            except User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado"}, 
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], serializer_class=CollaboratorSerializer)
    def remove_collaborator(self, request, pk=None):
        task = self.get_object()
        
        # Solo el propietario puede eliminar colaboradores
        if task.user != request.user:
            return Response({"detail": "Solo el propietario puede eliminar colaboradores"}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = CollaboratorSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                user = User.objects.get(username=username)
                if user in task.collaborators.all():
                    task.collaborators.remove(user)
                    return Response({"detail": f"Usuario {username} eliminado como colaborador"})
                else:
                    return Response({"detail": "El usuario no es colaborador de esta tarea"}, 
                                    status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado"}, 
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)