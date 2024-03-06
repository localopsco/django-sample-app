ECR_REPO = public.ecr.aws/r5p6q2u1
APP_NAME = django-sample-app

push-app:
	docker buildx build --platform linux/amd64 -t todo-web:latest -t todo-web:${version} .
	docker tag todo-web:latest ${ECR_REPO}/${APP_NAME}:latest
	docker tag todo-web:${version} ${ECR_REPO}/${APP_NAME}:${version}
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_REPO}
	docker push ${ECR_REPO}/${APP_NAME}:latest
	docker push ${ECR_REPO}/${APP_NAME}:${version}

push-helm-app:
	helm package helm -d helm/.tmp/
	aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${ECR_REPO}
	helm push helm/.tmp/django-sample-app-helm-${version}.tgz oci://${ECR_REPO}/
	helm registry logout public.ecr.aws

