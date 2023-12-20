# COMMAND TO CREATE THE DOCKER IMAGE

docker build -t testagram:v1 .

# COMMAND TO RUN THE DOCKER container

docker run -d --network=host  --name test_cont testagram:v1

#acces the endpoints using below
http://127.0.0.1:8000/<endpoint>

# Endpoints and request bodies
--------------------------------------------------------------------------
# /register

{
  "username": "abhay123aa",
  "password": "random_password456",
  "email": "aqfy@example.com"
}

---------------------------------------------------------------------------
# /login

{
  "username": "random_username123",
  "password": "random_password456"

}

---------------------------------------------------------------------------
# /create_post

{"title":"my photo",
"content":"image"
}

---------------------------------------------------------------------------

# get_all_post
  add token in headers

---------------------------------------------------------------------------

# /add_reaction
like:1
unlike:0

{
"post_id":"fb4e568f10164474bad6c68dfde52761",
"like_status":0
}
---------------------------------------------------------------------------

# /add_comment

{
    "comment":"nice pic",
    "post_id":"fb4e568f10164474bad6c68dfde52761"
    
}

---------------------------------------------------------------------------

