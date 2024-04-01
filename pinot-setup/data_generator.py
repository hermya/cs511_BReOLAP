import datetime
import uuid
import random
import json

while True:
    ts = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    id = str(uuid.uuid4())
    count = random.randint(0, 1000)
    print(
        json.dumps({"ts": ts, "uuid": id, "count": count})
    )
