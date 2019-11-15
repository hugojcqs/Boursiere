from django import forms


class BeerForm(forms.Form):
    beer_name = forms.CharField(label='Beer name', max_length=100, required=True)
    price = forms.FloatField(required=True)
    stock = forms.IntegerField(required=True)
    coef_up = forms.FloatField(required=True)
    coef_down = forms.FloatField(required=True)
    coef_max = forms.FloatField(required=True)
    coef_min = forms.FloatField(required=True)
    alcohol_percentage = forms.FloatField(label='% d\'alccol', required=True)
    bar = forms.IntegerField(label='Bar (1,2,3)', required=True)

    def __init__(self, *args, **kwargs):                        # set min value
        super(BeerForm, self).__init__(*args, **kwargs)
        self.fields['price'].widget.attrs['min'] = 0
        self.fields['stock'].widget.attrs['min'] = 0
        self.fields['coef_up'].widget.attrs['min'] = 0
        self.fields['coef_down'].widget.attrs['min'] = 0
        self.fields['coef_max'].widget.attrs['min'] = 0
        self.fields['coef_min'].widget.attrs['min'] = 0
        self.fields['bar'].widget.attrs['min'] = 1
        self.fields['alcohol_percentage'].widget.attrs['min'] = 0
        self.fields['bar'].widget.attrs['max'] = 3
