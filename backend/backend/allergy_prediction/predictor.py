import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
import pickle

ALLERGENS_FOOD_TYPES = ['Cereal grain and pulse', 'Dairy', 'Fruit', 'Citrus Fruit',
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


class Predictor:
    """
        Predictor object Handles Allergy and Food Type predictions
    """

    def __init__(self):
        self.df = shuffle(pd.read_csv('backend/allergy_prediction/new_dataset.csv'))
        # classifiers saved location
        self.file_name_allergy = 'backend/allergy_prediction/saved_models/mod_allergy_classifier.sav'
        self.file_name_food_type = 'backend/allergy_prediction/saved_models/mod_food_type_classifier.sav'

    def train_models(self):
        """
            Trains the two models and save them with the help of save_models() method
        """

        # preprocess
        self.preprocess()
        # encode
        self.encode_datasets()

        # For Allergy: GaussianNB classifier with tuned parameters
        gnb = GaussianNB(var_smoothing=0.0533669923120631)
        # training
        gnb.fit(self.x_allergy, self.y_allergy)

        # For Food Type: Decision Tree classifier with tuned parameters
        dtc = DecisionTreeClassifier(
            max_depth=11,
            max_features=None,
            max_leaf_nodes=50,
            min_samples_leaf=8,
            min_weight_fraction_leaf=0.1,
            splitter='random'
        )

        # training
        dtc.fit(self.x_food_type, self.y_food_type)

        self.save_models(gnb, dtc)

    def save_models(self, allergy_model, food_type_model):
        """
            Responsible for saving trained models

            :param allergy_model: The trained models object(GaussianNB()) of allergy predictions
            :type allergy_model: <class 'sklearn.naive_bayes.GaussianNB'>
            :param food_type_model: The trained models object(DecisionTreeClassifier()) of food type predictions
            :type food_type: <class 'sklearn.tree._classes.DecisionTreeClassifier'>

            :returns: None
        """

        with open(self.file_name_allergy, 'wb') as f:
            pickle.dump(allergy_model, f)

        with open(self.file_name_food_type, 'wb') as f:
            pickle.dump(food_type_model, f)

    def get_predictions(self, **kwargs):
        """
            Responsible for getting predictions for the passed data as kwargs

            :param \**kwargs:
                See below

            :Keyword Arguments:
                **age_type*(``str``) --
                  Provided age type of the user
                **amount_taken*(``str``) --
                  Provided food amount taken by the user
                **symptoms*(``list``) --
                  Provided symptoms by the user

            :returns: tuple containing
                predicted_allergy(``str``)
                predicted_food_type(``str``)
            :rtype: tuple
        """

        input_df = pd.DataFrame(data=None, columns=self.df.columns, index=self.df.index).dropna()
        input_df.drop(['Allergy', 'Food_Type', 'Food_Item'], axis=1, inplace=True)

        # insert data into dataframe
        data = [0 for i in range(input_df.shape[1])]
        data[0] = kwargs['age_type']
        data[1] = kwargs['amount_taken']

        input_df = input_df.append(pd.DataFrame([data], columns=input_df.columns))

        # mark symptoms 1 df
        for symptom in eval(kwargs['symptoms']):
            input_df[symptom] = 1

        # copy of df
        input_df_copy = input_df.copy()

        # transformation for allergy preds
        input_df = self.trained_oe_x_allergy.transform(input_df)

        # load saved file for allergy classifier
        classifier_allergy = pickle.load(open(self.file_name_allergy, 'rb'))

        # get allergy preds
        pred = classifier_allergy.predict(input_df)
        predicted_allergy = self.trained_oe_y_allergy.inverse_transform(pred.reshape(-1, 1))[0][0]
        print('Predicted Allergy: {}'.format(predicted_allergy))

        # add predicted allergy to dataset
        idx = 0
        input_df_copy.insert(loc=idx, column='Allergy', value=[predicted_allergy])

        # transformations for food type preds
        input_df_copy = self.trained_oe_x_food_type.transform(input_df_copy)

        # load saved file for food type classifier
        classifier_food_type = pickle.load(open(self.file_name_food_type, 'rb'))

        # get food type preds
        pred = classifier_food_type.predict(input_df_copy)
        predicted_food_type = self.trained_oe_y_food_type.inverse_transform(pred.reshape(-1, 1))[0][0]
        print('Predicted Food Type: {}'.format(predicted_food_type))

        return predicted_allergy, predicted_food_type

    def new_symptom_cols(self, row, col_name):
        """
            Create seperate columns for each symptom

            :param row: Row index of the record
            :type row: int
            :param col_name: Column name created for a symptom
            :type col_name: str

            :returns(``int``): Symptom is presented(1) or not(0)
            :rtype: int
        """
        if col_name in row['Symptoms']:
            return 1
        return 0

    def preprocess(self):
        """
            Preprocess the dataset
            :params:None
            :returns: None
        """

        for symptom in SYMPTOM_LIST:
            self.df[symptom] = self.df.apply(lambda x: self.new_symptom_cols(x, symptom), axis=1)

        self.df.drop('Symptoms', axis=1, inplace=True)

        # Selecting Columns For Allergy Predictions
        self.x_allergy = self.df.drop(['Allergy', 'Food_Type', 'Food_Item'], axis=1)
        self.y_allergy = self.df[['Allergy']]

        # Selecting Columns For Food Type Predictions
        self.x_food_type = self.df.drop(['Food_Type', 'Food_Item'], axis=1)
        self.y_food_type = self.df[['Food_Type']]

    def encode_datasets(self):
        """
            Encodes the dataset

            :params:None
            :returns: None
        """
        # ordinal encoders
        self.ordinal_encoder_x_allergy = preprocessing.OrdinalEncoder(
            handle_unknown='use_encoded_value',
            unknown_value=20
        )
        self.ordinal_encoder_y_allergy = preprocessing.OrdinalEncoder(
            handle_unknown='use_encoded_value',
            unknown_value=20
        )
        self.ordinal_encoder_x_food_type = preprocessing.OrdinalEncoder(
            handle_unknown='use_encoded_value',
            unknown_value=20
        )
        self.ordinal_encoder_y_food_type = preprocessing.OrdinalEncoder(
            handle_unknown='use_encoded_value',
            unknown_value=20
        )

        # trained ordinal encorder for allergy predictions
        self.trained_oe_x_allergy = self.ordinal_encoder_x_allergy.fit(self.x_allergy)
        self.trained_oe_y_allergy = self.ordinal_encoder_y_allergy.fit(self.y_allergy)
        # trained ordinal encorder for food_type predictions
        self.trained_oe_x_food_type = self.ordinal_encoder_x_food_type.fit(self.x_food_type)
        self.trained_oe_y_food_type = self.ordinal_encoder_y_food_type.fit(self.y_food_type)

        # applying transformations for allery dataset
        self.x_allergy = self.trained_oe_x_allergy.transform(self.x_allergy)
        self.y_allergy = self.trained_oe_y_allergy.transform(self.y_allergy)
        # applying transformations for food type dataset
        self.x_food_type = self.trained_oe_x_food_type.transform(self.x_food_type)
        self.y_food_type = self.trained_oe_y_food_type.transform(self.y_food_type)

        # encoded classes
        self.ALLERGY_CLASSES = self.trained_oe_y_allergy.categories_[0]
        self.FOOD_TYPE_CLASSES = self.trained_oe_y_food_type.categories_[0]

