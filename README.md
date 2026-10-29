# Help Desk Ticket System

- v1: Raise Issue
- v2: Display Tickets
- v3: Resolve/Close Issue

## Run on Windows PowerShell
From this project folder:
```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:APP_VERSION = "v1"
.\.venv\Scripts\python.exe app.py
```
Open http://localhost:5000/raise. Stop with Ctrl+C. Use APP_VERSION "v2" and visit /tickets, or "v3" and visit /resolve.

## Note
This starter uses in-memory tickets. Data is lost on restart and is not shared between separate versions. A shared database is needed for persistence.

## GitHub
Create an empty repository, then replace YOUR_USERNAME:
```bash
git init
git add .
git commit -m "Initial Help Desk system"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/help-desk-system.git
git push -u origin main
```
Create version branches and make version-specific commits.

## Docker
Replace YOUR_DOCKERHUB_USERNAME in Jenkinsfile and k8s manifests.
```bash
docker build -t YOUR_DOCKERHUB_USERNAME/help-desk-system:v1 .
docker build -t YOUR_DOCKERHUB_USERNAME/help-desk-system:v2 .
docker build -t YOUR_DOCKERHUB_USERNAME/help-desk-system:v3 .
docker login
docker push YOUR_DOCKERHUB_USERNAME/help-desk-system:v1
docker push YOUR_DOCKERHUB_USERNAME/help-desk-system:v2
docker push YOUR_DOCKERHUB_USERNAME/help-desk-system:v3
```
For local containers, use APP_VERSION and ports 5001, 5002, 5003.

## Kubernetes
Enable Docker Desktop Kubernetes or start Minikube. Replace Docker Hub username in manifests:
```bash
kubectl apply -f k8s/
kubectl get deployments
kubectl get pods
kubectl get services
```
Port forward in separate terminals:
```bash
kubectl port-forward service/helpdesk-v1-service 5001:5000
kubectl port-forward service/helpdesk-v2-service 5002:5000
kubectl port-forward service/helpdesk-v3-service 5003:5000
```
Visit localhost:5001/raise, localhost:5002/tickets, localhost:5003/resolve.

## Jenkins
Jenkinsfile assumes a Linux agent with Python, Docker CLI/daemon, kubectl, and Kubernetes credentials configured. Add Docker Hub username/token as credential ID dockerhub-creds. The checked-out branch must match the selected version.
