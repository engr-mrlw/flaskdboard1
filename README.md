# flaskdboard1

Backend:

pip install flask flask-cors requests

python app.py


(base)  [backend ] --> $  python app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://192.168.0.4:8000
Press CTRL+C to quit
 * Restarting with watchdog (windowsapi)
 * Debugger is active!
 * Debugger PIN: 100-801-270

Test:
http://localhost:8000/api/token

http://localhost:8000/api/products

Test Search:
http://localhost:8000/api/products?q=phone

http://localhost:8000/api/users

http://localhost:8000/api/dashboard

Swagger:

pip install flasgger

http://localhost:8000/apidocs


Frontend:

npm create vite@latest frontend -- --template react

npm install

npm install axios chart.js react-chartjs-2

npm run dev

(base)  [frontend ] --> $  npm run dev

> frontend@0.0.0 dev
> vite

Port 5173 is in use, trying another one...

  VITE v8.0.10  ready in 593 ms

  ➜  Local:   http://localhost:5174/
  ➜  Network: use --host to expose


Test the connection
In your browser console:

fetch("http://localhost:8000/api/token")
  .then(r => r.json())
  .then(console.log)


git commands:
git --version
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

git init # Start a new repository
git clone <repo_url> # Clone an existing repository

git status # View file states
git add <file> # Stage a file
git add . # Stage all changes
git commit -m "Message" # Commit staged changes

git push origin <branch> # Push commits to remote
git pull # Fetch and merge from remote

git branch # List branches
git checkout -b <branch> # Create & switch to new branch
git merge <branch> # Merge into current branch
git branch -d <branch> # Delete branch

git checkout -- <file> # Discard changes in file
git reset --hard HEAD # Reset to last commit

git tag v1.0.0 # Create a tag
git push --tags # Push tags to remote

https://copilot.microsoft.com/shares/RTWeHb2RM4PcefoC4xMST