#!/bin/bash
WORK_DIR=`dirname $0`
PKG_NAME='ncelery'
SRC="../ncelery"
PKG_PATH="$PKG_NAME"

python "pick.py" $SRC $PKG_NAME

mkdir -p "${PKG_PATH}/utils"
cp $SRC/utils/ ${PKG_PATH}/ -fr
cp $SRC/config ${PKG_PATH}/ -fr
cp $SRC/celery.py ${PKG_PATH}
cp $SRC/exception.py ${PKG_PATH}
sed -i -e "s/IS_NCELERY_API = False/IS_NCELERY_API = True/g" $PKG_PATH/config/conf.py
sed -i "/LOGGING_CONFIG_FILE/d" $PKG_PATH/config/conf.py
#sed -i "/connect(MONGO_DB/d" $PKG_PATH/conf.py
sed -i "/include=conf.INCLUDE_APP/d" $PKG_PATH/celery.py
sed -i "/fileConfig/d" $PKG_PATH/celery.py

sed -i -e "s/version = '.*'/version = '1.0'/g" setup.py
python "setup.py" "bdist_egg"
