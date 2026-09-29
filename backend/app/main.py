from fastapi import FastAPI
from app.config.settings import settings

app = FastAPI(title=settings.APP_NAME)

@app.get('/health')
def health_check():
    return {
        'message': 'Welcome Back here',
        'status': 'ok',
        'app': settings.APP_NAME,
        'environment': settings.ENVIRONMENT
    }