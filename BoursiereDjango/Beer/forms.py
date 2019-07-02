from django import forms


class BeerForm(forms.Form):
    beer_name = forms.CharField(label='Beer name', max_length=100, required=True)
    price = forms.IntegerField(required=True)
    stock = forms.IntegerField(required=True)
    coef_up = forms.FloatField(required=True)
    coef_down = forms.FloatField(required=True)
    coef_max = forms.FloatField(required=True)
    image = forms.ImageField(required=True)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, required=True)
    password = forms.CharField(label='Password', max_length=250, required=True, widget=forms.PasswordInput())
