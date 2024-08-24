## What is Python ?
Python is a high-level, general-purpose programming language. Its design philosophy emphasizes code readability with the
use of significant indentation. Python is dynamically typed and garbage-collected. It supports multiple programming 
paradigms, including structured, object-oriented and functional programming.

## What is Django ?
Django is a Python-based free and open-source web framework that follows the model-template-view architectural pattern.

## What is Redis ?
    
Redis is an in-memory data structure project implementing a distributed, in-memory key-value database with optional durability. 
The most common Redis use cases are session cache, full-page cache, queues, leader boards and counting, publish-subscribe, and much more. in this case, we will use Redis as a message broker.

## What is Ajax?
Ajax is a set of web development techniques that uses various web technologies on the client-side to create asynchronous web applications. With Ajax, web applications can send and retrieve data from a server asynchronously without interfering with the display and behavior of the existing page.

## What is Web Sockets ?

WebSocket is bidirectional, a full-duplex protocol that is used in the same scenario of client-server communication, unlike HTTP it starts from ws:// or wss://. It is a stateful protocol, which means the connection between client and server will keep alive until it is terminated by either party (client or server). After closing the connection by either of the client and server, the connection is terminated from both ends. 

## What is Channels?
Channels preserve the synchronous behavior of Django and add a layer of asynchronous protocols allowing users to write the views that are entirely synchronous, asynchronous, or a mixture of both. Channels basically allow the application to support “long-running connections”. It replaces Django’s default WSGI with its ASGI.

## What is Django Signals?
Django includes a “signal dispatcher” which helps decoupled applications get notified when actions occur elsewhere in the framework. In a nutshell, signals allow certain senders to notify a set of receivers that some action has taken place.


## What is Celery ?
Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operation but supports scheduling as well.

Why is this useful?

1. Think of all the times you have had to run a certain task in the future. Perhaps you needed to access an API every hour. Or maybe you needed to send a batch of emails at the end of the day. Large or small, Celery makes scheduling such periodic tasks easy.
2. You never want end users to have to wait unnecessarily for pages to load or actions to complete. If a long process is part of your application’s workflow, you can use Celery to execute that process in the background, as resources become available, so that your application can continue to respond to client requests. This keeps the task out of the application’s context.

Working:
1. Celery requires message broker to store messages received from task generators or producers. For reading information of messages in task
  serialization is required which can be in json/pickle/yaml/msgpack it can be in compressed form as zlib, bzip2 or a cryptographic message.
2. A celery system consists of multiple workers and brokers, giving way to high availability and horizontal scaling.
3. When a celery worker is started using command ```celery -A [borcelle_crm(project name)].celery worker -l info```, a supervisor is started.
4. Which spawns child processes or threads and deals with all the bookkeeping stuff. The child processes or threads execute the actual task.
  This child process are also known as execution pool. By default, no of child process worker can spawn is equal to the no of CPU cores.
5. The size of execution pool determines the number of tasks your celery worker can process
   1. Worker ----- Pool ----- Concurrency 
   2. When you start a celery worker, you specify the pool, concurrency, autoscale etc. in the command 
   3. Pool - Decides who will actually perform the task -thread, child process, worker itself or else. 
   4. Concurrency: will decide the size of pool
   5. autoscale: to dynamically resize the pool based on load. The autoscaler adds more pool processes when there is work
     to do, and starts removing processes when the workload is low.
   6. ```celery -A <project>.celery worker --pool=preform --concurrency=5 --autoscale=10 3 -l info ``` 
    this command states to start a worker with 5 child processes which can be auto-scaled upto 10 and can be decreased upto 3.
6. Type of Pools: 
    1. prefork (multiprocessing) (default):
       1. Use this when CPU bound task
       2. By passes GIL (Global Interpreter Lock)
       3. The number of available cores limits the number of concurrent processes.
       4. That's why Celery defaults concurrency to no of CPU cores available.
       5. Command: ```celery A -<project>.celery worker -l info```
    2. solo (Neither threaded nor process-based)
        1. Celery don't support windows, so you can use this pool of running celery on Windows
        2. It doesn't create pool as it runs solo.
        3. Contradicts the principle that the worker itself does not process any tasks
        4. The solo pool runs inside the worker process.
        5. This makes the solo worker fast, But it also blocks the worker while it executes tasks.
        6. In this concurrency doesn't make any sense.
        7. Command ```celery A -<project>.celery worker --pool=solo -l info```
    3. threads (multi threading)
        1. due to GIL in CPython, it restricts to single thread so can't achieve real multithreading
        2. Not much official support
        3. Uses threading module of python
        4. Command ```celery A -<project>.celery worker --pool=threads -l info```
    4. gevent/eventlet (Green Threads)
       1. Uses Green thread which are user level threads so can be manipulated at code level 
       2. This can be used to get a thousand of HTTP get request to fetch from external REST APIs.
       3. The bottleneck is waiting for I/O operation to finish and not CPU.
       4. There are implementation differences between the eventlet and gevent packages
       5. Command ```celery A -<project>.celery worker --pool=[gevent/eventlet] worker -l info```
    5. by default ```celery A -<project>.celery worker -l info``` uses pool-prefork and concurrency -no of cores
    6. Difference between greenlets and threads -
       1. Python's threading library makes use of the system's native OS to schedule threads. This general-purpose scheduler is not always very efficient. 
       2. It makes use of Python's global interpreter lock to make sure shared data structures are accessed by only one thread at a time to avoid race conditions.
          CPython Interpreter, GIL, OS Greenlets emulate multi-threaded environments without relying on any native operating system capabilities.
          Greenlets are managed in application space and not in kernel space. In greenlets, no scheduler pre-emptively switching between your threads
          at any given moment. 
       3. Instead, your greenlets voluntarily or explicitly give up control to one another at specified points in your code. 
       4. Thus more scalable and efficient. Less RAM required.
       
## What is Redis ?
    
Redis is an in-memory data structure project implementing a distributed, in-memory key-value database with optional durability. 
The most common Redis use cases are session cache, full-page cache, queues, leaderboards and counting, publish-subscribe, and much more. in this case, we will use Redis as a message broker.

## What is RabbitMQ ?

RabbitMQ is an open-source message broker that facilitates communication between different parts of a system by transmitting messages between producers and consumers. It implements the Advanced Message Queuing Protocol (AMQP), which is a standard protocol for messaging. 

In a typical scenario, producers send messages to a queue managed by RabbitMQ, and consumers receive those messages from the queue. This setup allows for asynchronous communication, meaning that producers and consumers don't need to interact with each other directly or even be online at the same time. RabbitMQ ensures that messages are reliably stored and delivered, which is crucial for maintaining data integrity in distributed systems.

RabbitMQ supports a variety of messaging patterns, including point-to-point messaging, publish/subscribe, and complex routing with exchanges that can direct messages to different queues based on rules. It is widely used for task queuing, where tasks are distributed across multiple workers, and for decoupling microservices, enabling them to communicate effectively without being tightly coupled.

Its lightweight, flexible, and scalable nature makes RabbitMQ a popular choice for building robust, fault-tolerant systems, particularly in cloud environments where scalable message queuing is essential for maintaining system performance and reliability.
