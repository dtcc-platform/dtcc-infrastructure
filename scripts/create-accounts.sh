#!/bin/bash

random_string=$(printf '%s' $(echo "$RANDOM" | md5sum) | cut -c 1-10)
#echo $random_string

function user_exists_passwd() {
    local username="$1"

    if grep -q "^$username:" /etc/passwd; then
#        echo "User $username exists."
        return 0
    else
#        echo "User $username does not exist."
        return 1
    fi
}


while IFS= read -r line; do
    # Extract username and name
#    username=$(echo "$line" | awk '{print $1}')
    name=$(echo "$line" | awk '{print $1,$2}')
    host=$(echo "$line" | awk -F '@' '{split($2, arr, "."); print arr[1]}')
    if [ "$host" == "chalmersindustriteknik" ]; then
    host="cit"
    fi
    if [ "$host" == "stadsbyggnad" ]; then
    host="goteborg"
    fi
    username=$(echo "$name"| awk '{print $2}'| tr '[:upper:]' '[:lower:]')
    username=$host\-$username
    if user_exists_passwd "$username"; then
    echo "User exists, skipping"
    else
    echo "User does not exist."
    useradd -m -s /bin/bash "$username"
    usermod -c "$name" "$username"
    newpass=`cat /dev/urandom | tr -dc 'A-Za-z0-9!@+-' | head -c8 ; echo`
    echo $newpass
    echo "$username:$newpass" | chpasswd
    # Force password change on first login
#    chage -d 0 "$username"
    echo "Account created for: $username"
    echo $username $newpass >> userslist-$random_string\.txt
    fi
sleep 1
done < "$1"
echo "User account creation completed!"
