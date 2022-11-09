### Requirements

See requirements.txt

For install use:
`pip3 install -r requirements.txt`

### Tests

See `test_selenium_rtk.py`

### Settings
See credentials in the file `settings.py`
File contains correct credentials for one user, uses in tests.

### Before run

Set your own settings for parameters `phone_number`, `email` and `password` in `settings.py`.

If you are using Chrome version 106, you can use chromedriver in a project.
If you use another version chrome or another browser, you must:
- change the path to the file __./chromedriver.exe__ to driver file path on your PC in __test_selenium_petfriends.py__.

Or

- put your driver in the project root folder nearby/instead __chromedriver.exe__.

Make sure that you run python scripts under administration rights.