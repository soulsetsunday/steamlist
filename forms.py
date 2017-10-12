from django import forms

class SteamForm(forms.Form):
    form_steam_id = forms.CharField(label='Your Steam ID:', max_length=17)
