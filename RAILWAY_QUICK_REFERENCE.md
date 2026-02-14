# Quick Railway Deployment Commands

## Initial Setup
```bash
# 1. Commit all changes
git add .
git commit -m "Add Railway deployment configuration"
git push origin main

# 2. Install Railway CLI
npm i -g @railway/cli

# 3. Login to Railway
railway login

# 4. Link your project (after creating on Railway dashboard)
railway link
```

## Management Commands
```bash
# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser

# Collect static files
railway run python manage.py collectstatic --noinput

# Load initial data
railway run python populate_db.py

# Open Django shell
railway run python manage.py shell

# View logs
railway logs

# Open app in browser
railway open
```

## Environment Variables (Set in Railway Dashboard)

### Essential Variables:
```env
SECRET_KEY=your-secret-key-generate-new-one
DEBUG=False
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
DATABASE_URL=${{Postgres.DATABASE_URL}}
CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://*.up.railway.app
SITE_URL=${{RAILWAY_PUBLIC_DOMAIN}}
```

### Optional (Email):
```env
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

## Common Issues & Solutions

### 1. Static files not loading
```bash
# Check WhiteNoise is in MIDDLEWARE
# Verify STATIC_ROOT is set
railway run python manage.py collectstatic --noinput
```

### 2. Database connection error
```bash
# Verify DATABASE_URL is set
railway variables
# Test connection
railway run python manage.py dbshell
```

### 3. App not starting
```bash
# Check logs
railway logs
# Verify Procfile exists and is correct
cat Procfile
```

### 4. 502 Bad Gateway
```bash
# Ensure app binds to $PORT
# Check gunicorn is installed
# Verify worker count in Procfile
```

## Deployment Checklist

- [ ] All code committed to GitHub
- [ ] Railway project created
- [ ] PostgreSQL database added
- [ ] Environment variables set
- [ ] Domain generated
- [ ] First deployment successful
- [ ] Migrations applied
- [ ] Superuser created
- [ ] Static files serving correctly
- [ ] Site fully functional

## Railway Project Structure

```
Railway Project
├── Django Service (your-app)
│   ├── Environment Variables
│   ├── Deployments
│   ├── Metrics
│   └── Logs
└── PostgreSQL Database
    ├── DATABASE_URL (copy this)
    ├── Metrics
    └── Backups
```

## URLs After Deployment

- **Railway Dashboard**: https://railway.app/project/[your-project-id]
- **Live Site**: https://[your-app].up.railway.app
- **Admin Panel**: https://[your-app].up.railway.app/admin/
- **API Endpoints**: https://[your-app].up.railway.app/events/

## Monitoring

```bash
# Real-time logs
railway logs --follow

# Check service status
railway status

# View environment variables
railway variables

# Check disk usage
railway run df -h

# Check memory usage
railway run free -h
```

## Updating Your Deployment

```bash
# 1. Make changes locally
git add .
git commit -m "Your update message"
git push origin main

# 2. Railway will auto-deploy
# Or manually trigger:
railway up
```

## Backing Up Database

```bash
# Export data
railway run python manage.py dumpdata > backup.json

# Import data (if needed)
railway run python manage.py loaddata backup.json
```

## Rolling Back

```bash
# In Railway Dashboard:
# 1. Go to Deployments tab
# 2. Find previous successful deployment
# 3. Click "Redeploy"
```

## Cost Management (Free Tier)

- Monthly: $5 credit
- Usage: $0.000463/GB-hour
- Database: Included
- Bandwidth: Included

**Tip**: Monitor usage in Railway dashboard to stay within free tier

## Security Reminders

1. ✅ Never commit `.env` to git
2. ✅ Use strong SECRET_KEY (generate new for production)
3. ✅ Set DEBUG=False in production
4. ✅ Restrict ALLOWED_HOSTS to your domains
5. ✅ Keep dependencies updated
6. ✅ Enable HTTPS (Railway does this automatically)

---

**For detailed guide, see [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md)**
