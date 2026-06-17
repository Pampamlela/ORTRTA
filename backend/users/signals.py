from django.dispatch import receiver
from django.core.mail import send_mail
from django_rest_passwordreset.signals import reset_password_token_created

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    reset_url = f"http://localhost:5173/reset-password?token={reset_password_token.key}"

    send_mail(
        subject="Réinisialisation de votre mot de passe - One Roll To Rule Them All",
        message=f"Bonjour {reset_password_token.user.username},\n\nVous avez demandé à réinitialiser votre mot de passe. Veuillez cliquer sur le lien ci-dessous pour le réinitialiser :\n\n{reset_url}\n\nCe lien est valale 24h.\n\nSi vous n'avez pas demandé cette réinitialisation, veuillez ignorer cet email.",
        from_email=None, # utilise DEFAULT_FROM_EMAIL défini dans settings.py
        recipient_list=[reset_password_token.user.email],
    )