
# Run linting on site settings:
echo Testing TWCoulsdon
pylint TWCoulsdon.settings TWCoulsdon.urls

# Run linting on core app:
echo Testing core app
pylint core.debug core.models core.views

# Run linting on home app:
echo Testing home app
pylint home.admin home.models home.urls home.views

# Run linting on events app:
echo Testing events app
pylint events.admin events.forms events.models events.queries events.urls events.views

# Run linting on profiles app:
echo Testing profiles app
pylint profiles.forms profiles.models profiles.urls profiles.views

# Run linting on boxoffice app:
echo Testing boxoffice app
pylint boxoffice.admin boxoffice.basket boxoffice.context boxoffice.forms \
       boxoffice.models boxoffice.payments boxoffice.queries boxoffice.reports \
       boxoffice.signals boxoffice.tickets boxoffice.urls boxoffice.views \
       boxoffice.webhook_handler boxoffice.webhooks
