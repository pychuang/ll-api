# CREATE ADMIN
$ mongo
> use admin
> use admin
> db.createUser(
  {
    user: "admin",
    pwd: "ADMINSECRET",
    roles:
    [
      {
        role: "userAdminAnyDatabase",
        db: "admin"
      }
    ]
  }
)

# CREATE USER
$ mongo
> use ll
> db.createUser(
    {
      user: "ll",
      pwd: "USERSECRET",
      roles: ["readWrite"],
    }
)
