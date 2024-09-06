from django.shortcuts import render
from rest_framework.response import Response
from hackmanage.models import Hackathon,Submission
from hackmanage.serializer import SubmissionSerializer,ListHackathonSerializer,CreateHackathonSerializer,UserSerializer,LoginSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate



# Create your views here.

@api_view(["POST"])
def signup(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@api_view(["GET"])
def hackathon_list(request):
    try:
        hacks = Hackathon.objects.all()  
        serializer = ListHackathonSerializer(hacks,many=True)
        
        return Response(
            {"message":serializer.data},
            status=status.HTTP_200_OK
        )

    except ValidationError as e:
        return Response(
           {"error":str(e)},
            status=400
        )
    
    except Exception as e:
        return Response(
            {"error":str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR 
        )


@api_view(['POST'])
@permission_classes([IsAdminUser])
def hackathon_create(request):
    try:
        serializer = CreateHackathonSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data = serializer.data
        hack = Hackathon.objects.create(**serialized_data)
        # hack = Hackathon.objects.filter().order_by("-created_at").first()
        return Response(
            {"message":f"Hackathon is successfully created - {hack.hack_id}"},
             status=status.HTTP_201_CREATED
        )
    
    except ValidationError as e:
        return Response(
           {"error":str(e)},
            status=400
        )
    
    except Exception as e:
        return Response(
            {"error":str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR 
        )
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def register_hackathon(request):
    user = request.user
    hack_id = request.data.get("hack_id")
    if not hack_id:
        return Response(
            {"message":"No hack id found"},
            status=status.HTTP_404_NOT_FOUND
        )
    try:
        hackathon = Hackathon.objects.filter(hack_id=hack_id)
        if not hackathon:
            return Response(
            {"message":f"No hackathon found for the {hack_id}"},
            status=status.HTTP_404_NOT_FOUND
        )
        hackathon = hackathon.first()
        
        hackathon.user.add(user)
        return Response(
            {"message":f"Successfully registered for hackathon - {hackathon.tittle}"},
            status=status.HTTP_202_ACCEPTED
        )

    except ValidationError as e:
        return Response(
            {"message":e},
            status=status.HTTP_400_BAD_REQUEST
        )

    except Exception as e:
        return Response(
            {
                "message":e
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def enrolled_hackathons(request):
    user = request.user
    hacks = Hackathon.objects.filter(user=user)

    try:
        serialized_hacks = ListHackathonSerializer(hacks,many=True)
        
        return Response({
            "enrolled hackathons":serialized_hacks.data,
        },status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response(
            {
                "message":str(e)
            }, status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        return Response(
            {
                "message":str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_submissions(request):
    user = request.user
    submissions = Submission.objects.filter(user=user)

    try:
        serializer = SubmissionSerializer(submissions,many=True)
        return Response({
            'message':serializer.data,
        },status=status.HTTP_200_OK)

    except ValidationError as e:
        return Response(
            {
                "message":str(e)
            }, status=status.HTTP_404_NOT_FOUND
        )
    
    except Exception as e:
        return Response(
            {
                "message":str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_submission(request):
    user = request.user
    hack_id = request.data.get("hack_id")
    if not hack_id:
        return Response(
            {"message":"No hack id found"},
            status=status.HTTP_404_NOT_FOUND
        )
    user_registered_hack_ids = user.hackathons.values_list('hack_id', flat=True)
    if hack_id not in user_registered_hack_ids:
        return Response(
            {
                "message":f"Kindly register to the hackathon - {hack_id} before you submit"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        hackathon = Hackathon.objects.filter(hack_id=hack_id)
        if not hackathon:
            return Response(
            {"message":f"No hackathon found for the {hack_id} for submission"},
            status=status.HTTP_404_NOT_FOUND
        )

        hackathon = hackathon.first()
        subsmission = Submission(
            description=request.data['description'],
            user_submission_type=request.data['user_submission_type'],
            user_submission=request.data['user_submission'],
            hackathon=hackathon,
            user=request.user 
        )

        subsmission.save()


        return Response(
            {"message":f"Successfully submitted - {subsmission.submission_id}"},
             status=status.HTTP_201_CREATED
        )
    except IntegrityError as e:
        return Response(
            {
                "integreted issue ":str(e)
            },
            status=status.HTTP_400_BAD_REQUEST
        )
    
    except ValidationError as e:
        return Response(
           {"error":str(e)},
            status=400
        )
    
    except Exception as e:
        return Response(
            {"error":str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR 
        )