# Security Policy

## Overview

Security is a top priority for Borcelle CRM. This document outlines our security practices, vulnerability reporting procedures, and guidelines for maintaining a secure deployment.

## Supported Versions

We provide security patches for the latest major and minor releases. Users are strongly encouraged to always update to the latest version to ensure they have the most recent security fixes.

| Version       | Supported          | End of Support |
| ------------- | ------------------ | -------------- |
| 2.1.x         | :white_check_mark: | Current        |
| 2.0.x         | :white_check_mark: | 2026-08-13     |
| 1.0.x         | :x:                | 2026-02-13     |
| < 1.0         | :x:                | N/A            |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability, please send an email to [admin@arpansahu.space](mailto:admin@arpansahu.space). To help us better understand and resolve the issue quickly, please include:

- **Type of vulnerability** (e.g., SQL injection, XSS, authentication bypass)
- **Full paths of source file(s)** related to the vulnerability
- **Location** of the affected source code (tag/branch/commit or direct URL)
- **Step-by-step instructions** to reproduce the issue
- **Proof-of-concept or exploit code** (if possible)
- **Impact assessment** (what data can be accessed, modified, or deleted)
- **Suggested remediation** (if you have any)
- **Your contact information** for follow-up questions

### Response Time

We take security reports seriously and will respond according to the following timeline:

- **Initial Response**: Within 48 hours of receiving your report
- **Status Update**: Within 5 business days with our initial assessment
- **Resolution Timeline**: Within 30 days for critical vulnerabilities
- **Public Disclosure**: Coordinated with the reporter after patch release

### Handling Vulnerabilities

Once a vulnerability is reported, the following steps will be taken:

1. **Acknowledgment**: We will acknowledge receipt of the vulnerability report.
2. **Investigation**: We will investigate the vulnerability and determine its impact.
3. **Fix Development**: We will develop a fix for the vulnerability.
4. **Patch Release**: We will release a patch for the supported versions listed above.
5. **Public Disclosure**: We will publicly disclose the vulnerability and the fix once the patch is released.

## Security Best Practices

### Application Configuration

#### Django Settings
- **Never use `DEBUG = True` in production**
- Set `SECRET_KEY` to a strong, randomly generated value (never commit to version control)
- Configure `ALLOWED_HOSTS` appropriately for your domain
- Enable `SECURE_SSL_REDIRECT`, `SECURE_HSTS_SECONDS`, and other security middleware
- Use `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` in production
- Set appropriate `CORS_ALLOWED_ORIGINS` (avoid using `*`)

#### Database Security
- Use strong, unique passwords for database connections
- Enable SSL/TLS for PostgreSQL connections in production
- Restrict database access to application servers only
- Regularly backup and encrypt database dumps
- Use connection pooling with appropriate limits

#### Redis & Message Brokers
- Enable authentication for Redis with strong passwords
- Use TLS for Redis connections in production
- Configure RabbitMQ/Kafka with proper authentication
- Restrict network access to message brokers

#### OAuth & Authentication
- Rotate OAuth client secrets regularly
- Use HTTPS for all OAuth redirect URIs
- Implement rate limiting on authentication endpoints
- Enable two-factor authentication (2FA) for admin users
- Use strong password policies (minimum length, complexity requirements)
- Implement account lockout after failed login attempts

#### File Storage
- Use signed URLs for S3/MinIO access with appropriate expiration
- Validate file types and sizes before upload
- Scan uploaded files for malware
- Set proper bucket permissions (never public write access)
- Use separate storage buckets for different data sensitivity levels

#### WebSocket Security
- Authenticate WebSocket connections properly
- Implement message rate limiting
- Validate all incoming WebSocket messages
- Use WSS (WebSocket Secure) in production

#### Container Security
- Regularly update base Docker images
- Scan containers for vulnerabilities
- Run containers as non-root users
- Use Kubernetes network policies to restrict pod communication
- Set resource limits to prevent DoS attacks

#### Monitoring & Logging
- Enable comprehensive logging (but never log sensitive data)
- Set up alerts for suspicious activities
- Monitor Celery task failures and retries
- Use Sentry for error tracking and performance monitoring
- Regularly review access logs

### Dependency Management
- Regularly update Python packages: `pip list --outdated`
- Use `pip-audit` or `safety` to check for known vulnerabilities
- Review `requirements.txt` and remove unused dependencies
- Pin specific versions in production to ensure reproducibility

### API Security
- Implement API rate limiting
- Use API authentication tokens with appropriate scopes
- Validate and sanitize all input data
- Use HTTPS for all API endpoints
- Implement proper CORS policies

### General Security
- Keep your software up to date
- Use strong, unique passwords for all accounts
- Enable two-factor authentication (2FA) where possible
- Regularly review and update security settings
- Conduct periodic security audits
- Train team members on security best practices

## Known Security Considerations

### Django-Specific
- **SQL Injection**: Always use Django ORM parameterized queries
- **XSS**: Template auto-escaping is enabled; be cautious with `|safe` filter
- **CSRF**: Ensure CSRF tokens are included in all forms and AJAX requests
- **Clickjacking**: X-Frame-Options middleware is enabled
- **SSL/TLS**: Enforce HTTPS in production environments

### Third-Party Services
- **Sentry**: Ensure sensitive data is not sent to error tracking
- **OAuth Providers**: Validate redirect URIs and state parameters
- **Elasticsearch**: Secure with authentication if exposed
- **Flower**: Protect with authentication; do not expose publicly

## Security Updates

Security updates are released as needed and will be announced via:
- GitHub Security Advisories
- CHANGELOG.md with `[SECURITY]` tag
- Email notification to registered administrators

## Compliance

This project implements security controls aligned with:
- OWASP Top 10 Web Application Security Risks
- Django Security Best Practices
- CWE/SANS Top 25 Most Dangerous Software Errors

## Contact

For security-related questions, concerns, or reports, please contact:
- **Email**: [admin@arpansahu.space](mailto:admin@arpansahu.space)
- **PGP Key**: Available upon request for encrypted communications

## Security Hall of Fame

We thank the following individuals and organizations for responsibly disclosing vulnerabilities:

*No vulnerabilities have been reported yet. Be the first to help us improve security!*

---

**Last Updated**: 2026-02-17  
**Next Review**: 2026-08-17