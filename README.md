# k8s-secrets-service

## install
### linux(debian)

#### virtualbox
```shell
echo "deb http://deb.debian.org/debian/ sid main contrib non-free" >> /etc/apt/sources.list
sudo apt update
sudo apt install virtualbox
```

#### kubectl
```shell
sudo apt-get update && sudo apt-get install -y apt-transport-https
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee -a /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubectl
```

#### minikube
```shell
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 \
  && chmod +x minikube
sudo mkdir -p /usr/local/bin/
sudo install minikube /usr/local/bin/
minikube start
```

#### migrations
```shell
python k8s_secrets_service/manage.py makemigrations
python k8s_secrets_service/manage.py migrate
```

#### create superuser
```shell
python k8s_secrets_service/manage.py createsuperuser
```

#### docker image build
```shell
minikube image build -f docker/Dockerfile -t k8s-secrets-service:latest .
```

#### kubernetes manifests(don't forget put SECRET_KEY to .env file)
```shell
kubectl apply -f kubernetes/namespace.yaml
source .env
SECRET_KEY=$(echo ${SECRET_KEY} | base64) envsubst < kubernetes/secret.yaml | kubectl apply -f -
kubectl apply -f kubernetes/role.yaml
kubectl apply -f kubernetes/rolebinding.yaml
kubectl apply -f kubernetes/serviceaccount.yaml
kubectl apply -f kubernetes/deployment.yaml
```

#### pod port forward
```shell
POD_NAME=$(kubectl get pod -n development -l app=k8s-secrets-service -o name)
kubeclt port-forward -n development ${POD_NAME} 8000:8000
```

## Usage
[Main page](http://0.0.0.0:8000/index/)

#### create developer account by superuser(also you can use superuser to create a kubernetes secret)
[Admin page](http://0.0.0.0:8000/admin/)


#### create demo-secret
[Create kubernetes secret](http://0.0.0.0:8000/create-secret/)
- secret name: demo-secret
- secret key: demo-key
- secret value: demo-value
- namespace: development

#### create demo-deployment with demo-secret
```shell
kubectl apply kubernetes/demo-deployment
```

#### check demo-secret value in the demo-pod env(output must be "DEMO_SECRET=demo-value")
```shell
DEMO_POD_NAME=$(kubectl get pod -n development -l app=demo-deployment -o name)
kubectl exec -n development ${DEMO_POD_NAME} -- env | grep DEMO_SECRET
```