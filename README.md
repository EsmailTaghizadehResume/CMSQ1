# CMSQ1

if you have small shop and need to use a content system for your shop you need a patform to interduce your product and and making a link and QR code for that and manage system for for add remove and edit it for you in this project we use and create this to solve your problem

# In V 1.0.3

- product manager
- QR code creator system
- admin panel
- no regestration

# Error in V 1.0.3

`CMSQ-v1.0.3/env/lib/python3.12/site-packages/flask_uploads.py` and modify the import statement:

Replace:

```python
from werkzeug import secure_filename, FileStorage
```

With:

```python
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
```

However, do note that modifying library code is generally not recommended as it might lead to issues when you update the library in the future.
