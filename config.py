import os
import datetime

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'flex_and_vibe_secret_key')

    # TiDB Cloud connection (MySQL-compatible)
    SQLALCHEMY_DATABASE_URI = (
    'mysql+pymysql://47vaDr39q2MWZRN.root:0mD5HmOy4Ffzze3O@'
    'gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/test'
    '?ssl_ca=E:\\BackendFolderEcomerse\\certs\\isrgrootx1.pem'
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cloudinary
    CLOUDINARY_CLOUD_NAME = 'dr5r2rvkg'
    CLOUDINARY_API_KEY = '177237536613665'
    CLOUDINARY_API_SECRET = 'IgdDmXCBP2tf3aexFEMO-Pbrt64'

    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key"  # change in production
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=7)
