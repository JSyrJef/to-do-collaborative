from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, UserSerializer, CollaboratorSerializer

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsOwnerOrCollaborator(permissions.BasePermission):
    """
    Permite acceso al propietario o a colaboradores
    """
    def has_object_permission(self, request, view, obj):
        # Verificar si el usuario es propietario
        if obj.owner == request.user:
            return True
        
        # Los colaboradores pueden ver y actualizar pero no eliminar
        if request.user in obj.collaborators.all():
            if request.method in ['DELETE']:
                return False
            return True
        
        return False

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrCollaborator]

    def get_queryset(self):
        owner = self.request.user
        # Obtener tareas propias o en las que es colaborador
        own_tasks = Task.objects.filter(owner=owner)
        collaborative_tasks = Task.objects.filter(collaborators=owner)
        # Usar distinct() para evitar duplicados
        return (own_tasks | collaborative_tasks).distinct()
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    # Filtrar por estado
    def list(self, request):
        queryset = self.get_queryset()
        status_param = request.query_params.get('status', None)
        if status_param:
            queryset = queryset.filter(status=status_param)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_collaborator(self, request, pk=None):
        task = self.get_object()
        
        # Solo el propietario puede añadir colaboradores
        if task.owner != request.user:
            return Response({"detail": "Solo el propietario puede añadir colaboradores"}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = CollaboratorSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            try:
                owner = User.objects.get(username=username)
                # No añadir al propietario como colaborador
                if owner == request.user:
                    return Response({"detail": "No puedes añadirte a ti mismo como colaborador"}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                # No añadir colaboradores duplicados
                if owner in task.collaborators.all():
                    return Response({"detail": "El usuario ya es colaborador"}, 
                                    status=status.HTTP_400_BAD_REQUEST)
                    
                task.collaborators.add(owner)
                return Response({"detail": f"Usuario {username} añadido como colaborador"})
            except User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado"}, 
                                status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], serializer_class=CollaboratorSerializer)
    def remove_collaborator(self, request, pk=None):
        task = self.get_object()
        
        # Solo el propietario puede eliminar colaboradores
        if task.owner != request.user:
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