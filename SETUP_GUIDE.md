# Setup guide: Leave System

This ZIP contains the complete V3 application plus Docker, Jenkins, tests, and Kubernetes files.

## Important: create version-specific source code
The `app.py` in this ZIP is the complete V3 application. Before publishing each image, make the source code match its version:
- V1: keep homepage and `/apply`; remove `/approve`, `/approve/<id>`, `/reject/<id>` routes. Remove the Review requests link from `templates/index.html`.
- V2: retain V1 and `/approve` plus `/approve/<id>`; remove `/reject/<id>` route and reject form from `templates/approve.html`.
- V3: use all included code.
Commit each version to its own branch before building that version's Docker image. This avoids incorrectly tagging V3 code as V1 or V2.

## Local run (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe app.py
```
Open http://localhost:5000. Press Ctrl+C to stop.

## GitHub
Create an empty GitHub repository named `leave-system`, then:
```powershell
git init
git branch -M main
git add .
git commit -m "Add initial leave system"
git remote add origin https://github.com/YOUR_USERNAME/leave-system.git
git push -u origin main
```
Create the version branches and commit version-specific changes separately.

## Docker
Replace `YOUR_DOCKERHUB_USERNAME` in `Jenkinsfile` and all Kubernetes deployment YAML files. Build from the matching branch:
```powershell
docker build -t YOUR_DOCKERHUB_USERNAME/leave-system:v1 .
docker build -t YOUR_DOCKERHUB_USERNAME/leave-system:v2 .
docker build -t YOUR_DOCKERHUB_USERNAME/leave-system:v3 .
```
Login and push:
```powershell
docker login
docker push YOUR_DOCKERHUB_USERNAME/leave-system:v1
docker push YOUR_DOCKERHUB_USERNAME/leave-system:v2
docker push YOUR_DOCKERHUB_USERNAME/leave-system:v3
```

## Kubernetes
Make sure kubectl points to your local cluster and images are public or image-pull credentials are configured:
```powershell
kubectl apply -f k8s/v1-deployment.yaml
kubectl apply -f k8s/v1-service.yaml
kubectl apply -f k8s/v2-deployment.yaml
kubectl apply -f k8s/v2-service.yaml
kubectl apply -f k8s/v3-deployment.yaml
kubectl apply -f k8s/v3-service.yaml
kubectl get deployments,pods,services
```
Run each port-forward in a separate terminal:
```powershell
kubectl port-forward service/leave-v1-service 5001:5000
kubectl port-forward service/leave-v2-service 5002:5000
kubectl port-forward service/leave-v3-service 5003:5000
```
URLs: http://localhost:5001, http://localhost:5002, http://localhost:5003.

## Jenkins
The included Jenkinsfile uses `sh`, so use a Linux Jenkins agent with Python, Docker CLI/daemon access, and kubectl configured. Add a Jenkins username/password credential with ID `dockerhub-creds`; use a Docker Hub access token as the password. Set the correct Git branch for each version. For a multibranch pipeline, configure branch-to-version mapping so the chosen source branch and image tag match.

## Limitations
This is an educational sample. It uses in-memory storage, has no login/authorization, and does not persist data across restarts or replicas. Use a database, authentication, authorization, CSRF protection, and persistent/shared storage before real use.
