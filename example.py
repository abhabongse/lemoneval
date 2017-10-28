# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from lemoneval.assembled.framework import FiveChoicesFramework
from lemoneval.backbone.session import Session

framework = FiveChoicesFramework(
    question="This is the question text",
    choices=("Choice A", "Choice B", "Choice C", "Choice D", "Choice E"),
    answer=0, score=10
)
session = framework.create_session()
print("session =", session)
jsontxt = session.to_json()
new_session = Session.from_json(
    jsontxt, dict(FiveChoicesFramework=FiveChoicesFramework)
)
print("new_session =", new_session)
