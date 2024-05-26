from .base import *  # NOQA

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

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

# ADMINS
ADMINS = env.json("ADMINS")

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
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

# Storage configurations
# --------------------------------------------------------------------------
USE_CLOUDFRONT = env.bool("USE_CLOUDFRONT", default=False)
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = env("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = env("AWS_SECRET_ACCESS_KEY")
AWS_AUTO_CREATE_BUCKET = True
AWS_DEFAULT_ACL = "public-read"
AWS_QUERYSTRING_AUTH = False
AWS_S3_SECURE_URLS = True
AWS_S3_REGION_NAME = "ap-south-1"

if USE_CLOUDFRONT:
    AWS_S3_CUSTOM_DOMAIN = env("AWS_S3_CUSTOM_DOMAIN")
else:
    AWS_S3_CUSTOM_DOMAIN = "{}.s3.amazonaws.com".format(AWS_STORAGE_BUCKET_NAME)

# STATIC_URL = '//{}/static/'.format(AWS_S3_CUSTOM_DOMAIN)
MEDIA_URL = "//{}/media/".format(AWS_S3_CUSTOM_DOMAIN)
# 'https://{0}/media/'.format(AWS_S3_CUSTOM_DOMAIN)

DEFAULT_FILE_STORAGE = "config.settings.s3utils.MediaRootS3BotoStorage"
# STATICFILES_STORAGE = 'config.settings.s3utils.StaticRootS3BotoStorage'

AWS_PRELOAD_METADATA = False

# source ./sendgrid.env
SENDGRID_API_KEY = env("SENDGRID_API_KEY")
