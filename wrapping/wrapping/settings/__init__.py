from .base import *
from decouple import config

# you need to set "myproject = 'prod'" as an environment variable
# in your OS (on which your website is hosted)
if config('MODE', 'production') == 'production':
   from .production import *
else:
   from .development import *
