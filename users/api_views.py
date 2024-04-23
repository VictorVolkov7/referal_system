import time

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserSerializer, UserProfileSerializer, CodeProfileSerializer
from users.services import generate_random_passcode, send_sms


class UserRegAuthAPIView(APIView):
    """
    API endpoint that allows to be created users and sent SMS code.
    """
    serializer_class = UserSerializer

    def post(self, request):
        """
        Creating a new user by sending an SMS code
        or sending SMS code to existing SMS user.
        :param request: data sent by the client.
        :return: response data.
        """
        # getting phone number
        data = request.data
        phone_number = data.get('phone_number')

        if not phone_number:
            return Response({'error': _('Missing phone_number in request')}, status=status.HTTP_400_BAD_REQUEST)

        # generating pass code
        pass_code = generate_random_passcode()
        # search user for phone number
        user = User.objects.filter(phone_number=phone_number).first()

        if not user:
            # If user doesn't exist, create a new one
            creation = self.user_creation(phone_number, pass_code)
            if creation:
                # If creation was successful, an SMS is sent
                send_sms(phone_number, pass_code)
                return Response({'detail': _(f'User created and pass code {pass_code} sent successfully')},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'error': _('The phone number entered is not valid.')},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            # If user exists, update pass_code and send it
            user.pass_code = pass_code
            user.save()
            send_sms(phone_number, pass_code)
            return Response({'detail': _(f'Pass code {pass_code} sent successfully')}, status=status.HTTP_200_OK)

    def user_creation(self, phone_number, pass_code) -> bool:
        """
        Creating a new user.
        :param phone_number: user phone number
        :param pass_code: generated pass code
        :return: True or False
        """
        user_data = {'phone_number': phone_number, 'pass_code': pass_code}
        user_serializer = self.serializer_class(data=user_data)

        if user_serializer.is_valid():
            user_serializer.save()
            return True
        else:
            errors = user_serializer.errors
            print("Validation errors:", errors)
            return False


class UserLoginAPIView(APIView):
    """
    API endpoint that allows to auth a user.
    """

    @staticmethod
    def post(request):
        """
        Authenticate user using SMS code.
        """
        # getting pass code
        pass_code = request.data.get('pass_code')

        if not pass_code:
            return Response({'error': _('Missing pass_code in request')}, status=status.HTTP_400_BAD_REQUEST)

        # search user for pass code
        user = User.objects.filter(pass_code=pass_code).first()

        if not user:
            # If user doesn't exist returned error
            return Response({'error': _('Invalid pass code')}, status=status.HTTP_400_BAD_REQUEST)

        # Clear pass_code after successful authentication
        user.pass_code = None
        user.save()

        # Generating JWT token
        token = RefreshToken.for_user(user).access_token

        return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserProfileAPIView(RetrieveUpdateAPIView):
    """
    API endpoint that allows to retrieve user profile information.
    """
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Retrieve user profile information.
        :return: current user profile
        """
        return self.request.user

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserProfileSerializer
        else:
            return CodeProfileSerializer

    def post(self, request):
        # getting referral code
        referral_code = request.data.get('referral_code')

        if not referral_code:
            # If referral code doesn't exist returned error
            return Response({'error': _('Missing referral_code in request')}, status=status.HTTP_400_BAD_REQUEST)

        # search user for referral_code
        referred_user = User.objects.filter(referral_code=referral_code).first()

        if not referred_user:
            # If referred user code doesn't exist returned error
            return Response({'error': _('User with provided referral_code does not exist')},
                            status=status.HTTP_400_BAD_REQUEST)

        # Getting current user
        referring_user = self.request.user

        if referring_user.referred_code:
            # If the user has activated a referral code
            return Response({'error': _('You have already activated your referral code.')},
                            status=status.HTTP_400_BAD_REQUEST)
        elif referring_user.referral_code == referral_code:
            # If the user tries to activate their code
            return Response({'error': _('You cannot activate your referral code.')}, )
        else:
            # Adding current user to referred user in him referrals
            referred_user.referrals.add(referring_user)
            # Adding referral code like referred
            referring_user.referred_code = referral_code
            referred_user.save()
            referring_user.save()
            return Response({'message': _('You have successfully activated referral code.')},
                            status=status.HTTP_200_OK)
