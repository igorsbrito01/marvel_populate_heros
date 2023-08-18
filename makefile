docker_build_task:
	@docker-compose build task

docker_create_database_tables:
	@docker-compose up init_database

run_database:
	@docker-compose up -d db

run_task:
	@docker-compose up task

run_custom:
	@docker-compose up task_custom
