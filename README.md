# Платформа онлайн-обучения на Django Rest Framework

## Описание проекта

Проект представляет собой платформу для онлайн-обучения, где пользователи могут создавать и проходить курсы, управлять подписками и осуществлять платежи через Stripe.

## Основные функции

- **Управление пользователями**: Регистрация, аутентификация, профили пользователей
- **Система курсов**: Создание, редактирование и управление курсами
- **Уроки**: Добавление уроков к курсам с видео-материалами
- **Подписки**: Система подписок на обновления курсов
- **Платежная система**: Интеграция с Stripe для оплаты курсов
- **Асинхронные задачи**: Фоновая отправка email-уведомлений через Celery
- **Безопасность**: Система прав доступа (модераторы, владельцы контента)

## Технологический стек

- **Backend**: Django 5.2+, Django REST Framework
- **База данных**: PostgreSQL
- **Веб-сервер**: Nginx + Gunicorn
- **Аутентификация**: JWT (Simple JWT)
- **Платежная система**: Stripe API
- **Асинхронные задачи**: Celery + Redis
- **Контейнеризация**: Docker + Docker Compose
- **CI/CD**: GitHub Actions

## Установка и запуск

### 1. Настройка удаленного сервера  

Подготовка сервера (Ubuntu 22.04)  
  
```bash
# Подключение к серверу
ssh username@your-server-ip

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Docker
sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io

# Установка Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Добавление пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker

# Настройка firewall
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 2. Клонирование репозитория

```bash
git clone https://github.com/ChubshevAB/DRF-Project.git
cd DRF-Project
```

### 3. Настройка переменных окружения
Создайте файл .env в корневой директории:
 
#### Django  
SECRET_KEY=your-secret-key-here  
DEBUG=False  
ALLOWED_HOSTS=your-domain.com,server-ip  

#### Database
POSTGRES_DB=your_db_name  
POSTGRES_USER=your_db_user  
POSTGRES_PASSWORD=your_strong_password  
DB_NAME=your_db_name  
DB_USER=your_db_user  
DB_PASSWORD=your_strong_password  
DB_HOST=db  
DB_PORT=5432  

#### Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_your_key  
STRIPE_SECRET_KEY=sk_test_your_key  

#### Email
EMAIL_HOST=smtp.gmail.com  
EMAIL_PORT=587  
EMAIL_HOST_USER=your_email@gmail.com  
EMAIL_HOST_PASSWORD=your_app_password  
DEFAULT_FROM_EMAIL=your_email@gmail.com  

#### Celery
CELERY_BROKER_URL=redis://redis:6379/0  
CELERY_RESULT_BACKEND=redis://redis:6379/0  

### 4. Запуск проекта с Docker Compose

```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Запуск в фоновом режиме
docker-compose up -d --build

# Остановка проекта
docker-compose down

# Остановка с удалением volumes
docker-compose down -v

# Перезапуск конкретного сервиса
docker-compose restart web
```
