To INstall dependencies
(fastapivenv) PS C:\Naga\Learning\pythonprojects\fastapi-app> pip install -r requirements.txt

http://localhost:8000/
http://localhost:8000/docs
http://localhost:8000/redoc

To run
(fastapivenv) PS C:\Naga\Learning\pythonprojects\fastapi-app> python main.py
OR
uvicorn main:app --reload

with auth enabled
openssl rand -hex 32
uvicorn mainwithauth:app --reload

Topics Covered : 
1. FAST API
2. Pickle Serialization and Deserialization
3. Adding Middleware to FASTAPI app
4. JWT Auth Enabled
5. Hashing
6. JWT Encode and Decode 

