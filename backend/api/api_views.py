from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework import authentication, permissions, status
from api.serializers import *

ALLERGENS = ['Cereal grain and pulse', 'Dairy', 'Fruit', 'Citrus Fruit',
       'Nut and seed', 'Poultry', 'Meat', 'SeaFood', 'Vegetable']
SYMPTOM_LIST = ['Frequent Inflammation', 'Diarrhea with smelly stools', 'Vomiting',
       'Abdominal distention', 'Inflammation in the small intestine',
       'Frequent diarrhea / Constipation', 'Fatigue ',
       'Blistering skin condition', 'Leg or arm numbness',
       'Eye irritation', 'Canker sores inside the mouth',
       'Swelling in the face', 'Nausea and vomiting',
       'Runny or stuffed nose', 'Loss of consciousness',
       'Rapid and irregular pulse', 'Itchiness in the mouth', 'Dizziness',
       'Wheezing', 'Tingling feeling around the lips or mouth',
       'Loose stools or diarrhea', 'Coughing or shortness of breath',
       'Slight swelling and bumpiness of the mouth, throat, or lips',
       'Difficulty swallowing or breathing',
       'Itching and tingling of the mouth, throat, and sometimes lips',
       'Sinus infection and inflammation', 'Nasal and sinus polyps',
       'Gas or Diarrhea', 'Gut inflammation (colitis)', 'Tissue swelling',
       'Stuffy nose', 'Swelling of the skin - angioedema',
       'Narrowing of the throat', 'Extreme itching',
       'Dry, scaly, flaky skin', 'Swelling and Blisters',
       'skin redness and skin that burns', 'Bumps on the skin (hives)',
       'Swelling around the mouth, and vomiting',
       'Stomach pains, or diarrhoea', 'Itchy skin and rash',
       'Wheeze or persistent cough', 'Paleness and floppiness',
       'Difficulty talking or a hoarse voice',
       'Irritated, red skin, or an eczema-like rash',
       'Skin inflammation/burning', 'Bloating', 'Chest tightness',
       'Nasal congestion/runny nose', 'Rapid pulse',
       'Coughing or wheezing', 'Red, irritated skin',
       'An inflamed or swollen throat', 'Swollen tongue or lips',
       'Swollen, watery eyes', 'Reddened Skin', 'Raised circular weals',
       'Indigestion', 'Swollen, waterly eyes', 'Lightheadedness',
       'Diarrhea', 'Skin irritation, hives and rashes',
       'Cramping and bloating', 'Difficulty in breathing',
       'Runny nose and watery eyes', 'Swelling', 'Tingling', 'Nausea',
       'Coughing', 'Hives or a rash anywhere on the body',
       'Tingling or itching in the mouth', 'Stomach pains', 'Cramping',
       'Gas', 'Dizziness or lightheadedness',
       'Tingling sensation on your lips', 'Sneezing and Runny nose',
       'A little drop in blood pressure', 'Achy muscles and joints',
       'Itchiness and Loss of consciousness']


class UserAPIView(APIView):
    """ Control user details """

    authentication_classes = [JWTTokenUserAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.id)
        serializer = UserSerializer(user)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        sex = request.POST['sex']
        allergies = request.POST['allergies']
        age = request.POST['age']
        family_history = request.POST['family_history']
        drug_allergies = request.POST['drug_allergies']

        if sex.lower() == 'male':
            sex = Patient.MALE
        else:
            sex = Patient.FEMALE

        if allergies == 'true' or 'True':
            allergies = Patient.YES
        else:
            allergies = Patient.NO
        if family_history == 'true' or 'True':
            family_history = True
        else:
            family_history = False
        if drug_allergies == 'true' or 'True':
            drug_allergies =True
        else:
            drug_allergies = False

        user = User.objects.get(pk=request.user.id)

        if Patient.objects.filter(user=user).exists():
            patient = Patient.objects.filter(user=user).update(
                sex=sex,
                allergies=allergies,
                age=age,
                family_history=family_history,
                drug_allergies=drug_allergies
            )
        else:
            patient = Patient.objects.create(
                user=user,
                sex=sex,
                allergies=allergies,
                age=age,
                family_history=family_history,
                drug_allergies=drug_allergies
            )

        serializer = UserSerializer(user)

        context = {
            'detail': 'User details updated!',
            'data': serializer.data
        }

        return Response(context, status=status.HTTP_200_OK)


class AllergyAPIView(APIView):
    """ Gets predictions """

    def get(self, request, *args, **kwargs):
        context = {
            'food_items': ALLERGENS,
            'symptoms': SYMPTOM_LIST
        }

        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        age_type = request.POST['age_type']
        amount_taken = request.POST['amount_taken']
        symptoms_list = request.POST['symptoms_list']
        food_list = request.POST['food_list']
        


        

