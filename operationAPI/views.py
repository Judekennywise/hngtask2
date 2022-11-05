from os import environ
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView
from .serializers import OperationSerializer
from django.http import JsonResponse
from rest_framework.response import Response
import openai
from .gpt import GPT, Example
import os 

openai.api_key = os.environ.get('OPEN_API_KEY')
gpt = GPT(engine="davinci",
          temperature=0.5,
          output_prefix="",
          max_tokens=100)
gpt2 = GPT(engine="davinci",
          temperature=0.5,
          output_prefix="",
          max_tokens=100)

# add some calculation examples
gpt.add_example(Example("Add 3+5", "8"))
gpt.add_example(Example("Add 8 and 5 together", "13"))
gpt.add_example(Example("Can you please add 50 and 25", "75"))
gpt2.add_example(Example("Can you please add 50 and 25", "addition"))
gpt2.add_example(Example("Can you please add the following numbers together - 10 and 25", "addition"))
gpt.add_example(Example("Can you please add the following numbers together - 4 and 13", "17"))
gpt.add_example(Example("subtract 4 from 8", "4"))
gpt.add_example(Example("what is the prduct of 4 and 5", "20"))
gpt.add_example(Example("Can you multiply 4 by 6", "24"))
gpt2.add_example(Example("what is the product of 5 and 6", "multiplication"))
gpt2.add_example(Example("Add 3+5", "addition"))
gpt2.add_example(Example("Add 8 and 5 together", "addition"))
gpt2.add_example(Example("subtract 4 from 8", "subtraction"))
gpt2.add_example(Example("Can you multiply 4 by 6", "multiplication"))





# Create your views here.
class OperationsView(CreateAPIView):
    serializer_class = OperationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            print(gpt.get_all_examples())
            operation_type = serializer.data['operation_type']
            try:
                x = serializer.data['x']
                y = serializer.data['y']
            except KeyError:
                pass
            if operation_type == 'addition':
                result = x + y
                response = JsonResponse({'slackUsername':'judekennywise','result': result, 'operation_type' : operation_type})
            elif operation_type == 'subtraction':
                result = x - y
                response = JsonResponse({'slackUsername':'judekennywise','result': result, 'operation_type' : operation_type})
            elif operation_type == 'multiplication':
                result = x * y
                response = JsonResponse({'slackUsername':'judekennywise','result': result, 'operation_type' : operation_type})
            else:
                result = gpt.get_top_reply(operation_type)
                result2 = gpt2.get_top_reply(operation_type)
                response = JsonResponse({'slackUsername':'judekennywise','result': result.strip("\n\n"), 'operation_type' : result2.strip("\n\n") })
            return response
            
