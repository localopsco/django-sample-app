### To push docker image

```shell
docker build -t todo-web .
```

```shell
docker tag todo-web:latest public.ecr.aws/x1e8o8e1/django-sample-app:latest
```

```shell
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/x1e8o8e1
```

```shell
docker push public.ecr.aws/x1e8o8e1/django-sample-app:latest
```

### To helm install

```shell
helm install todo ./helm
```
