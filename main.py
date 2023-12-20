
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from db.schema import Session,User,Post,Comment,Like
from utils.user_util import  *
from config_data.config import HOST,PORT
app = Flask(__name__)
sql_session=Session()

# CORS(app)

@app.route('/register', methods=['POST'])
def register():
    '''This Api registers the new user
        request: json
        return :json
    '''
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password=hashed_password)
    sql_session.add(new_user)
    sql_session.commit()
    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    '''This api is for login
        request: json
        return :json
    '''
    req_json = request.json
    user = sql_session.query(User).filter_by(username=req_json['username']).first()
    if user and check_password_hash(user.password,req_json['password']):
        response={
                'token':generate_jwt_token({"username":req_json['username'],'user_id':user.id}),
                'status':'success',
                'message':'Logged In'}
        return jsonify(response)
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/create_post', methods=['POST'])
def create_post():
    '''
        This Api creates the new post
        request: json
        return :json
    '''
    req_json = request.json
    user_info =decode_jwt_token(request)
    post_id=uuid4().hex
    user = sql_session.query(User).filter_by(username=user_info['username']).first()
    new_post = Post(id=post_id,title=req_json['title'], content=req_json['content'], user=user)
    sql_session.add(new_post)
    sql_session.commit()
    post_details=sql_session.query(Post).filter_by(id=post_id).first()
    response={
            "post_details":{
                            "post_id":post_id,
                            "title":str(post_details.title),
                            'content':str(post_details.content),
                            'username':str(user_info['username'])},
            'message': 'Post created successfully',
            "status":"success"
            }
    return jsonify(response)
    
@app.route('/add_reaction',methods=['POST'])
def add_reaction():
    '''
        This Api performs like and unlike over the post 
        request: json
        return :json
    '''
    try:
        req_json=request.json
        user_info=decode_jwt_token(request)
        user_id_from_token=user_info['user_info']['user_id']
        like_status=req_json.get('like_status')

        is_already_liked=sql_session.query(Like).filter_by(user_id=user_id_from_token).first()
        post_instance = sql_session.query(Post).filter_by(id=req_json.get('post_id')).first()

        if not is_already_liked:
            if like_status:
                post_instance.like_count += 1
                reaction = Like(post_id=req_json['post_id'], user_id=user_id_from_token)
                sql_session.add(reaction)
        else:
            return jsonify({"message":'user already the post',"status":"success"})

        if not like_status:
            post_instance.like_count -= 1
            sql_session.query(Like).filter_by(user_id=user_id_from_token).delete()

        sql_session.commit()
        return jsonify({"message":'reaction added successfully',"status":"success"})
    except Exception as e:
        return jsonify({"message":"did not add reaction","status":"failure",'error':e})

@app.route('/add_comment',methods=['POST'])
def add_comment():
    '''
        This Api adds the comment on the post
        request: json
        return :json
    '''
    try:
        user_info=decode_jwt_token(request)
        req_json=request.json
        comment=req_json.get('comment')
        post_id=req_json.get('post_id')
        user_id=user_info['user_info']['user_id']
        user=sql_session.query(User).filter_by(username=user_info['user_info']['username']).first()
        new_comment=Comment(text=comment,user=user,post_id=post_id,user_id=user_id)
        sql_session.add(new_comment)
        sql_session.commit()
        return {"message":"added comment succesfully"}
    except Exception as e:
        return jsonify({"message":"did not add reaction","status":"failure",'error':e})


@app.route('/get_all_post', methods=['GET'])
def get_posts():
    '''
        This Api returns the post details
        request: json
        return :json
    '''
    decode_jwt_token(request)
    try:
        posts = sql_session.query(Post).all()
        post_list = []
        for post in posts:
            likes_count=sql_session.query(Like).filter_by(post_id=post.id).count()
            comments=sql_session.query(Comment).filter_by(post_id=post.id)
            post_comments=[]
            for comment in comments:
                user=sql_session.query(User).filter_by(id=comment.user_id).first()
                post_comments.append({'username':user.username,'comment ':comment.text,'time':comment.timestamp})

            post_data = {
                'id': post.id,
                'title': post.title,
                'content': post.content,
                'timestamp': post.timestamp,
                'user': post.user.username,
                'likes':likes_count,
                'comments':post_comments
            }
            post_list.append(post_data)
        return jsonify({'posts': post_list})
    except Exception as e:
        return jsonify({"message":"failed to fetch posts","status":"failure",'error':e})

if __name__ == '__main__':
    app.run( host=HOST,port=PORT,debug=False)
