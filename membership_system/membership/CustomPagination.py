from rest_framework.pagination import PageNumberPagination
from django.conf import settings


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        request = self.request
        base_url = settings.BASE_URL
        if response.data.get('next'):
            response.data['next'] = response.data['next'].replace(request._current_scheme_host, base_url)
        if response.data.get('previous'):
            response.data['previous'] = response.data['previous'].replace(request._current_scheme_host, base_url)
        return response
