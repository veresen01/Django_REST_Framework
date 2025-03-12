from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .serializers import UserSerializer
from .models import User


class UserRegistration(APIView):
    @extend_schema(
        summary="Регистрация пользователя",
        description="Создаёт нового пользователя с уникальным email, именем, фамилией, возрастом и профессией. "
                    "Возраст должен быть в пределах от 16 до 99 лет. Если профессия не указана, подставляется значение "
                    "'Безработный(ая)'.",
        request=UserSerializer, #Указание на сериализатор, который используется для обработки входящих данных.
        responses={
            201: OpenApiResponse(response=UserSerializer, description="Пользователь успешно создан"),
            400: OpenApiResponse(description="Ошибки валидации") #Описание возможных ответов, включая коды статусов и сериализаторы для успешных и ошибочных ответов.
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"status": "User created", "id": user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
#Метод для получения списка всех пользователей    
class UserList(APIView):
    #Определили декоратор extend_schema для описания нашего метода, указав краткое описание, подробное описание и возможные ответы.
    @extend_schema(
        summary="Получение информации обо всех пользователях",
        description="Возвращает список всех зарегистрированных пользователей.",
        responses={
            200: OpenApiResponse(response=UserSerializer(many=True), description="Список всех пользователей")
        }
    )
    def get(self, request):
        users = User.objects.all() #Получили всех пользователей из базы данных с помощью User.objects.all().
        serializer = UserSerializer(users, many=True) #Сериализовали данные пользователей с помощью UserSerializer, передав параметр many=True для обработки списка объектов.
        return Response(serializer.data)  #Вернули сериализованные данные в ответе с помощью Response(serializer.data).

#метод для получения информации про одного пользователя по его ID.
class UserDetail(APIView):
    @extend_schema(
        summary="Получение информации о пользователе",
        description="Возвращает информацию о пользователе по его ID.",
        responses={
            200: OpenApiResponse(response=UserSerializer, description="Информация о пользователе"),
            404: OpenApiResponse(description="Пользователь не найден")
        }
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    
#Метод для удаления пользователя по его ID
class UserDelete(APIView):
    @extend_schema(
        summary="Удаление пользователя",
        description="Удаляет пользователя по его ID. Если пользователь не найден, возвращает ошибку.",
        responses={
            200: OpenApiResponse(description="Пользователь успешно удалён"),
            404: OpenApiResponse(description="Пользователь не найден"),
            400: OpenApiResponse(description="ID пользователя не предоставлен")
        }
    )
    def delete(self, request, user_id):
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                user.delete()
                return Response({"status": "User deleted"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "User ID not provided"}, status=status.HTTP_400_BAD_REQUEST)
    
    
#Метод для удаления всех пользователей
class UserDeleteAll(APIView):
    @extend_schema(
        summary="Удаление всех пользователей",
        description="Удаляет всех пользователей из базы данных.",
        responses={
            200: OpenApiResponse(description="Все пользователи успешно удалены")
        }
    )
    def delete(self, request):
        User.objects.all().delete()
        return Response({"status": "All users deleted"}, status=status.HTTP_200_OK)