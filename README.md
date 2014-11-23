ncelery
=========================
ncelery是一个celery快速开发项目，目的在于快速增加celery task到celery平台

### Features
- 快速增加celery task
- supervisord启动celery worker
- 自动生成supervisord配置文件
- 抽取api接口供其他平台调用

### Install
    $ pip install celery
	$ pip install supervisor
	$ git clone git@github.com:Acey9/ncelery.git

### Configuration
	================================
	ncelery configuration
	================================
	$vim ncelery/ncelery/config/conf.py
	"""celery configuration"""
	#Name of the main module if running
	MAIN_NAME = "Pandaria"

	#URL of the default broker used
	BROKER = 'amqp://guest@espp.broker.com:5672//'

	#The result store backend class, or the name of the backend class to use
	BACKEND = 'redis://espp.redis.com:6379/1'
         
	#Periodic Tasks 
	CELERY_TIMEZONE = 'Asia/Shanghai'
	CELERYBEAT_SCHEDULE = {}
	CELERYBEAT_SCHEDULE_FILENAME = '/var/log/2ncelery/beat-schedule'

	#app switch conf
	APP_MODE_NUM = {
        #celery加载哪些任务，后面的数字为worker数量
        'ncelery.tasks.example':1,
        }

	#ack late
	CELERY_ACKS_LATE = True

	#Tasks settings
	CELERY_DEFAULT_QUEUE = "celery"

	#result settings
	CELERY_TASK_RESULT_EXPIRES = 60*15
	CELERY_IGNORE_RESULT = True

	#worker settings
	#Maximum number of tasks a pool worker process can execute before it’s replaced with a new one.
	CELERYD_MAX_TASKS_PER_CHILD = 128
	#The number of concurrent worker processes/threads/green threads executing tasks.
	CELERYD_CONCURRENCY = 1
	#How many messages to prefetch at a time multiplied by the number of concurrent processes
	CELERYD_PREFETCH_MULTIPLIER = 4

	#Task hard time limit in seconds. The worker processing the task will be killed and replaced 
	#with a new one when this is exceeded.
	CELERYD_TASK_TIME_LIMIT = 60*6

	#Task soft time limit in seconds.
	#The SoftTimeLimitExceeded exception will be raised when this is exceeded. 
	#The task can catch this to e.g. clean up before the hard time limit comes.
	CELERYD_TASK_SOFT_TIME_LIMIT = 60*5

	#Maximum number of connections available in the Redis connection pool used for sending and retrieving results.
	CELERY_REDIS_MAX_CONNECTIONS = 128

	#The maximum number of connections that can be open in the connection pool.
	BROKER_POOL_LIMIT = 10
	CELERYD_POOL_RESTARTS = True

	#Send events so the worker can be monitored by tools like celerymon.
	CELERY_SEND_EVENTS = False

	#If enabled, a task-sent event will be sent for every task so tasks can be 
	#tracked before they are consumed by a worker.
	CELERY_SEND_TASK_SENT_EVENT = False

	# Enables error emails.
	CELERY_SEND_TASK_ERROR_EMAILS = False
	#Name and email addresses of recipients
	#List of (name, email_address) tuples for the administrators that should receive error emails.
	ADMINS = (
    	('wanghui', 'wanghui@xx.com'),
	)
	#Email address used as sender (From field).
	SERVER_EMAIL = 'nightswatch@xx.com'
	#Mailserver configuration
	EMAIL_HOST = '10.7.254.150'
	EMAIL_PORT = 25
	EMAIL_HOST_USER = 'nightswatch'
	EMAIL_HOST_PASSWORD = ''
	#Timeout in seconds for when we give up trying to connect to the SMTP server when sending emails.
	EMAIL_TIMEOUT = 5
	#Use SSL when connecting to the SMTP server.
	EMAIL_USE_SSL = False
	#Use TLS when connecting to the SMTP server. 
	EMAIL_USE_TLS = False

	#logging
	LOGGING_CONFIG_FILE = os.path.normpath(os.path.join(PROJECT_PATH, 'config/logging.cfg'))
	CELERYD_HIJACK_ROOT_LOGGER = False
	CELERY_REDIRECT_STDOUTS_LEVEL = 'INFO'

	=========================
	supervisord configuration
	=========================
	$vim ncelery/supervisord_conf.py
	#celery configuration
	CELERY_USER = "top"
	CELERY_LOG_LEVEL = "INFO"                                  
	BEAT_IS_ON = False #是否开启celery beat
	BEAT_PID_FILE = '/var/log/2ncelery/celery_beat.pid' #celery beat pid文件
	NIGHTSWATCH_PID_FILE = '/var/log/2ncelery/nighitswatch.pid' #celery worker存活监控进程pid文件                          
	
	#supervisor conf
	SPVR_START_PROGRAM_USER = "root"
	SPVR_PROGRAM_LOG_DIR = "/var/log/2supervisord/"            
	SPVR_SOCK = '/var/run/ncelery.supervisor.sock'             
	SPVR_PORT = 9999 
	SPVR_ADMIN = 'fan'                                         
	SPVR_ADMIN_PASSWORD = 'fan'
	SPVR_LOG_FILE = '/var/log/2supervisord/supervisord.log'    
	SPVR_PID_FILE = '/var/run/2supervisord.pid'                
	SPVR_CHILDLOGDIR = '/var/log/2supervisord/'                
	    
	#supervisord configuration file.                           
	SUPERVISORD_CONF = '/etc/ncelery/supervisord/supervisord.conf' 

### Runing
    $cd ncelery/
	$./celery.sh conf
	$./celery.sh start
	$./celery.sh startwk all
	$./celery.sh status

### Test
	$cd ncelery/ncelery/test/example
	$python tasks.py

### task develop example
	所有task放到ncelery/ncelery/tasks目录
	目录结构示例如下：
	example/
	├── __init__.py
	├── taskconf.py
	└── tasks.py
	其中taskconf.py文件必须存在,这里配置任务相关信息
	
	#task代码示例
	$cd ncelery/ncelery/tasks/example
	$vim tasks.py
	from ncelery.celery import ncelery
	@ncelery.task(ignore_result=False)
	def add(x, y):
    		return x+y
	
	任务配置示例，必须配置以下选项:
	$cd ncelery/ncelery/tasks/example
	$vim taskconf.py
	INCLUDE_APP = ['ncelery.tasks.example.tasks',]

	CELERY_ROUTES = {
	        "ncelery.tasks.example.tasks.add":{
	            "queue":"ncq.example"
	            },
	        }
	
	CELERYBEAT_SCHEDULE = {
	        'add-every-30-minute':{
	            'task': 'ncelery.tasks.example.tasks.add',
	            'schedule': timedelta(seconds=60*30),
	            },
	        }
	
	CELERY_ANNOTATIONS = {
	    "ncelery.tasks.example.tasks.add":{
	        "time_limit":15,
	        "soft_time_limit":10,
	        },
	}

### api use usage
	生成api
	$cd ncelery
	$./celery.sh api
	执行完成后再api/dist目录下面就能看到类似这样的包了，ncelery_api-1.0.1400-py2.7.egg
	
	api用法,请到需要用到api的平台安装egg包
	>>>from ncelery.config import conf
	>>>conf.BROKER = 'amqp://guest@localhost//'       #设置broker
	>>>conf.BACKEND = 'amqp://guest@localhost//'      #设置backend
	>>>from ncelery.tasks.example.tasks import add
	>>>add.delay(1, 2)
