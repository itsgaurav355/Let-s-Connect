# Let's Connect - Social Media Platform

![Social Media Platform](static/images/myimg.jpg)

A full-featured social media platform with real-time messaging, post interactions, and user connections.

## Features

### User Authentication
- Secure signup/login with credential validation
- Profile management with image upload
- Password protected sessions

### Core Features
- Create and share image posts with captions
- Like/unlike posts with real-time counters
- Follow/unfollow other users
- Search for users by username
- View user profiles with follower statistics
- Suggested users to follow

### Real-time Chat
- WebSocket-based messaging
- Typing indicators
- Message read receipts
- Chat history persistence

### Additional Features
- Responsive UI with Tailwind CSS
- File upload handling (images)
- Activity feed with followed users' posts
- User review system

## Installation

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Setup
```bash
git clone https://github.com/itsgaurav355/Let-s-Connect.git
cd Let-s-Connect
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate

pip install django pillow channels
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Project Structure
```
project/
├── core/                 # Main application
│   ├── models.py         # Database models
│   ├── views.py          # Business logic
│   ├── urls.py           # App routes
│   └── admin.py          # Admin configurations
├── project/              # Project settings
│   ├── settings.py       # Project configuration
│   ├── urls.py           # Main routes
│   └── wsgi.py           # WSGI config
├── templates/            # HTML templates
├── static/               # Static assets
│   └── assets/           # CSS, JS, images
├── media/                # User-uploaded files
└── manage.py             # Django CLI
```

## Configuration
- **Database**: SQLite (default), can be changed in `settings.py`
- **Static/Media Files**: Configured in `settings.py`
- **Authentication**: Session-based with Django's built-in system
- **Real-time Features**: Using Django Channels (WebSockets)

## Running the Server
```bash
# Development mode
python manage.py runserver

# Production setup (example)
# Configure ALLOWED_HOSTS in settings.py
# Set DEBUG=False
# Add proper database configuration
```

## Contributing
1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

