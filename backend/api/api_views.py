from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication
from rest_framework import authentication, permissions, status
from api.serializers import *
from backend.allergy_prediction import predictor


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
        foods = Food.objects.values_list('food', flat=True).order_by('food')
        context = {
            'food_items': foods,
            'symptoms': predictor.SYMPTOM_LIST
        }

        return Response(context, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        amount_taken = request.POST['amount_taken']
        symptoms_list = request.POST['symptoms_list']
        food_list = request.POST['food_list']

        if amount_taken.lower() == 'Small Amount':
            amount_taken = 'Small Amount'
        else:
            amount_taken = 'Large Amount'

        age = Patient.objects.get(user=request.user.id).age

        age_type = AgeType.objects.filter(
            min_range__lte=age,
            max_range__gte=age
        )[0].get_type_display()

        prdtr = predictor.Predictor()
        prdtr.train_models()

        allergy, food_type = prdtr.get_predictions(
            age_type=age_type,
            amount_taken=amount_taken,
            symptoms=symptoms_list
        )

        food_type_obj = FoodType.objects.filter(food_type__contains=food_type).values_list('id', flat=True)

        foods = list(Food.objects.filter(food_type__in=food_type_obj).values_list('food', flat=True))
        foods = [food.lower() for food in foods]

        allergens = [food for food in eval(food_list) if food.lower() in foods]

        references = Reference.objects.filter(allergy__allergy__contains=allergy)

        serializer = ReferenceSerializer(references, many=True)

        context = {
            'predicted_allergy': allergy,
            'predicted_food_type': food_type,
            'possible_allergens': allergens,
            'references': serializer.data
        }

        return Response(context, status=status.HTTP_200_OK)

