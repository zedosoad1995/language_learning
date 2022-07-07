from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **otherfields):
        if username is None:
            raise TypeError('Users must have an username address.')

        user = self.model(username=username, password=password, email=self.normalize_email(email), **otherfields)
        user.set_password(password)

        print(user)
        user.save()

        return user

    def create_superuser(self, username, email, password, **otherfields):
        otherfields.setdefault('is_superuser', True)
        otherfields.setdefault('is_staff', True)
        otherfields.setdefault('is_active', True)
        if otherfields.get('is_superuser') is not True:
            raise TypeError('Superuser must have an is_superuser=True.')
        if otherfields.get('is_staff') is not True:
            raise TypeError('Superuser must have an is_staff=True.')
        if otherfields.get('is_active') is not True:
            raise TypeError('Superuser must have an is_active=True.')

        user = self.create_user(username, email, password, **otherfields)
        user.is_admin = True
        user.save()

        return user