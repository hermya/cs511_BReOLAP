while read -r line; do
    #echo ${line}
    envline="$(echo "${line}" |
        sed 's/[[:blank:]]*=[[:blank:]]*/=/g' |
        sed 's/^[[:blank:]]*//g' |
        grep -E "^[[:upper:]]([[:upper:]]|_|[[:digit:]])*=" ||
        true)"
    #echo ${envline}
    envline="$(eval "echo ${envline}")"
    #echo ${envline}
    #echo ${envline}
    if [[ "${envline}" == *"="* ]]; then
        echo ${envline}
        echo
        #eval 'export "${envline}"'
    fi
done <"be.conf"