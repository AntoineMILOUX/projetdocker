db.createUser({
    user: "JeanM",
    pwd: "jeanm",
    roles : [
        {
            "role": "readWrite",
            "db": "tot"
        }
    ]
})