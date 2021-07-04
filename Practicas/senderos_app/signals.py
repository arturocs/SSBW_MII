from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
import logging
logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info('Usuario ' + user.username + ' ha iniciado sesion')
    print('user {} logged in through page {}'.format(user.username, request.META.get('HTTP_REFERER')))


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    logger.info('Inicio de sesion fallido: ' + credentials.get('username'))
    print('user {} logged in failed through page {}'.format(credentials.get('username'), request.META.get('HTTP_REFERER')))


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info('Usuario ' + user.username + ' ha cerrado sesion')
    print('user {} logged out through page {}'.format(user.username, request.META.get('HTTP_REFERER')))