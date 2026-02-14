# 🚀 Event Management System - Railway Deployment Guide

## 📋 সম্পূর্ণ Deployment প্রক্রিয়া (Step by Step)

এই গাইড অনুসরণ করে আপনি **Railway Platform** এ সম্পূর্ণ প্রজেক্ট deploy করতে পারবেন।

---

## ✅ পূর্ব প্রস্তুতি (Prerequisites)

### 1. **প্রয়োজনীয় Account তৈরি করুন**
- ✅ [Railway Account](https://railway.app/) - Sign up with GitHub
- ✅ [GitHub Account](https://github.com/) - আপনার কোড এখানে থাকবে

### 2. **Project ফাইলসমূহ যাচাই করুন**
নিম্নলিখিত ফাইলগুলো আপনার প্রজেক্টে আছে কিনা নিশ্চিত করুন:

- ✅ `Procfile` - Railway এর জন্য start command
- ✅ `runtime.txt` - Python version
- ✅ `railway.toml` - Railway configuration
- ✅ `nixpacks.toml` - Build configuration
- ✅ `requirements.txt` - Python dependencies (gunicorn, whitenoise সহ)
- ✅ `.env.example` - Environment variables এর example

---

## 🔧 Step 1: Local Configuration

### 1.1 Environment Variables Setup

`.env` ফাইলে নিচের variables গুলো add করুন:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-this-in-production
DEBUG=False
ALLOWED_HOSTS=*

# Database (Railway PostgreSQL থেকে পাবেন)
DATABASE_URL=postgresql://user:password@host:port/database

# Site Settings
SITE_URL=https://your-app.up.railway.app

# Email Configuration (Optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

### 1.2 Static Files Test

Local এ static files collect করে test করুন:

```bash
python manage.py collectstatic --noinput
```

---

## 🌐 Step 2: GitHub Repository Setup

### 2.1 Code Push করুন

```bash
# Check current status
git status

# Add all changes
git add .

# Commit changes
git commit -m "Add Railway deployment configuration"

# Push to GitHub
git push origin main
```

### 2.2 Repository Public/Private সেট করুন
- আপনার GitHub repository settings এ যান
- Public বা Private সেট করুন (Railway উভয়ের সাথে কাজ করে)

---

## 🚂 Step 3: Railway Deployment

### 3.1 নতুন Project তৈরি

1. **Railway Dashboard এ যান**: https://railway.app/dashboard
2. **"New Project" ক্লিক করুন**
3. **"Deploy from GitHub repo" সিলেক্ট করুন**
4. আপনার repository সিলেক্ট করুন: `Event-Management-Website`

### 3.2 PostgreSQL Database Add করুন

1. Railway project ড্যাশবোর্ডে **"+ New"** ক্লিক করুন
2. **"Database" → "PostgreSQL"** সিলেক্ট করুন
3. Database automatically provision হবে

### 3.3 Environment Variables সেট করুন

Railway dashboard এ আপনার service এ ক্লিক করুন → **"Variables"** ট্যাবে যান:

#### Required Variables:

```env
SECRET_KEY=django-insecure-your-very-long-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
CSRF_TRUSTED_ORIGINS=https://*.railway.app,https://*.up.railway.app

# Database - Railway PostgreSQL থেকে copy করুন
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Site Settings
SITE_URL=${{RAILWAY_PUBLIC_DOMAIN}}
PORT=8000

# Email (Optional - আপনার Gmail credentials)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com
```

#### 🔗 Database URL Link করার উপায়:

1. PostgreSQL service এ ক্লিক করুন
2. **"Variables"** ট্যাবে `DATABASE_URL` কপি করুন
3. Django service এ গিয়ে `DATABASE_URL` variable এ paste করুন
4. অথবা Reference variable ব্যবহার করুন: `${{Postgres.DATABASE_URL}}`

### 3.4 Domain Setup

1. **"Settings"** ট্যাবে যান
2. **"Networking" section এ "Generate Domain"** ক্লিক করুন
3. আপনার app এর domain তৈরি হবে (e.g., `your-app.up.railway.app`)
4. এই domain টি `ALLOWED_HOSTS` এ যোগ করুন

---

## 🎯 Step 4: Deployment Verification

### 4.1 Build Logs চেক করুন

1. Railway ড্যাশবোর্ডে **"Deployments"** ট্যাবে যান
2. Latest deployment এর logs দেখুন
3. নিচের messages দেখতে হবে:
   ```
   ✓ Installing dependencies
   ✓ Running collectstatic
   ✓ Starting gunicorn
   ```

### 4.2 Database Migration

Railway automatically migrations run করবে (Procfile এ আছে)। Manual run করতে চাইলে:

1. Service এ ক্লিক → **"Settings"** → **"Deploy"**
2. Deployment trigger করুন

অথবা Railway CLI দিয়ে:

```bash
railway run python manage.py migrate
```

### 4.3 Superuser তৈরি করুন

Railway CLI install করে superuser তৈরি করুন:

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Link your project
railway link

# Create superuser
railway run python manage.py createsuperuser
```

অথবা Railway Shell ব্যবহার করুন:
1. Service → **"Settings"** → **"One-Click Shell"**
2. Shell open হলে: `python manage.py createsuperuser`

---

## 🧪 Step 5: Testing Your Deployment

### 5.1 আপনার Live Site Test করুন

আপনার Railway domain খুলুন (e.g., `https://your-app.up.railway.app`):

- ✅ Home page লোড হচ্ছে কিনা
- ✅ CSS/JS files সঠিকভাবে লোড হচ্ছে কিনা
- ✅ Login/Signup কাজ করছে কিনা
- ✅ Image upload কাজ করছে কিনা
- ✅ Admin panel access করা যাচ্ছে কিনা (`/admin/`)

### 5.2 Static Files যদি লোড না হয়

Railway logs চেক করুন:

```bash
railway logs
```

Problem থাকলে:
1. `STATIC_ROOT` ঠিক আছে কিনা চেক করুন
2. `WhiteNoise` middleware সঠিকভাবে configured আছে কিনা
3. `collectstatic` সফলভাবে run হয়েছে কিনা

---

## 📊 Step 6: Post-Deployment Setup

### 6.1 Initial Data Load (Optional)

আপনার local database থেকে data load করতে চাইলে:

```bash
# Local থেকে data dump করুন
python manage.py dumpdata > data.json

# Railway এ load করুন
railway run python manage.py loaddata data.json
```

### 6.2 Populate Sample Data

```bash
railway run python populate_db.py
```

### 6.3 Custom Domain Setup (Optional)

Railway paid plan এ custom domain add করতে পারেন:
1. **Settings → Networking → Custom Domain**
2. আপনার domain provider এ CNAME record add করুন
3. মোটামুটি 5-10 মিনিট পর activate হবে

---

## 🔍 Troubleshooting Guide

### Problem 1: Application Crashed
**Solution:**
```bash
railway logs
```
Logs দেখে error identify করুন। সাধারণ কারণ:
- Missing environment variables
- Database connection failed
- Import errors

### Problem 2: Static Files Not Loading
**Solution:**
1. Check `STATIC_ROOT` in settings
2. Verify WhiteNoise in `MIDDLEWARE`
3. Run `collectstatic` again

### Problem 3: Database Connection Error
**Solution:**
1. Verify `DATABASE_URL` is set correctly
2. Check PostgreSQL service is running
3. Test connection: `railway run python manage.py dbshell`

### Problem 4: 502 Bad Gateway
**Solution:**
1. Check if app is listening on correct PORT
2. Verify `Procfile` has correct command
3. Check memory/CPU limits in Railway dashboard

---

## 🛠️ Railway CLI Commands (Useful)

```bash
# Install CLI
npm i -g @railway/cli

# Login
railway login

# Link project
railway link

# View logs
railway logs

# Run commands
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py shell

# Open in browser
railway open

# Environment variables
railway variables
```

---

## 📈 Monitoring & Maintenance

### Railway Dashboard Features:

1. **Metrics Tab**: CPU, Memory, Network usage দেখুন
2. **Deployments Tab**: Deployment history
3. **Logs Tab**: Real-time logs
4. **Variables Tab**: Environment variables manage
5. **Settings Tab**: Service configuration

### Regular Maintenance:

- **Weekly**: Logs check করুন error আছে কিনা
- **Monthly**: Database backup নিন
- **As Needed**: Dependencies update করুন

---

## 💰 Railway Pricing

### Free Tier:
- ✅ $5 credit/month
- ✅ 500 hours runtime
- ✅ PostgreSQL database included
- ✅ Custom domains (paid plans)

### Hobby Plan ($5/month):
- ✅ $5 credit + usage-based billing
- ✅ Unlimited projects
- ✅ Priority support

**Note**: Free tier এ ছোট projects easily চালানো যায়।

---

## 🔐 Security Best Practices

### Production Checklist:

- ✅ `DEBUG=False` set করুন
- ✅ Strong `SECRET_KEY` ব্যবহার করুন
- ✅ `ALLOWED_HOSTS` শুধু আপনার domains এ restrict করুন
- ✅ `CSRF_TRUSTED_ORIGINS` properly set করুন
- ✅ Database credentials secure রাখুন
- ✅ Email credentials environment variables এ রাখুন
- ✅ Never commit `.env` file to git

---

## 📚 Additional Resources

- **Railway Documentation**: https://docs.railway.app/
- **Django Deployment Checklist**: https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/
- **WhiteNoise Documentation**: http://whitenoise.evans.io/
- **PostgreSQL on Railway**: https://docs.railway.app/databases/postgresql

---

## ✨ Success Checklist

Deploy করার পর নিচের সবগুলো check করুন:

- [ ] ✅ Site পুরোপুরি লোড হচ্ছে
- [ ] ✅ Static files (CSS/JS) কাজ করছে
- [ ] ✅ Images display হচ্ছে
- [ ] ✅ User registration/login working
- [ ] ✅ Admin panel accessible
- [ ] ✅ Events creation working
- [ ] ✅ RSVP system functioning
- [ ] ✅ Email notifications sending (if configured)
- [ ] ✅ Database queries successful
- [ ] ✅ Forms submission working

---

## 🎉 Congratulations!

আপনার **Event Management System** এখন successfully deploy হয়েছে এবং live! 🚀

### Next Steps:
1. আপনার live URL বন্ধুদের সাথে share করুন
2. README.md তে live demo link যোগ করুন
3. GitHub repository তে deployment badge add করুন
4. Regular monitoring setup করুন

---

## 📞 Need Help?

কোন সমস্যা হলে:
1. Railway Community Discord: https://discord.gg/railway
2. GitHub Issues: Create issue in your repository
3. Railway Documentation: https://docs.railway.app/

**Happy Deploying! 🎊**
