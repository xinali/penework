#!/bin/bash

# Admin User
MONGODB_ADMIN_USER=${MONGODB_ADMIN_USER:-"admin"}
MONGODB_ADMIN_PASS=${MONGODB_ADMIN_PASS:-"admin"}

# Application Database User
MONGODB_APPLICATION_DATABASE=${MONGODB_APPLICATION_DATABASE:-"penework"}
MONGODB_APPLICATION_USER=${MONGODB_APPLICATION_USER:-"penework"}
MONGODB_APPLICATION_PASS=${MONGODB_APPLICATION_PASS:-"penework"}

# Wait for MongoDB to boot
RET=1
while [[ RET -ne 0 ]]; do
    echo "=> Waiting for confirmation of MongoDB service startup..."
    sleep 5
    mongo admin --eval "help" >/dev/null 2>&1
    RET=$?
done

# Create the admin user
echo "=> Creating admin user with a password in MongoDB"
mongo admin --eval "db.createUser({user: '$MONGODB_ADMIN_USER', pwd: '$MONGODB_ADMIN_PASS', roles:[{role:'root',db:'admin'}]});"

sleep 3

# create application db user
if [ "$MONGODB_APPLICATION_DATABASE" != "admin" ]; then
    echo "=> Creating a ${MONGODB_APPLICATION_DATABASE} database user with a password in MongoDB"
    mongo admin -u $MONGODB_ADMIN_USER -p $MONGODB_ADMIN_PASS << EOF
echo "Using $MONGODB_APPLICATION_DATABASE database"
use $MONGODB_APPLICATION_DATABASE
db.createUser({user: '$MONGODB_APPLICATION_USER', pwd: '$MONGODB_APPLICATION_PASS', roles:[{role:'dbOwner', db:'$MONGODB_APPLICATION_DATABASE'}]})
EOF
fi

sleep 1

# If everything went well, add a file as a flag so we know in the future to not re-create the
# users if we're recreating the container (provided we're using some persistent storage)
touch /data/db/.mongodb_password_set

echo "MongoDB configured successfully. You may now connect to the DB."
