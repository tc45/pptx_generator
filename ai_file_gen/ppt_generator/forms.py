from django import forms
from mdeditor.fields import MDTextFormField


class pptx_markdown(forms.Form):
    #pptx_markdown = MDTextFormField(widget=forms.Textarea)
    pptx_markdown = MDTextFormField(widget=forms.Textarea(attrs={'id': 'markupInput'}))

