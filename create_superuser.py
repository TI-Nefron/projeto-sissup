from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='Gabryel').exists():
    User.objects.create_superuser('Gabryel', 'nucleoti@gruponefron.com.br', 'Gabryel123$')
    print("Superuser 'Gabryel' created.")
else:
    print("Superuser 'Gabryel' already exists.")
