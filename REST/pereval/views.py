from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .serializers import *

STATUS_DICT = dict(PEREVAL_POSSIBLE_STATUSES)

class PartialModelViewSet(mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """Abstract class that does not implement destroy()"""
    pass


class PerevalViewSet(PartialModelViewSet):
    """API endpoint that allows users to view or add perevals.
    Use null for optional fields, or don't include them.
    Do NOT use "" as value for optional fields! """
    queryset = Added.objects.all()
    serializer_class = PerevalSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__email', 'status']
    lookup_field = 'pk'

    def create(self, request, *args, **kwargs):
        """Formats response for POST mehtod as per specification.
        Note: doesn't format JSON syntax errors, or 500 errors.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=False):
            return Response({'status': 400, 'message': str(serializer.errors), 'id': None},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print(serializer.__dict__)
        return Response({'status': 201, 'message': None, 'id': serializer.instance.pk},
                        status=status.HTTP_201_CREATED, headers=headers)

    def get_serializer_class(self):
        """Returns different type of serializer for update"""
        if self.action == 'update':
            return PerevalUpdateSerializer
        else:
            return PerevalSerializer

    def update(self, request, *args, **kwargs):
        """Formats response for PUT and PATCH mehtods as per specification.
        Also disallows editing if status is different from new.
        Note: doesn't format JSON syntax errors, or 500 errors.
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if instance.status != 'new':
            return Response({'status': 400,
                             'message': f'Отчёт о перевале имеет статус "{STATUS_DICT[instance.status]}" '
                                        f'и не может быть изменён. Пожалуйста, обратитесь к модератору',
                             'id': instance.pk},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid(raise_exception=False):
            return Response({'status': 400, 'message': str(serializer.errors), 'id': instance.pk},
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response({'status': 200, 'message': None, 'id': serializer.instance.pk},
                        status=status.HTTP_200_OK)



