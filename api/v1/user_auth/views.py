from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.generics import RetrieveAPIView, CreateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api.v1.user_auth.serializers import UserDetailSerializer, UserCreateSerializer, UserLoginSerializer
from user.models import User


class AuthDetailAPIView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class AuthRegisterAPIView(CreateAPIView):
    model = User
    permission_classes = [AllowAny]
    serializer_class = UserCreateSerializer

    def __init__(self):
        self.obj = None

    def perform_create(self, serializer):
        self.obj = serializer.save()

    @swagger_auto_schema(
        responses={
            201: "User created successfully",
            400: "Bad data"})
    def post(self, request, *args, **kwargs):
        """Registers (creates) a new user from the provided fields,
        generates and provides a new authentication token"""
        response = super().post(request, *args, **kwargs)
        token, _ = Token.objects.get_or_create(user=self.obj)

        return Response({"token": token.key}, status.HTTP_201_CREATED)


class AuthLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    @swagger_auto_schema(
        responses={
            200: "User token",
            400: "Bad credentials",
            404: "User not found"})
    def post(self, request):
        """Provides a user with an authentication token
        if credentials are correct"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = User.objects.filter(username=serializer.validated_data["username"]).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        token, _ = Token.objects.get_or_create(user=user)
        if user.check_password(serializer.validated_data["password"]):
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
