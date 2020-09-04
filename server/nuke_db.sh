ls
rm -rf migrations || \
    rm bitchmin/bitchmin.db || \
    flask db init || \
    flask db migrate -m "Initial" || \
    flask db upgrade