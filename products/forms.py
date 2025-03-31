from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(required=False, label=False)


class PriceFilterForm(forms.Form):
    min_price = forms.IntegerField(required=False, label='От')
    max_price = forms.IntegerField(required=False, label='До')
    in_stock = forms.BooleanField(required=False, label='В наличии', widget=forms.CheckboxInput())
