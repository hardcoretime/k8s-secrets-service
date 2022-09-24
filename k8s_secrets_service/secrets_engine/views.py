from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from kubernetes.client import ApiException

from secrets_engine.k8s_client import K8sClient


def index(request):
    return render(request, 'secrets_engine/index.html')


# def login(request):
#     return render(request, 'secrets_engine/login.html')


# def create_secret(request, secret_name, secret_key, secret_value, namespace):
@login_required(login_url='login')
def create_secret(request):
    # k8s_client = K8sClient()
    #
    # try:
    #     k8s_client.add_secret(secret_name, secret_key, secret_value, namespace)
    # except ApiException as e:
    #     return render(request, 'secrets_engine/exception.html', context={'exception': e})

    # context = {
    #     'secret_name': secret_name,
    # }
    # return render(request, 'secrets_engine/create_secret.html', context=context)
    return render(request, 'secrets_engine/create_secret.html')
