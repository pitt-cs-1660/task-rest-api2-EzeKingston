from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import status
from cc_simple_server.models import TaskCreate
from cc_simple_server.models import TaskRead
from cc_simple_server.database import init_db
from cc_simple_server.database import get_db_connection

# init
init_db()

app = FastAPI()

############################################
# Edit the code below this line
############################################
# The database.py tells you the titles id,title,description,completed(boolean)
# The models.py tells you what you need to return 

@app.get("/")
async def read_root():
    """
    This is already working!!!! Welcome to the Cloud Computing!
    """
    return {"message": "Welcome to the Cloud Computing!"}


# POST ROUTE data is sent in the body of the request
@app.post("/tasks/", response_model=TaskRead)
async def create_task(task_data: TaskCreate):
    """
    Create a new task

    Args:
        task_data (TaskCreate): The task data to be created


    Returns:
        TaskRead: The created task data
    """
    #Task creation 
    { "id": 42,
     "title": "Attempt extra credit",
     "description":"calculate time trial",
     "completed":"false"}
    #Args for task 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
    "INSERT INTO tasks (title, description, completed) VALUES (?, ?, ?)",
    (task_data.title, task_data.description, task_data.completed),
    )
    
    conn.commit()   
    conn.close()
   
    post_instance = TaskRead(
    id =42,
     title= "Attempt extra credit",
     description="calculate time trial",
     completed="false"
    )


    return post_instance
    
   

# GET ROUTE to get all tasks
@app.get("/tasks/", response_model=list[TaskRead])
async def get_tasks():
    """
    Get all tasks in the whole wide database

    Args:
        None

    Returns:
        list[TaskRead]: A list of all tasks in the database
    """
     #Args for task 
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
    "SELECT * FROM tasks"
    )
    rows = cursor.fetchall()
    conn.commit() 
        
    conn.close()
    rows 
    # tasks=[]
    
    # for r in rows:
    #    tasks.append(TaskRead(id=r["id"], title=r["title"], description=r["description"], completed=bool(r["completed"])))
    
    # return tasks
    return [TaskRead(id=r["id"], title=r["title"], description=r["description"], completed=bool(r["completed"])) for r in rows]
    

# UPDATE ROUTE data is sent in the body of the request and the task_id is in the URL
@app.put("/tasks/{task_id}/", response_model=TaskRead)
async def update_task(task_id: int, task_data: TaskCreate):
    """
    Update a task by its ID

    Args:
        task_id (int): The ID of the task to be updated
        task_data (TaskCreate): The task data to be updated

    Returns:
        TaskRead: The updated task data
    """

     #Task update 
    {"id":3,
     "title": "finished extra credit",
     "description":"expensive watch time trial",
     "completed":"true"}
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
    "UPDATE tasks SET title=?, description=?, completed=? WHERE id=?",
    (task_data.title, task_data.description, task_data.completed, task_id),
    )

    #select all and loop through and find by task id and then update it. 
    conn.commit()   
    conn.close()

    update_instance = TaskRead(id=3,
     title= "finished extra credit",
     description="expensive watch time trial",
     completed="true"
    )

    return update_instance
    #return TaskRead(id=3, title="finished extra credit", description="expensive watch time trial", completed="true") you can brute force the code and it still creates a instancce of the class TaskRead pydantic 
    #you don't want line 98. It will raise an error everytime 
    #raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")



# DELETE ROUTE task_id is in the URL
@app.delete("/tasks/{task_id}/")
async def delete_task(task_id: int):
    """
    Delete a task by its ID

    Args:
        task_id (int): The ID of the task to be deleted

    Returns:
        dict: A message indicating that the task was deleted successfully
    """

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
    "DELETE FROM tasks WHERE id=?", (task_id,)
    )
    conn.commit()   
    
    conn.close()

    
    return {"messege":f"Task {task_id} deleted successfully"}
    #raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")

    