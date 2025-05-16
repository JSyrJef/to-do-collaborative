from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.shortcuts import get_object_or_404 
from .models import Task
from .serializers import TaskSerializer, UserSerializer

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
        
        username = request.data.get('username', None)
        if not username:
            return Response({"detail": "Se requiere nombre de usuario"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username=username)
            task.collaborators.add(user)
            return Response({"detail": f"Usuario {username} añadido como colaborador"})
        except User.DoesNotExist:
            return Response({"detail": "Usuario no encontrado"}, 
                            status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def remove_collaborator(self, request, pk=None):
        task = self.get_object()
        
        # Solo el propietario puede eliminar colaboradores
        if task.user != request.user:
            return Response({"detail": "Solo el propietario puede eliminar colaboradores"}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        username = request.data.get('username', None)
        if not username:
            return Response({"detail": "Se requiere nombre de usuario"}, 
                            status=status.HTTP_400_BAD_REQUEST)
        
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