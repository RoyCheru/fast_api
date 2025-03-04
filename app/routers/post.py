from .. import models, schemas, oath2
from fastapi import Depends,FastAPI, Response, status, HTTPException, APIRouter
from .. database import get_db
from sqlalchemy.orm import Session
from typing import Optional, List
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

#@router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()
    #you can add the function below based on the requirements of your app
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), get_current_user: int = 
                Depends(oath2.get_current_user), current_user: int = Depends(oath2.get_current_user)):
    #print(post)
    #post_dict = post.model_dump()
    #post_dict['id'] = randrange(0, 1000000)
    #my_posts.append(post_dict)
    
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    print(current_user.email)
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post
# title str, content str
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    #cursor.execute(""" SELECT * from posts WHERE id = %s""", (str(id)))
    #post = cursor.fetchone()
    #post = find_post(id)
    #post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with id {id} was not found"}
        
    # I have added the condition below so that you can only get your own posts. But you can change based on your app requirements
    
    #if post.owner_id != current_user.id:
        #raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorozed to perform requested action")
    return post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    #deleting post
    #find the index in the array that has the required id
    #my_posts.pop(index)
    
    #cursor.execute(""" DELETE FROM posts WHERE id= %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()
    
    #index = find_index_post(id)
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorozed to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oath2.get_current_user)):
    
    #cursor.execute(""" UPDATE posts SET title =%s, content=%s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #index = find_index_post(id)
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorozed to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    #post_dict = post.model_dump()
    #post_dict['id'] = id
    #print (post_dict)
    #my_posts[index] = post_dict
    #print(my_posts[index])
    return  post_query.first()
