TITLE 'test suite'
ECHO OFF
echo
python ./tests/configuration_test.py
python ./tests/generators_test.py
python ./tests/masher_test.py
python ./tests/parsing_rules_test.py
python ./tests/parsing_test.py
python -c "input('press enter to exit.')"