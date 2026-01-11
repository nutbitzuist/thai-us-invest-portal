# Deployment & Project Details

## Vercel (Frontend)
- **Project Name**: `thai-us-invest-frontend`
- **Project ID**: `prj_JXxWSSxOvUPObJnwqKj345IohuMn`
- **Website URL**: [https://thai-us-invest-frontend.vercel.app/](https://thai-us-invest-frontend.vercel.app/)
- **Deployment Method**: Git Push to `main` branch.
- **Root Directory Fix**: The project uses a root `package.json` to proxy build commands to `frontend/` and move artifacts to root.

### CLI Commands
```bash
# Login
vercel login

# Link to project
vercel link --project prj_JXxWSSxOvUPObJnwqKj345IohuMn

# Deploy manually (if needed)
vercel deploy --prod
```

## Railway (Backend)
- **Project Name**: `thai-us-invest-portal`
- **Project ID**: `6779cf68-2851-4b42-9453-7b62f762f64b`
- **Service Name**: `thai-us-invest-portal`
- **Production URL**: `https://thai-us-invest-portal-production.up.railway.app`
- **Deployment Method**: Git Push to `main` branch (Monorepo root).

### CLI Commands
```bash
# Login
railway login

# Link to project
railway link -p 6779cf68-2851-4b42-9453-7b62f762f64b

# Run commands locally with production variables
railway run --service thai-us-invest-portal python3 -m scripts.seed_analysis

# Check logs
railway logs
```

## Seed Analysis Data
To re-populate or update the AI stock analysis in the database, use the admin endpoint:

```bash
curl -X POST https://thai-us-invest-portal-production.up.railway.app/api/seed_analysis \
  -H "X-Admin-Key: dev-secret-key"
```
