from modules.origin_api import OriginAPI
from config.settings import settings

origin_api = OriginAPI(settings.origin_email, settings.origin_pass)
