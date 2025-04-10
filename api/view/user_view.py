from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from models import user
from models import song
from models import message
from models import album
from serializer import userSerializer
# Create your views here.


