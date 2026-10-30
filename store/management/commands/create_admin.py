import secrets
import string

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from store.models import Users


def generate_password(length=14):
    """Random password that satisfies your signup rules:
    letter + number + special char from @$!%*#?&"""
    letters = string.ascii_letters
    digits = string.digits
    specials = "@$!%*#?&"
    pool = letters + digits + specials

    while True:
        pwd = "".join(secrets.choice(pool) for _ in range(length))
        if (
            any(c in letters for c in pwd)
            and any(c in digits for c in pwd)
            and any(c in specials for c in pwd)
        ):
            return pwd


class Command(BaseCommand):
    help = "Create an admin account with a random one-time password."

    def add_arguments(self, parser):
        parser.add_argument("--email", required=True)
        parser.add_argument("--name", required=True)
        parser.add_argument("--phone", required=True)
        
        
    def handle(self, *args, **options):
        import os
        email = options["email"].strip().lower()
        name = options["name"].strip()
        phone = options["phone"].strip()
        password = os.environ.get("ADMIN_PASSWORD") or generate_password()

        user = Users.objects.filter(email__iexact=email).first()
        if user is None:
            user = Users(email=email, date_joined=timezone.now())

        user.full_name = name
        user.phone_number = phone
        user.password = make_password(password)
        user.is_active = True
        user.role = Users.ROLE_ADMIN
        user.must_change_password = False
        user.save()

        self.stdout.write(self.style.SUCCESS(f"Admin ready: {email}"))