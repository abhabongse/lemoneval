# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from lemoneval.assembled.framework import FiveChoicesFramework
from lemoneval.backbone.session import Session

framework = FiveChoicesFramework(
    question="This is the question text",
    choices=("Choice A", "Choice B", "Choice C", "Choice D", "Choice E"),
    answer=0, score=10
)
session = iter(framework)  # type: Session
print("session 01 =", session)

# Fetch data and display
public_data = next(session)
print("session 02 =", session)
print(public_data)

# Save session in JSON string
json_str = session.to_json()

# Obtain answer of choice
choose = int(input("You choose: "))

# Load session from JSON string
new_session = Session.from_json(json_str)
print("session 03 =", new_session)

# Submit the choosing
try:
    new_session.submit(dict(choose=choose))
except StopIteration:
    print("session 04 =", new_session)

# Display result
print(new_session.report)

# jsontxt = session.to_json()
# print("jsontxt =", jsontxt)
# new_session = Session.from_json(jsontxt)
# print("new_session =", new_session)
#
# next(session)
# print("session =", session)
# jsontxt = session.to_json()
# print("jsontxt =", jsontxt)
# new_session = Session.from_json(jsontxt)
# print("new_session =", new_session)
