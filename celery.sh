#!/bin/bash
#ncelery
#create at 2012-10-16
#
#chkconfig: -99 14
#description:
#Author acey9 
#created by 2011-01-25
#modify acey9 
#. /etc/rc.d/init.d/functions

DAEMON_PATH=`dirname $0`
OLD_DIR=`pwd`
cd $DAEMON_PATH
SUPERVISORD_CONF=`grep SUPERVISORD_CONF supervisord_conf.py|grep -v 'grep' |awk -F "=" '{print $2}'|awk -F "\'" '{print $2}'`
cd $OLD_DIR
create_conf_file() { 
		OLD_DIR=`pwd`
		cd $DAEMON_PATH
		echo $SUPERVISORD_CONF
		#supervisorctl -c  $SUPERVISORD_CONF stop all 
		#supervisorctl -c  $SUPERVISORD_CONF shutdown
		python superman.py #&& supervisord -c $SUPERVISORD_CONF 
		cd $OLD_DIR
		}

create_api_pkg() {
		OLD_DIR=`pwd`
		cd $DAEMON_PATH/api
		sh api.sh
		cd $OLD_DIR
		}

run_cmd() {
		rcmd=$1
		echo 'runing: '$rcmd
		$rcmd
		}
ncelery_start() {
		cmd="supervisord -c $SUPERVISORD_CONF"
		run_cmd "$cmd"
		echo 'started.'
		}

ncelery_reload() {
		cmd="supervisorctl -c $SUPERVISORD_CONF reload"
		run_cmd "$cmd"
		echo 'reload.'
		}

ncelery_stop() {
		cmd1="supervisorctl -c $SUPERVISORD_CONF stop all"
		cmd2="supervisorctl -c $SUPERVISORD_CONF shutdown"
		run_cmd "$cmd1" && run_cmd "$cmd2"
		echo 'stoped.'
		}

ncelery_status() {
		cmd="supervisorctl -c $SUPERVISORD_CONF status"
		run_cmd "$cmd"
		}

ncelery_startwk() {
		cmd="supervisorctl -c $SUPERVISORD_CONF start "$1""
		run_cmd "$cmd"
		}

ncelery_stopwk() {
		cmd="supervisorctl -c $SUPERVISORD_CONF stop "$1""
		run_cmd "$cmd"
		}

case $1 in 
	api)
		create_api_pkg	
		;;
	conf)
		create_conf_file
		;;
	start)
		ncelery_start
		;;
	stop)
		ncelery_stop
		;;
	reload)
		ncelery_reload
		;;
	restart)
		ncelery_stop && ncelery_start
		;;
	status)
		ncelery_status
		;;
	startwk)
		ncelery_startwk "$2"
		;;
	stopwk)
		ncelery_stopwk "$2"
		;;
	restartwk)
		ncelery_stopwk "$2" && ncelery_startwk "$2"
		;;
	*)
		echo "usage:$0 api|start|stop|restart|reload|conf|stopwk|startwk|restartwk|status [worker]"
esac
