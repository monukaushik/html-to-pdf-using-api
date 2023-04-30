from django.shortcuts import render
from .serializers import StudentSerializer
from .models import Student
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from myapp import *


from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
import uuid  
from django.conf import settings 
# Create your views here.

class StudentList(APIView):
    def get(self, request, format=None):
        student_obj = Student.objects.all()
        serializer = StudentSerializer(student_obj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def save_pdf(params:dict):
    template=get_template("pdf.html")
    html=template.render(params)
    response=BytesIO()
    pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name=uuid.uuid4()

    try:
        with open(f'{str(settings.BASE_DIR)}/media/uploads/{file_name}.pdf', 'wb+') as output:
            pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
    except Exception as e:
        print(e)  

    return ('', False) if pdf.err else (file_name, True)
    
class GeneratePdf(APIView):
    def get(self,request):
        student_obj = Student.objects.all()
        params={
            'student_obj':student_obj
        }
        file_name, status=save_pdf(params)
        
        if not status:
            return Response({'status':400})  
        return Response({'status':200, 'path':f'/media/uploads/{file_name}.pdf'})    
    
    