# Borcelle CRM

This WhatsApp clone project provides a comprehensive chat application with various advanced features. Below are the main components and functionalities of the project.

## Project Features

1. **Account Functionality:** Complete account management.
2. **PostgreSql Integration:** Utilized as a database.
3. **AWS S3/MinIO Integration:** For file storage.
4. **Redis Integration:** Utilized for caching and message pub/sub.
5. **Autocomplete JS Library:** Implemented for enhanced user experience.
6. **MailJet Integration:** Used for email services.
7. **Dockerized Project:** Fully containerized for easy deployment.
8. **Kubernetes-native** Kubernetes support also available.
9. **CI/CD Pipeline:** Continuous integration and deployment included using Jenkins.

## Implemented CRM
    
1.	User Registration and Contact Management: Users can register and manage their contacts individually, with all contacts being private to each user. This includes full CRUD (Create, Read, Update, Delete) functionality for managing contacts.
2.	Messaging and Email Integration: Users can message their contacts directly through the portal. These messages are sent to the contacts’ email addresses, ensuring seamless communication.
3.	Message History Tracking: Users can track the history of messages sent to their contacts, providing a clear record of all interactions.
4.	Email Verification: Before a user can log in and access their contacts, they must verify their email address, adding a layer of security to the system.
5.	Celery and Redis Integration for Note Taking and Emailing:
    1.	Implemented Celery and Redis to manage the process of taking notes and sending them via email.
    2. Initially used Gmail with SMTP for sending emails, but due to Heroku’s restrictions on SMTP activities, MailJet was adopted for production.
    3. Users can see the progress of the task on the frontend, with a progress bar implemented using WebSockets and Channels.
6.	Task Scheduling with Celery Beat: Integrated Celery Beat to schedule emails as reminders, ensuring timely delivery based on predefined schedules.
7.	Async Operations in Signals: Utilized asyncio within Django signals to prevent conflicts with sync_to_async, ensuring smooth task execution without interference.
8.	Task Completion Notification: Upon task completion, an automatic notification is sent to the CRM manager, keeping them informed in real-time.
9.	Progress Tracking: Implemented a progress bar to visually display the progress of both scheduled and non-scheduled emails, providing users with real-time status updates.
10.	Redis as a Message Broker: Redis is employed as the message broker, facilitating the efficient handling and distribution of tasks to Celery workers.
11.	Email Task Workflow:
    1.	Immediate Email Requests: When a user requests to send notes via email, the Django application sends a task to the Redis broker. This task  is processed by Celery, with progress being saved in the CELERY_RESULT_BACKEND. Users can track progress through WebSockets and Channels, allowing the server to push status updates directly to the frontend without repeated user requests.
    2. Scheduled Email Reminders: For scheduled email reminders, the Django view creates a cron task, which is assigned to Celery Beat. When the scheduled time arrives, the task is passed to the broker, and then to Celery for execution. Upon task completion, a notification is sent through channels to the frontend, informing the user of the task’s completion.
12.	Admin Notifications: Admins can broadcast notifications to all users through Django channels. These notifications can be scheduled via cron and Celery Beat, and when the time arrives, the task is processed and sent to users connected to the channels, ensuring real-time updates.


[alt text](https://github.com/arpansahu/borcelle_crm/blob/master/explanation.png?raw=true)

