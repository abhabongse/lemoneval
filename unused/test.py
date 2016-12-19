# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>

from lemoneval.core.report import StringReporter
from lemoneval.example.add1 import config as add1

reporter = StringReporter()
testconfig = add1.DefaultTestConfiguration('.')
score = testconfig.post_submit('', reporter)

print(score)
print(reporter.export_string())
with open('tmp.log', 'w') as f:
    reporter.export_file(f)

score = testconfig.post_submit('')
print(score)
