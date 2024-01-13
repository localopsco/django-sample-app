### To push docker image

```shell
docker buildx build --platform linux/amd64 -t todo-web:latest -t todo-web:<version> .
```

```shell
docker tag todo-web:latest public.ecr.aws/x1e8o8e1/django-sample-app:latest
docker tag todo-web:<version> public.ecr.aws/x1e8o8e1/django-sample-app:<version>
```

```shell
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/x1e8o8e1
```

```shell
docker push public.ecr.aws/x1e8o8e1/django-sample-app:latest
docker push public.ecr.aws/x1e8o8e1/django-sample-app:<version>
```

### To helm install

```shell
helm install todo ./helm
```

### To push new helm version

```shell
helm package helm -d helm/.tmp/
```

```shell
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/x1e8o8e1
```

```shell
helm push helm/.tmp/django-sample-app-helm-0.1.0.tgz oci://public.ecr.aws/x1e8o8e1/
```
