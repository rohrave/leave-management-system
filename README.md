# Leave Management System (V1, V2, V3)

## Versions
- V1: Apply for leave
- V2: Apply for leave + approve pending requests
- V3: Apply for leave + approve + reject pending requests

## Run locally (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```
Open http://localhost:5000.

## Important demo limitation
This educational sample stores requests in process memory. Data is not persistent and is not shared between the three versions or multiple replicas. Use a database and authentication for a real deployment.

## Build Docker images
Check out each version branch before building:
```powershell
docker build -t YOUR_DOCKERHUB_USERNAME/leave-system:v1 .
docker build -t YOUR_DOCKERHUB_USERNAME/leave-system:v2 .
docker build -t YOUR_DOCKERHUB_USERNAME/leave-system:v3 .
```
Only tag the matching source version with each tag.

## Kubernetes
Replace YOUR_DOCKERHUB_USERNAME in the manifests, then apply them:
```powershell
kubectl apply -f k8s/v1-deployment.yaml
kubectl apply -f k8s/v1-service.yaml
kubectl apply -f k8s/v2-deployment.yaml
kubectl apply -f k8s/v2-service.yaml
kubectl apply -f k8s/v3-deployment.yaml
kubectl apply -f k8s/v3-service.yaml
```
Run each port-forward command in a separate terminal:
```powershell
kubectl port-forward service/leave-v1-service 5001:5000
kubectl port-forward service/leave-v2-service 5002:5000
kubectl port-forward service/leave-v3-service 5003:5000
```

## Jenkins notes
The Jenkinsfile assumes a Linux agent with Python, Docker CLI/daemon access, and kubectl configured for the target cluster. Configure a Jenkins username/password credential with ID `dockerhub-creds` and store your Docker Hub username and access token. Update the image name in Jenkinsfile. Build the matching Git branch for each version.
