from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = [
    "127.0.0.1",
]

ADMIN_BASE_URL = env("ADMIN_BASE_URL")
NGO_BASE_URL = env("NGO_BASE_URL")
COLLEGE_BASE_URL = env("COLLEGE_BASE_URL")
PROJECT_BASE_URL = env("PROJECT_BASE_URL")

# Razor pay cred

KEY_ID = env("Key_id")
KEY_SECRET = env("Key_secret")
MERCHANT_ID = env("merchant_id")
RAZOR_PAY_API_KEY = env("razor_pay_api_key")
RAZORPAY_WEBHOOK_SECRET = env("razor_webhook_secret")

ADMINS = (
    (
        "Dev Email",
        env("DEV_ADMIN_EMAIL", default="kalpeshr@hyperlinkinfosystem.net.in"),
    ),
)
MANAGERS = ADMINS

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "db_dev_activityngo",
        "USER": "root",
        "PASSWORD": "",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    }
}

# E-mail settings
# -----------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
# DEFAULT_FROM_EMAIL = SERVER_EMAIL = env('SERVER_EMAIL_SIGNATURE') + ' <%s>' % env('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
BCC_LIST = env.list("BCC_LIST")



# source ./sendgrid.env
SENDGRID_API_KEY = env("SENDGRID_API_KEY")