from django import forms

class NewChatForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea)

class ChatForm(forms.Form):
    message = forms.CharField(max_length=2000, widget=forms.Textarea)
