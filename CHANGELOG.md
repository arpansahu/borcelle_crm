# Changelog

All notable changes to the Borcelle CRM project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-02-17
### Added
- Enhanced contact management features with autocomplete functionality
- Improved real-time notification system with WebSocket connection management
- Added comprehensive health check system for service monitoring
- Email notification templates with Celery task queue integration
- Manager dashboard with advanced analytics and reporting
- Automated README generation and HTML documentation system
- Flatpickr date picker integration for better UX
- SweetAlert2 for improved user notifications
- HTMX for dynamic content loading without full page refreshes

### Changed
- Optimized WebSocket connection handling for better performance
- Enhanced Celery task management and monitoring
- Improved Docker and Kubernetes deployment configurations
- Updated static file management with better caching strategies
- Refined supervisor configuration for process management

### Fixed
- WebSocket reconnection issues on network interruptions
- Celery task retry logic for failed email deliveries
- Static file serving in production environments
- Database connection pooling optimization
- CORS configuration for better API security

### Security
- Enhanced authentication middleware with rate limiting
- Improved CSRF protection for AJAX requests
- Updated dependencies to patch known vulnerabilities
- Strengthened OAuth social authentication validation
- Added security headers for XSS and clickjacking protection

## [2.0.0] - 2026-02-13
### Added
- Comprehensive environment configuration with support for RabbitMQ, Kafka, Elasticsearch
- OAuth social authentication integration (Google, GitHub, Facebook, Twitter, LinkedIn)
- Enhanced security with SSL/TLS support for Redis and PostgreSQL  
- MinIO storage backend with fallback to AWS S3
- Advanced monitoring with Sentry integration
- Celery Beat scheduler for automated tasks
- Real-time notifications via Django Channels and WebSockets
- Flower dashboard for Celery monitoring
- Docker and Kubernetes deployment support
- CI/CD pipeline via Jenkins
- Comprehensive testing framework setup

### Changed
- Updated database configuration to use production PostgreSQL with schema support
- Migrated to updated Redis and RabbitMQ configurations
- Enhanced storage backends for better file management
- Improved security policies and best practices

### Fixed
- Database schema creation and migration issues
- SSL/TLS certificate handling for remote services
- Environment variable configuration consistency

## [1.0.0] - 2024-06-27
### Added
- Initial release of the project.
- User authentication module.