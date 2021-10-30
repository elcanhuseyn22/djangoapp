from django import forms

#https://docs.djangoproject.com/en/3.2/ref/forms/

class LoginForm(forms.Form):
    username = forms.CharField(label='İstifadəçi adı')
    password = forms.CharField(max_length=32,label = 'Şifrə',widget = forms.PasswordInput)


class RegisterForm(forms.Form):
    #----------
    name = forms.CharField(max_length=32,label='Ad')
    surname = forms.CharField(max_length=32,label='Soyad')
    email = forms.EmailField(label = "Email")
    #----------
    username = forms.CharField(max_length=32,label='İstifadəçi adı') 
    password = forms.CharField(min_length = 8,max_length=32,label = 'Şifrə',widget = forms.PasswordInput)
    confirm = forms.CharField(min_length = 8,max_length=32,label = 'Şifrəni təsdiq edin',widget = forms.PasswordInput)

    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        confirm = self.cleaned_data.get('confirm')

        if password and confirm and password !=confirm:
            raise forms.ValidationError("Şifrələr üsd-üsdə düşmür!")
        
        values = {
            "username":username,
            "password":password
        }
        return values

