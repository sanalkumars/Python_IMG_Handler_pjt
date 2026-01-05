from fastapi import FastAPI,HTTPException
import uvicorn
from app.schema import Post

app =  FastAPI()

posts = [
    {
        "userId": 1,
        "id": 1,
        "title": "sunt aut facere repellat provident occaecati excepturi optio reprehenderit",
        "body": "quia et suscipit\nsuscipit recusandae consequuntur expedita et cum\nreprehenderit molestiae ut ut quas totam\nnostrum rerum est autem sunt rem eveniet architecto"
    },
    {
        "userId": 1,
        "id": 2,
        "title": "qui est esse",
        "body": "est rerum tempore vitae\nsequi sint nihil reprehenderit dolor beatae ea dolores neque\nfugiat blanditiis voluptate porro vel nihil molestiae ut reiciendis\nqui aperiam non debitis possimus qui neque nisi nulla"
    },
      {
    "userId": 2,
    "id": 12,
    "title": "in quibusdam tempore odit est dolorem",
    "body": "itaque id aut magnam\npraesentium quia et ea odit et ea voluptas et\nsapiente quia nihil amet occaecati quia id voluptatem\nincidunt ea est distinctio odio"
  },
  {
    "userId": 2,
    "id": 13,
    "title": "dolorum ut in voluptas mollitia et saepe quo animi",
    "body": "aut dicta possimus sint mollitia voluptas commodi quo doloremque\niste corrupti reiciendis voluptatem eius rerum\nsit cumque quod eligendi laborum minima\nperferendis recusandae assumenda consectetur porro architecto ipsum ipsam"
  }
]



@app.get("/posts")
async def get_all_posts(userId:int = None):
    if userId is None:
        return posts
    # post_by_user = next((p for p in posts if p["userId"] == userId),None) #this will return only one dictionary even if there are multiple data for the specific end point
    post_by_user = [p for p in posts if p["userId"] == userId] # here this gets all the matching data as a list of dictionary
    if not  post_by_user :
        raise HTTPException(status_code = 404,detail="Post not found")
    return post_by_user


@app.get("/post/{id}")
async def get_post_by_id(id:int):
    for post in posts:
        if(post["id"] == id):
            return post
    raise HTTPException(status_code=404, detail="Post not found")

# next learning post 

@app.post("/post",status_code =201)
async def create_new_poast(new_post : Post):
    post_dic = new_post.model_dump()

    if any(p['id'] == post_dic["id"] for p in posts):
        raise HTTPException(status_code =409,detail="Post already exists")
    posts.append(post_dic)
    return post_dic
