import os
import joblib
import numpy as np
import re
import pandas as pd
from nltk.tokenize import word_tokenize
from django import forms
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from .models import Users, Emotion, Story, AnalyzedStory

# User registration
class Userform(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Last Name"}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "First Name"}))
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = Users
        fields = ['email', 'last_name', 'first_name', 'username', 'password', 'confirm_password']
    
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Password does not match!")
        return confirm_password
    
    def save(self, commit=True):
        users = super().save(commit=False)
        # Create user instance
        user = get_user_model().objects.create_user(username=self.cleaned_data['username'], email=self.cleaned_data['email'], last_name=self.cleaned_data['last_name'], first_name=self.cleaned_data['first_name'], password=self.cleaned_data['password'])
        user.save()
        users.account = user
        if commit:
            users.save()
        return users


# Get the current working directory
current_directory = os.path.dirname(os.path.realpath(__file__))

# Path of the saved model 
model_file_path = os.path.join(current_directory, 'model', 'OVA_Linear_model.pkl')

# Load the trained model and related objects from the file
model_components = joblib.load(model_file_path)
SVM_model, vectorizer, tfidf_transformer = model_components

# Path of the stopwords and stemmer data 
stopwords_file_path = os.path.join(current_directory, 'model', 'stopwords_tl.csv')
stemmer_file_path = os.path.join(current_directory, 'model', 'stem_tl.csv')

# Load stopwords and stemmer data
stopword = pd.read_csv(stopwords_file_path)
stopwords_set = set(stopword['stopword'])

stemmer = pd.read_csv(stemmer_file_path)
word_to_stem = dict(zip(stemmer['word'], stemmer['stem']))

replace_patterns = {
    re.compile(r"\bngayo\'y\b"): 'ngayon ay',
    re.compile(r"\bhangga\'t\b"): 'hanggang',
    re.compile(r"\b\'?y\b"): ' ay',
    re.compile(r"\b\'?t\b"): ' at',
    re.compile(r"\b\'?yan\b"): 'iyan',
    re.compile(r"\b\'?yo\b"): 'iyo',
    re.compile(r"\b\'?yon\b"): 'iyon',
    re.compile(r"\b\'?yun\b"): 'iyun',
    re.compile(r"\b\'?pagkat\b"): 'sapagkat',
    re.compile(r"\b\'?di\b"): 'hindi',
    re.compile(r"\b\'?kaw\b"): "ikaw",
    re.compile(r"\b\'?to\b"): 'ito',
    re.compile(r"\b\'?wag\b"): 'huwag',
    re.compile(r"\bgano\'n\b"): 'ganoon'
}

# Foul words set
foul_words = {
    'gago', 'gaga', 'puta', 'pakyu', 'pakshet', 'buang', 'walanghiya',
    'piste', 'lintik', 'putangina', 'tarantado', 'punyeta', 'bwisit',
    'kupal', 'hinyupak', 'tanga', 'tangina', 'bobo', 'boba', 'putragis', 'syet'
}

# Class names mapping
class_names = {
    1: 'Fear',
    2: 'Anger',
    3: 'Joy',
    4: 'Sadness',
    5: 'Disgust',
    6: 'Surprise'
}

# Preprocessing function
def data_preprocess(text, replace_patterns, word_to_stem, stopwords_set):
    text = text.lower()

    for pattern, replacement in replace_patterns.items():
        text = pattern.sub(replacement, text)

    text = re.sub(r"[^a-zA-Z0-9\s?!]", '', text)
    tokens = word_tokenize(text)
    text = ' '.join([word_to_stem.get(word, word) for word in tokens if word.lower() not in stopwords_set])

    return text


class StoryForm(forms.Form):
    story = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Enter text here...", "id": "text","class": "form"})
    )

    def save(self, request, commit=True):
        paragraph_text = self.cleaned_data['story']

        # Save the story to the Story table
        story_instance = Story.objects.create(story=paragraph_text)

        # Emotion prediction using the loaded model
        user_input_processed = data_preprocess(paragraph_text, replace_patterns, word_to_stem, stopwords_set)
        user_input_vectorized = vectorizer.transform([user_input_processed])
        user_input_tfidf = tfidf_transformer.transform(user_input_vectorized)
        decision_values = SVM_model.decision_function(user_input_tfidf)[0]
        exp_values = np.exp(decision_values - np.max(decision_values))
        probabilities = exp_values / exp_values.sum(axis=0, keepdims=True)

        probabilities_percentage = np.round(probabilities * 100, 2)

        # Find the emotion with the highest probability
        max_emotion_index = np.argmax(probabilities)
        max_emotion = class_names[max_emotion_index + 1]  

        # Save the analyzed story to the AnalyzedStory table with the logged-in user
        analyzed_story = AnalyzedStory(
            user=request.user.users if request.user.is_authenticated else None,
            phrase=story_instance,  
            fear=probabilities_percentage[0],
            anger=probabilities_percentage[1],
            joy=probabilities_percentage[2],
            sadness=probabilities_percentage[3],
            disgust=probabilities_percentage[4],
            surprise=probabilities_percentage[5],
            analyzed_emotion=Emotion.objects.get(emotion=max_emotion) 
        )
        analyzed_story.save()

        return paragraph_text

