from django import forms
from .models import CustomUser, Orders, Items, RequestRows


class UserRegisterForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'role', 'password']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CreateGoodsForm(forms.ModelForm):

    class Meta:
        model = Items
        fields = ['item_group', 'unit_measurement', 'quantity', 'price',
                  'status', 'storage_location', 'contact_person', 'photo']
        labels = {
            'item_group': 'Group',
            'unit_measurement': 'Measurement',
            'quantity': 'Quantity',
            'price': 'Price',
            'status': 'Status',
            'storage_location': 'Storage Address',
            'contact_person': 'Information about supplier',
            'photo': 'Image',
        }
        widgets = {
            'item_group': forms.Select(attrs={'class': 'form-control'}),
            'unit_measurement': forms.Select(attrs={'class': 'form-control'}),
            # 'quantity': forms.IntegerField(attrs={'class': 'form-control'}),
            # 'price': forms.DecimalField(attrs={'class': 'form-control'}),
            # 'status': forms.TextInput(attrs={'class': 'form-control'}),
            # 'storage_location': forms.TextInput(attrs={'class': 'form-control'}),
            # 'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            # 'photo': forms.ImageField(attrs={'class': 'form-control'}),
        }


class GoodsUpdateForms(forms.ModelForm):

    class Meta:
        model = Items
        exclude = ['item_id']
        labels = {
            'item_group': 'Group',
            'unit_measurement': 'Measurement',
            'quantity': 'Quantity',
            'price': 'Price',
            'status': 'Status',
            'storage_location': 'Storage Address',
            'contact_person': 'Information about supplier',
            'photo': 'Image'
        }


class CreateOrderForm(forms.ModelForm):

    class Meta:
        model = Orders
        fields = ['product_name', 'item_id', 'unit_measurement', 'quantity',
                  'price', 'comment']

        labels = {
            'product_name': 'Name',
            'item_id': 'ID of required item',
            'unit_measurement': 'Measurement',
            'quantity': 'Quantity',
            'price': 'Price',
            'comment': 'Comment',
        }

        widgets = {
            'unit_measurement': forms.Select(attrs={'class': 'form-control'}),
        }


class OrdersUpdateForms(forms.ModelForm):

    class Meta:
        model = Orders
        exclude = ['request_id']
        labels = {
            'product_name': 'Name',
            'item_id': 'ID of required item',
            'unit_measurement': 'Measurement',
            'quantity': 'Quantity',
            'price': 'Price',
            'comment': 'Comment',
        }
