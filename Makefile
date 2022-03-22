#setup:	@ set up all requirements
setup.env: setup.pip setup.poetry

#setup.pip:	@ set up pip and poetry
setup.pip:
	pip install --upgrade pip
	pip install poetry --extra-index-url https://www.piwheels.org/simple

#setup.poetry:	@ set up poetry dependencies
setup.poetry:
	poetry config virtualenvs.create true
	poetry config virtualenvs.in-project true
	poetry install --no-interaction --no-ansi
#
#setup.elastic:
#	#docker network create elastic
#	docker pull docker.elastic.co/elasticsearch/elasticsearch:7.14.0
#	docker run --name es01-test \
#		--net elastic \
#		-p 9200:9200 \
#		-p 9300:9300 \
#		-e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.14.0
#
#setup.kibana:
#	docker pull docker.elastic.co/kibana/kibana:7.14.0
#	docker run --name kib01-test \
#			   --net elastic \
#   			   -p 5601:5601 \
#   			   -e "ELASTICSEARCH_HOSTS=http://localhost:9200" docker.elastic.co/kibana/kibana:7.14.0
#
#setup.ent-search:
#	docker pull docker.elastic.co/enterprise-search/enterprise-search:7.14.0
#	docker run --name ent-search \
#		  -p 3002:3002 \
#		  -e "elasticsearch.host=http://localhost:9200" \
#		  -e "secret_management.encryption_keys=[bf778c6b86a5d165df8746873f1ee8160e434e303dbed906886ae43d62c4a93d]" \
#		  -e "allow_es_settings_modification=true" docker.elastic.co/enterprise-search/enterprise-search:7.14.0
