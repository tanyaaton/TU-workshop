# Security Guidelines

## ⚠️ IMPORTANT: Secrets Management

This repository contains workshop materials that require API keys and credentials. **NEVER commit sensitive information to Git.**

## Protected Files

The following files are excluded from version control and contain sensitive data:

### Environment Variables
- `.env` files (all locations)
- `backup/.env`
- Any file matching `*.env` pattern

### Credentials & Keys
- `*credentials.json`
- `*token.json`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `id_rsa*`, `*.ppk`
- Any file containing `apikey` or `api_key`

### Deployment Scripts
- `set_connection_creds.sh`
- `**/deploy_*.sh`
- `**/build_and_push.sh`

### Databases
- `*.db`, `*.sqlite`, `*.sqlite3` (may contain sensitive data)

## Setup Instructions

1. **Copy template files** (when provided):
   ```bash
   cp .env.example .env
   ```

2. **Add your credentials** to the copied files (never to templates)

3. **Verify files are ignored** before committing:
   ```bash
   git status
   git add -n .
   ```

4. **Never commit** if you see sensitive files in the staging area

## What to Do If You Accidentally Commit Secrets

1. **DO NOT** just delete the file and commit again - it's still in Git history
2. **Immediately rotate/revoke** the exposed credentials
3. **Remove from Git history** using:
   ```bash
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch PATH/TO/FILE" \
     --prune-empty --tag-name-filter cat -- --all
   ```
4. **Force push** (if already pushed to remote):
   ```bash
   git push origin --force --all
   ```

## Best Practices

✅ **DO:**
- Use environment variables for all secrets
- Keep `.env` files local only
- Use template files (`.env.example`) for documentation
- Review changes before committing
- Use `git add -n .` to preview what will be staged

❌ **DON'T:**
- Hardcode credentials in source code
- Commit `.env` files
- Share credentials in chat/email
- Use production credentials in development
- Commit database files with real data

## IBM Cloud Specific

For IBM Cloud services:
- Store API keys in `.env` files
- Use IBM Cloud Secrets Manager for production
- Never commit `ibmcloud_api_key*` files
- Rotate keys regularly

## Questions?

If you're unsure whether a file should be committed, ask before pushing!