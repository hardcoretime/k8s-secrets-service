from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from kubernetes.client import ApiException

from secrets_engine.k8s_client import K8sClient


def index(request):
    return render(request, 'secrets_engine/index.html')


@login_required(login_url='login')
def create_secret(request):
    k8s_client = K8sClient()

    if request.method == 'POST':
        secret_name = request.POST.get('secret_name')
        secret_key = request.POST.get('secret_key')
        secret_value = request.POST.get('secret_value')
        namespace = request.POST.get('namespace')
        try:
            k8s_client.add_secret(secret_name, secret_key, secret_value, namespace)
            return render(request, 'secrets_engine/secret_detail.html', context={'secret_name': secret_name})
        except ApiException as e:
            return render(request, 'secrets_engine/exception.html', context={'exception': e})

    return render(request, 'secrets_engine/create_secret.html')


def list_secrets(request):
    k8s_client = K8sClient()

    if request.method == 'POST':
        namespace = request.POST.get('namespace')
        try:
            secrets = k8s_client.list_secrets(namespace).items
            context = {
                'namespace': namespace,
                'secrets': secrets,
            }
            return render(request, 'secrets_engine/secrets_list.html', context=context)
        except ApiException as e:
            return render(request, 'secrets_engine/exception.html', context={'exception': e})

    return render(request, 'secrets_engine/get_secrets.html')
