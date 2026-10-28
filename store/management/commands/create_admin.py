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
        email = options["email"].strip().lower()
        name = options["name"].strip()
        phone = options["phone"].strip()

        if Users.objects.filter(email__iexact=email).exists():
            raise CommandError(f"A user with email {email} already exists.")
        if Users.objects.filter(phone_number=phone).exists():
            raise CommandError(f"A user with phone {phone} already exists.")

        password = generate_password()

        Users.objects.create(
            full_name=name,
            email=email,
            phone_number=phone,
            password=make_password(password),  # hashed, never stored as plain text
            date_joined=timezone.now(),
            is_active=True,
            role=Users.ROLE_ADMIN,
            must_change_password=True,
        )

        self.stdout.write(self.style.SUCCESS("Admin account created."))
        self.stdout.write(f"  Email:    {email}")
        self.stdout.write(f"  Password: {password}")
        self.stdout.write(self.style.WARNING(
            "This password is shown ONCE. Hand it over via a password manager, "
            "not chat or email. It must be changed at first login."
        ))