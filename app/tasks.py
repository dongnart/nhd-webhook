from app.models import WebhookConfig

def process_data(data, type):
    webhooks = WebhookConfig.query.filter_by(type=type).all()
    for webhook in webhooks:
        print(f"Sending data to {webhook.url}: {data}")