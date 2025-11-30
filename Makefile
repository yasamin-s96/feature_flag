.PHONY: i18n-extract i18n-init-en i18n-init-fa i18n-update i18n-compile excel-from-log dev-setup generate-models

i18n-extract:
	poetry run pybabel extract -F babel.cfg -o i18n/messages.pot .

i18n-init-en:
	poetry run pybabel init -i i18n/messages.pot -d i18n/translations -l en

i18n-init-fa:
	poetry run pybabel init -i i18n/messages.pot -d i18n/translations -l fa

i18n-update:
	poetry run pybabel update -i i18n/messages.pot -d i18n/translations --previous --no-fuzzy-matching

i18n-compile:
	poetry run pybabel compile -d i18n/translations

excel-from-log:
	poetry run python core/utils/log_to_excel.py

generate-models:
	poetry run python scripts/generate_models.py
	poetry run python scripts/models_separator.py

dev-setup:
	sudo curl -L "https://tools.admin.dornicafile.ir/dornica-co.local.crt" -o /usr/local/share/ca-certificates/dornica-co.local.crt
	poetry config certificates.nexus-pypi.cert /usr/local/share/ca-certificates/dornica-co.local.crt
	poetry source add --priority=explicit nexus-pypi https://nexus.dornica-co.local/repository/pypi/simple
	poetry install --no-root