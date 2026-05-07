# Reaction Rush

Small Django MVP game for reaction training.

## What it does

- Registration and login
- 60-second round with circles that appear faster as time decreases
- Score based on clicked circles
- Leaderboard based on each player's best score
- Update-guard component that verifies a signed update manifest before trusting a release source

## Run locally

```powershell
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## Update guard

The guard service can be started with:

```powershell
python security/guard_server.py
```

It validates `security/update_manifest.json` using `UPDATE_GUARD_SECRET`.