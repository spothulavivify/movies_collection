from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import MovieService
# from rest_framework.permissions import IsAuthenticated, AllowAny

class MovieListView(APIView):
    def get(self, request):
        try:
            page = request.query_params.get('page', 1)
            movie_service = MovieService()
            movies_data = movie_service.get_movies(page)
            return Response(movies_data)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )