# 🎉 Event Management System - "Eventia"

A comprehensive full-stack event management web application built with Django, PostgreSQL, and Tailwind CSS. Features include user authentication, role-based access control, event creation, RSVP management, and a modern responsive design.

## 🌐 Live Demo

🔗 **[View Live Application](https://event-management-website-1-0g6e.onrender.com/)**

---

## ✨ Key Features

### 👥 User Management
- **User Registration & Authentication**: Secure signup/login with email verification
- **Role-Based Access Control**: Three user roles with different permissions
  - **Admin**: Full system control and user management
  - **Organizer**: Create and manage events
  - **Participant**: Browse events and RSVP
- **User Dashboard**: Personalized dashboard for each user role

### 📅 Event Management
- **Create Events**: Organizers can create events with details (name, description, date, time, location, category, image)
- **Event Categories**: Organize events by categories (Conference, Workshop, Seminar, etc.)
- **Event Listing**: Browse all events with search and filter options
- **Event Details**: View comprehensive event information with RSVP options
- **CRUD Operations**: Full Create, Read, Update, Delete functionality for events

### 📝 RSVP System
- **Event Registration**: Users can RSVP to events
- **My RSVPs**: Track all registered events in user dashboard
- **RSVP Management**: View and manage event participants

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-first design using Tailwind CSS
- **Animated Homepage**: Modern landing page with gradient effects and smooth animations
- **Interactive Navbar**: Role-based navigation with dropdown menus
- **Clean Interface**: Professional and intuitive user interface

### 🔍 Advanced Features
- **Search Functionality**: Search events by name, description, or location
- **Filter by Category**: Browse events by specific categories
- **Query Optimization**: Optimized database queries using `select_related()` and `prefetch_related()`
- **Image Upload**: Event image management with Pillow
- **Debug Toolbar**: Development debugging and performance monitoring

---

## 🛠️ Tech Stack

### Backend
- **Django 6.0.1** - Python web framework
- **PostgreSQL** - Production database
- **SQLite** - Development database (optional)
- **psycopg2-binary 2.9.11** - PostgreSQL adapter
- **dj-database-url** - Database URL configuration
- **python-decouple** - Environment variable management

### Frontend
- **Tailwind CSS 3.4.16** - Utility-first CSS framework
- **Alpine.js** - Lightweight JavaScript framework (for dropdowns)
- **HTML5 & CSS3** - Modern web standards

### Deployment
- **Gunicorn 21.2.0** - WSGI HTTP server
- **WhiteNoise 6.6.0** - Static file serving
- **Render** - Cloud hosting platform

### Development Tools
- **Django Debug Toolbar** - Development debugging
- **Faker** - Test data generation
- **Pillow** - Image processing

---

## 📋 Prerequisites

- Python 3.10 or higher
- PostgreSQL 13 or higher (for production)
- Node.js 14+ and npm (for Tailwind CSS)
- Git

---

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/ripro805/Event-Management-Website.git
cd Event-Management-Website
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Node Dependencies (Tailwind CSS)
```bash
npm install
```

### 5. Configure Environment Variables
Create a `.env` file in the project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Settings (PostgreSQL)
DB_NAME=event_management
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com

# Site Configuration
SITE_URL=http://127.0.0.1:8000
ALLOWED_HOSTS=*
```

### 6. Setup Database
```bash
# Create PostgreSQL database
createdb event_management

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# (Optional) Load sample data
python populate_db.py
```

### 7. Build Tailwind CSS
```bash
# Development (watch mode)
npm run watch:tailwind

# Production build
npm run build:tailwind
```

### 8. Collect Static Files (Production)
```bash
python manage.py collectstatic --no-input
```

### 9. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

## 📁 Project Structure

```
event_management/
├── event_management/        # Project settings
│   ├── settings.py         # Django configuration
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI configuration
│
├── events/                 # Main events app
│   ├── models.py           # Event, Category, RSVP models
│   ├── views.py            # Event views
│   ├── urls.py             # Event URLs
│   ├── admin.py            # Admin configuration
│   ├── signals.py          # Django signals
│   └── templates/          # Event templates
│       └── events/
│           ├── home.html           # Landing page
│           ├── event_list.html     # Events listing
│           ├── event_detail.html   # Event details
│           ├── category_list.html  # Categories
│           └── ...
│
├── user_panel/             # User management app
│   ├── views.py            # Authentication views
│   ├── forms.py            # User forms
│   └── templates/
│       └── user_panel/
│           ├── signup.html         # Registration
│           ├── login.html          # Login
│           ├── dashboard.html      # User dashboard
│           └── my_rsvps.html       # User RSVPs
│
├── organizer/              # Organizer functionality
│   ├── views.py            # Organizer views
│   ├── forms.py            # Event/Category forms
│   └── templates/
│       └── organizer/
│           ├── dashboard.html      # Organizer dashboard
│           ├── event_list.html     # Manage events
│           ├── event_form.html     # Create/Edit event
│           └── ...
│
├── admin_panel/            # Admin functionality
│   ├── views.py            # Admin views
│   └── templates/
│       └── admin_panel/
│           ├── dashboard.html      # Admin dashboard
│           └── user_list.html      # User management
│
├── static/                 # Static files
│   ├── css/
│   │   ├── tailwind.css    # Tailwind input
│   │   ├── output.css      # Compiled CSS
│   │   └── style.css       # Custom styles
│   ├── images/             # Static images
│   │   ├── banner/         # Homepage banners
│   │   └── events/         # Event images
│   └── js/                 # JavaScript files
│
├── media/                  # User uploaded files
│   └── events/             # Event images
│
├── templates/              # Global templates
│   ├── base.html           # Base template
│   └── nopermission.html   # Permission denied
│
├── build.sh                # Render build script
├── manage.py               # Django management
├── populate_db.py          # Sample data generator
├── requirements.txt        # Python dependencies
├── package.json            # Node dependencies
├── tailwind.config.js      # Tailwind configuration
└── .env                    # Environment variables (not in Git)
```

---

## 👤 User Roles & Permissions

### Admin
- View admin dashboard with system statistics
- Manage all users (view, edit, delete)
- Assign roles to users
- Access Django admin panel
- Full CRUD operations on all resources

### Organizer
- Create, edit, and delete own events
- Manage event categories
- View event participants and RSVPs
- Access organizer dashboard
- Cannot modify other organizers' events

### Participant
- Browse all events
- RSVP to events
- View own RSVPs
- Access user dashboard
- Cannot create or modify events

---

## 🎨 Key Pages

### Public Pages
- **Home** (`/`) - Landing page with featured banners and role descriptions
- **Event List** (`/events/`) - Browse all events with search and filters
- **Event Detail** (`/events/<id>/`) - View event details and RSVP
- **Categories** (`/categories/`) - Browse event categories

### Authentication
- **Sign Up** (`/user/signup/`) - New user registration
- **Login** (`/user/login/`) - User authentication
- **Logout** (`/user/logout/`) - End session

### User Dashboards
- **User Dashboard** (`/user/dashboard/`) - Participant dashboard
- **My RSVPs** (`/user/my-rsvps/`) - View registered events
- **Organizer Dashboard** (`/organizer/dashboard/`) - Event management
- **Admin Dashboard** (`/admin-panel/dashboard/`) - System administration

---

## 🗄️ Database Models

### Event
- name, description, date, time, location
- category (ForeignKey to Category)
- image (ImageField)
- rsvps (ManyToMany with User through RSVP)

### Category
- name, description

### RSVP
- user (ForeignKey to User)
- event (ForeignKey to Event)
- responded_at (DateTime)

### Participant (Legacy)
- name, email, phone
- events (ManyToMany with Event)

---

## 🚀 Deployment (Render)

### Prerequisites
1. Render account
2. PostgreSQL database on Render
3. GitHub repository connected

### Environment Variables (Render)
```env
SECRET_KEY=production-secret-key
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=postgresql://user:pass@host:5432/db
CSRF_TRUSTED_ORIGINS=https://your-app.onrender.com

# Email settings
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### Build Command
```bash
./build.sh
```

### Start Command
```bash
gunicorn event_management.wsgi:application
```

---

## 🔧 Development Commands

```bash
# Run development server
python manage.py runserver

# Watch Tailwind CSS changes
npm run watch:tailwind

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Generate sample data
python populate_db.py

# Collect static files
python manage.py collectstatic

# Run Django shell
python manage.py shell

# Run tests
python manage.py test
```

---

## 🐛 Common Issues & Solutions

### Static files not loading
```bash
python manage.py collectstatic --no-input
```

### Database connection error
- Check PostgreSQL is running
- Verify database credentials in `.env`
- Ensure database exists

### Tailwind CSS not updating
```bash
npm run build:tailwind
```

### Permission denied errors
- Check user roles and groups
- Verify login decorators on views

---

## 📝 API Endpoints

### Events
- `GET /events/` - List all events
- `GET /events/<id>/` - Event detail
- `POST /events/<id>/rsvp/` - RSVP to event

### Categories
- `GET /categories/` - List all categories
- `GET /categories/<id>/` - Category detail with events

### User
- `GET /user/dashboard/` - User dashboard
- `GET /user/my-rsvps/` - User's RSVPs

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available for educational purposes.

---

## 👨‍💻 Author

**Rifat Rizvi**

- GitHub: [@ripro805](https://github.com/ripro805)
- Email: rifatrizviofficial001@gmail.com

---

## 🙏 Acknowledgments

- **Phitron** - Software Development Track
- **Django Documentation** - Comprehensive framework guide
- **Tailwind CSS** - Modern CSS framework
- **Render** - Deployment platform

---

## 📸 Screenshots

### Homepage
Modern landing page with animated banners and role descriptions

### Event Listing
Browse and search events with category filters

### Event Details
View event information and RSVP

### User Dashboard
Role-based dashboards for Admin, Organizer, and Participant

---

## 🔮 Future Enhancements

- [ ] Event calendar view
- [ ] Email notifications for RSVPs
- [ ] Event capacity limits
- [ ] Payment integration
- [ ] Social media sharing
- [ ] Event reviews and ratings
- [ ] Advanced analytics dashboard
- [ ] Multi-language support

---

**Built with ❤️ using Django, PostgreSQL, and Tailwind CSS**
