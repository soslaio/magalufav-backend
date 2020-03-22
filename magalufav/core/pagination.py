
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'meta': {
                'page_number': self.page.number,
                'page_size': self.page_size
            },
            'favorites': data
        })
