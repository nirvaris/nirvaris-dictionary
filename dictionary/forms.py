import pdb

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from .models import Comment


class UploadCSVForm(forms.Form):
    file = forms.FileField()

class SearchForm(forms.Form):
    search_input = forms.CharField(required=True, label=_('Search'), max_length=200)

class CommentForm(forms.ModelForm):

    name = forms.CharField(required=False, label=_('Name'), max_length=200)
    email = forms.EmailField(required=False, label=_('Email'), max_length=200)
    word_entry_id = forms.CharField(required=True, widget=forms.HiddenInput())
    
    class Meta:
        model = Comment
        fields =[
            'word_entry_id' ,'name', 'email', 'content'
        ]

    def clean(self):
        
        cleaned_data = super(CommentForm, self).clean()
        name = ''
        email = ''
        try:
            name = cleaned_data['name']
            email = cleaned_data['email']
        except:
            pass
        
        if name != '' or email != '':
            if name == '' or email == '':
                self.add_error('name',_('You have to inform both, email and name, otherwise, leave both blank.'))
                return cleaned_data
        
        if email != '':
            if User.objects.filter(email=email).exists():
                self.instance.author = User.objects.get(email=email)
            else:
                self.instance.author = User(username=email, email=email)

            first_name = name.split(' ')[0].strip()
            last_name = name.replace(first_name, '').strip()

            self.instance.author.first_name = first_name
            self.instance.author.last_name = last_name

        self.instance.word_entry_id = cleaned_data['word_entry_id']

        return cleaned_data
    
    def save(self, commit=True):
        
        if commit:
            if self.instance.author:
                self.instance.author.save()
            self.instance.save()
        