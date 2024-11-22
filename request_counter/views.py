from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .middleware import RequestCountMiddleware

class RequestCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        count = RequestCountMiddleware.get_request_count()
        return Response({
            'requests': count
        })

class RequestCountResetView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        RequestCountMiddleware.reset_request_count()
        return Response({
            'message': 'request count reset successfully'
        })