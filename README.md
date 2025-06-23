📬 Доска объявлений

После регистрации пользователь вводит код подтверждения.
Сейчас используется консольный email-бэкенд — код отображается в терминале.
Можно легко подключить SMTP-сервер для реальной отправки писем.

settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'your_email@gmail.com'
EMAIL_HOST_PASSWORD = 'your_app_password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
