# Jenkins Environment Setup Guide for borcelle_crm

## Upgrade Summary (Completed)
✅ **Django upgraded:** 3.2.13 → 4.2.28  
✅ **Storage settings:** Converted to Django 4.2+ STORAGES dict  
✅ **Dependencies:** Updated asgiref, certifi, django-storages  

## Jenkins Credential Setup

### Step 1: Create `.env` File

Create a file with all required environment variables:

```bash
# Project Configuration
ENV_PROJECT_NAME=borcelle_crm
DEBUG=0
SECRET_KEY=your-secret-key-here
DOMAIN=borcelle.arpansahu.space
PROTOCOL=https://

# Docker Registry
DOCKER_REGISTRY=harbor.arpansahu.space
DOCKER_REPOSITORY=library
DOCKER_IMAGE_NAME=borcelle_crm
DOCKER_PORT=8001

# Database
DATABASE_URL=postgresql://user:password@postgres.arpansahu.space:9551/borcelle_crm

# Redis
REDIS_CLOUD_URL=rediss://:Gandu302redis@redis.arpansahu.space:9551/ssl_cert_reqs=none

# RabbitMQ (for Celery Results)
RABBIT_MQ_URL=amqps://admin:Gandu302@rabbitmq@rabbitmq.arpansahu.space:9556/%2F

# MinIO/S3 Storage
BUCKET_TYPE=MINIO
AWS_ACCESS_KEY_ID=arpansahu
AWS_SECRET_ACCESS_KEY=Gandu302@minio
AWS_STORAGE_BUCKET_NAME=arpansahu-one-bucket
AWS_S3_REGION_NAME=us-east-1
AWS_S3_ENDPOINT_URL=https://minioapi.arpansahu.space
AWS_S3_CUSTOM_DOMAIN=minioapi.arpansahu.space/arpansahu-one-bucket

# Email (Mailjet)
MAIL_JET_API_KEY=your-api-key
MAIL_JET_API_SECRET=your-api-secret
MAIL_JET_EMAIL_ADDRESS=noreply@arpansahu.space
MY_EMAIL_ADDRESS=your@email.com

# Sentry
SENTRY_ENVIRONMENT=production
SENTRY_DSH_URL=your-sentry-dsn
SENTRY_ORG=arpansahu
SENTRY_PROJECT=borcelle_crm
SENTRY_AUTH_TOKEN=your-sentry-token

# Jenkins
JENKINS_DOMAIN=jenkins.arpansahu.space

# Flower (Celery Monitoring)
FLOWER_ADMIN_USERNAME=admin
FLOWER_ADMIN_PASS=showmecode

# Server
SERVER_NAME=borcelle.arpansahu.space

# Harbor
HARBOR_URL=https://harbor.arpansahu.space
HARBOR_USERNAME=admin
HARBOR_PASSWORD=Gandu302@harbor
```

### Step 2: Upload to Jenkins

1. **Navigate to Jenkins:**
   ```
   https://jenkins.arpansahu.space
   Username: arpansahu
   Password: Gandu302@jenkins
   ```

2. **Go to Credentials:**
   - Dashboard → Manage Jenkins → Credentials
   - System → Global credentials → Add Credentials

3. **Create New Credential:**
   - **Kind:** Secret file
   - **File:** Upload your `.env` file
   - **ID:** `borcelle_crm_env_file` (MUST match Jenkinsfile)
   - **Description:** Environment variables for borcelle_crm
   - Click "Create"

### Step 3: Create Jenkins Pipeline

1. **Create New Pipeline:**
   - Dashboard → New Item
   - Name: `borcelle-crm` (or `borcelle-crm-build`)
   - Type: Pipeline
   - Click OK

2. **Configure Pipeline:**
   - **Description:** Build pipeline for borcelle_crm
   - **Pipeline Definition:** Pipeline script from SCM
   - **SCM:** Git
   - **Repository URL:** `https://github.com/arpansahu/borcelle_crm.git`
   - **Credentials:** Add GitHub credentials if private repo
   - **Branch:** `*/main`
   - **Script Path:** `Jenkinsfile-build`
   - Click "Save"

### Step 4: Trigger Build

```bash
# Option 1: From Jenkins UI
# Click "Build with Parameters" → Select RUN_TESTS → Click "Build"

# Option 2: Using curl (after setting up API token)
curl -X POST "https://arpansahu:<API_TOKEN>@jenkins.arpansahu.space/job/borcelle-crm/buildWithParameters?RUN_TESTS=true"
```

## Deployment Pipeline Setup

### Step 1: Create Harbor Registry Secret in Kubernetes

```bash
ssh arpansahu@arpansahu.space

# Create Harbor secret for pulling images
sudo kubectl create secret docker-registry harbor-registry-secret \
  --docker-server=harbor.arpansahu.space \
  --docker-username=admin \
  --docker-password=Gandu302@harbor \
  --docker-email=admin@arpansahu.space \
  -n default
```

### Step 2: Create Kubernetes Secret for Environment Variables

```bash
# Create secret from .env file
sudo kubectl create secret generic borcelle-crm-secret \
  --from-env-file=.env \
  -n default
```

### Step 3: Create Deploy Pipeline in Jenkins

1. **Create New Pipeline:**
   - Name: `borcelle-crm-deploy`
   - Type: Pipeline
   - Script Path: `Jenkinsfile-deploy`

2. **Required Jenkins Credentials:**
   - `borcelle_crm_env_file` (already created)
   - `jenkins-admin-credentials` (Username/Password for SSH)
     - Username: arpansahu
     - Password: Gandu302@

### Step 4: Deploy

```bash
# Trigger deploy pipeline
# This will:
# - Pull latest image from Harbor
# - Update Kubernetes deployment
# - Run database migrations
# - Collect static files
# - Restart pods
```

## Verification

```bash
# Check deployment status
ssh arpansahu@arpansahu.space 'sudo kubectl get deployments -n default | grep borcelle'

# Check pod status
ssh arpansahu@arpansahu.space 'sudo kubectl get pods -n default | grep borcelle'

# Check logs
ssh arpansahu@arpansahu.space 'sudo kubectl logs -n default deployment/borcelle-crm-app --tail=50'

# Test application
curl -I https://borcelle.arpansahu.space
```

## Troubleshooting

### Issue: Jenkins can't read .env file
**Solution:** Ensure credential ID matches exactly: `borcelle_crm_env_file`

### Issue: Docker registry authentication failed
**Solution:** 
```bash
# Verify Harbor credentials in .env
HARBOR_USERNAME=admin
HARBOR_PASSWORD=Gandu302@harbor
```

### Issue: Static files not uploading to MinIO
**Solution:** 
```bash
# Verify MinIO settings in .env
AWS_S3_ENDPOINT_URL=https://minioapi.arpansahu.space
AWS_S3_CUSTOM_DOMAIN=minioapi.arpansahu.space/arpansahu-one-bucket
```

### Issue: Database connection failed
**Solution:**
```bash
# Check PostgreSQL is accessible
curl -I https://pgadmin.arpansahu.space
# Verify DATABASE_URL in .env uses correct port 9551
```

## Next Steps

1. ✅ Django upgraded to 4.2.28
2. ✅ Storage settings updated to STORAGES dict
3. ⏳ Create Jenkins credential with .env file
4. ⏳ Create/configure Jenkins build pipeline
5. ⏳ Trigger build to create Docker image
6. ⏳ Create Jenkins deploy pipeline
7. ⏳ Deploy to production

The codebase is ready - just need to setup Jenkins credentials and trigger the pipelines!
