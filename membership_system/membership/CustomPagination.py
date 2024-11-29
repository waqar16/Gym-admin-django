from rest_framework.pagination import PageNumberPagination


# Custom Pagination Class
class CustomPageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        request = self.request
        # Add the port to next/previous links
        if response.data.get('next'):
            response.data['next'] = response.data['next'].replace(':80', ':8080')
        if response.data.get('previous'):
            response.data['previous'] = response.data['previous'].replace(':80', ':8080')
        return response
