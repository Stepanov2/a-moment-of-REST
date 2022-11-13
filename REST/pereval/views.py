from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import *


class PartialModelViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """Abstract class that does not implement update() or destroy()"""
    pass


class PerevalViewSet(PartialModelViewSet):
    """API endpoint that allows users to view or add perevals.
    Use null for optional fields, or don't include them.
    Do NOT use "" as value for optional fields! """
    queryset = Added.objects.all().order_by('status', '-add_time')
    serializer_class = PerevalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email', 'status']

    def create(self, request, *args, **kwargs):
        """Formats response as per specification."""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({'status': 400, 'message': str(serializer.errors), 'id': None},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.__dict__)
        return Response({'status': 201, 'message': None, 'id': serializer.instance.pk},
                        status=status.HTTP_201_CREATED, headers=headers)

    def get(self, request, *args, **kwargs):
        pass