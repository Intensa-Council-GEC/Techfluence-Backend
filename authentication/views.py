from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import ListAPIView
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .serializers import *
from .threads import *
from .models import *
from .utils import *
import xlrd


@api_view(["POST"])
def addOrganisers(request):
    try:
        ser = AddOrganiserSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            file = ser.data["file"]
            path = str(settings.BASE_DIR)+str(file)
            workbook = xlrd.open_workbook(path)
            sheet = workbook.sheet_by_index(0)
            for row in range(1,sheet.nrows):
                org = OrganisersModel.objects.create(
                        name = str(sheet.cell_value(row,0)),
                        email = str(sheet.cell_value(row,1)).lower(),
                        phone = sheet.cell_value(row,2)
                    )
                pw = get_random_string(8)
                org.set_password(pw)
                thread_obj = send_organisers_mail(str(sheet.cell_value(row,1)).lower(), pw)
                thread_obj.start()
                org.save()
            return Response({"message":"Organisers Added"}, status=status.HTTP_201_CREATED)
        return Response({"error":ser.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def organiser_login(request):
    try:
        data = request.data
        serializer = loginSerializer(data=data)
        if serializer.is_valid():
            email = str(serializer.data["email"]).lower()
            password = serializer.data["password"]
            customer_obj = OrganisersModel.objects.filter(email=email).first()
            if customer_obj is None:
                print("Account does not exist")
                return Response({"message":"Account does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user = authenticate(email=email, password=password)
            if not user:
                print("Incorrect password")
                return Response({"message":"Incorrect password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
            jwt_token = RefreshToken.for_user(user)
            return Response({"message":"Login successfull", "token":str(jwt_token.access_token)}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def organiser_forgot(request):
    try:
        data = request.data
        serializer = emailSerializer(data=data)
        if serializer.is_valid():
            email = str(serializer.data["email"]).lower()
            user = OrganisersModel.objects.get(email=email)
            if not user:
                return Response({"message":"Account does not exists"}, status=status.HTTP_404_NOT_FOUND)
            otp = uuid.uuid4()
            user.token = otp
            print(otp)
            user.save()
            thread_obj = send_forgot_email(email, otp)
            thread_obj.start()
            return Response({"message":"reset mail sent"}, status=status.HTTP_200_OK)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def organiser_reset(request):
    try:
        data = request.data
        serializer = otpSerializer(data=data)
        if serializer.is_valid():
            otp = serializer.data["otp"]
            if not OrganisersModel.objects.filter(token=otp).first():
                return Response({"message":"user does not exist"}, status=status.HTTP_404_NOT_FOUND)
            user_obj = OrganisersModel.objects.get(token=otp)
            pw = serializer.data["pw"]
            user_obj.set_password(pw)
            user_obj.token = None
            user_obj.save()
            return Response({"message":"Password changed successfull"}, status=status.HTTP_202_ACCEPTED)
        return Response({"error":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return Response({"error":str(e), "message":"Something went wrong"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetColleges(ListAPIView):
    queryset = CollegeModel.objects.all()
    serializer_class = CollegesSerializer

