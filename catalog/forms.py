from django import forms
from catalog.models import Product,Version

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name','category','price','description','photo',)

    def clean_name(self):
        cleaned_data = self.cleaned_data.get('name')
        forbidden_words = ["казино","криптовалюта","крипта","радар","биржа","дешево","бесплатно","обман","полиция"]
        if cleaned_data.lower() in forbidden_words:
            raise forms.ValidationError('Вы использовали неуместное слово в названии продукта')
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'