init:
	pip install django

test: init
	python test_dj_log_config_helper.py
