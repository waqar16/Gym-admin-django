from rest_framework.pagination import PageNumberPagination
import os


class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        request = self.request
        base_url = os.getenv('BASE_URL', 'http://localhost:8080')  # Fallback if not set
        if response.data.get('next'):
            response.data['next'] = response.data['next'].replace(request._current_scheme_host, base_url)
        if response.data.get('previous'):
            response.data['previous'] = response.data['previous'].replace(request._current_scheme_host, base_url)
        return response
