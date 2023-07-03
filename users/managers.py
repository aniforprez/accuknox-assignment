from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields = {"is_staff": True, "is_superuser": True, **extra_fields}
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields = {**extra_fields, "is_staff": True, "is_superuser": True}

        user = self.create_user(email=email, password=password, **extra_fields)

        return user
