from fastapi import FastAPI,Depends,status,Response,HTTPException
import schemas
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from typing import List
from hashing import Hash
app = FastAPI()


models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog',status_code=201,tags = ['Blogs'])
def create(request:schemas.Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog',response_model=List[schemas.Show_blog],tags = ['Blogs'])
def all_blogs(db:Session = Depends(get_db)):
    blog = db.query(models.Blog).all()
    return blog

@app.get('/blog/{id}',response_model=schemas.Show_blog,status_code = 200,tags = ['Blogs'])
def blog_id(id,response:Response,db:Session = Depends(get_db)):
    #blog = db.query(models.Blog).get(id)
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        #response.status_code = 404
        raise HTTPException(status_code = 404,detail = f'Blog with id {id} not found in database')
        #return {'details':f'Blog with id {id} not found in database'}
    
    return blog

@app.delete('/blog/{id}',status_code=204,tags = ['Blogs'])
def blog_delete(id,response:Response,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    if not blog:
        #response.status_code = 404
        raise HTTPException(status_code = 404,detail = f'Blog with id {id} not found in database')
        #return {'details':f'Blog with id {id} not found in database'}
    db.commit()
    return 'Done'

@app.put('/blog/{id}',status_code = 202,tags = ['Blogs'])
def update_blog(id,request:schemas.Blog,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code = 404,detail= f'Blog with id {id} not found in database')
    print(request)
    blog.update({'title':request.title,'body':request.body})
    db.commit()
    return 'Blog Updated'


@app.post('/user',response_model = schemas.Show_user,tags = ['Users'])
def create_user(request:schemas.User,db:Session = Depends(get_db)):
    
    new_user = models.User(name = request.name, email = request.email,password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user',response_model = List[schemas.Show_user],tags = ['Users'])
def show_user(db:Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user
@app.get('/user/{id}',response_model = schemas.Show_user,tags = ['Users'])
def user_id(id,response:Response,db:Session = Depends(get_db)):
    #blog = db.query(models.Blog).get(id)
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        #response.status_code = 404
        raise HTTPException(status_code = 404,detail = f'User with id {id} not found in database')
        #return {'details':f'Blog with id {id} not found in database'}
    
    return user