#!/usr/bin/env python3
# Lemoneval Project
# Author: Abhabongse Janthong <6845502+abhabongse@users.noreply.github.com>

import unittest
from lemoneval.assembled.standard.multiplechoices import FiveChoicesFramework
from lemoneval.backbones.sessions import Session
from lemoneval.utils.json import loads

##############################################
##  Unit tests: Framework Creations Errors  ##
##############################################

class Phase_CreationErrors(unittest.TestCase):

    def test_invalid_attributes(self):
        with self.assertRaisesRegex(TypeError,
                r"type 'int' for 'answer'"):
            FiveChoicesFramework(
                question="", choices=("", "", "", "", ""),
                answer="0"
                )
        with self.assertRaisesRegex(ValueError,
                r'index for correct answer'):
            FiveChoicesFramework(
                question="", choices=("", "", "", "", ""),
                answer=6
                )
        with self.assertRaisesRegex(TypeError,
                r"type 'int' for 'score'"):
            FiveChoicesFramework(
                question="", choices=("", "", "", "", ""),
                answer=0, score="10"
                )
        with self.assertRaisesRegex(TypeError,
                r"type 'int' for 'score'"):
            FiveChoicesFramework(
                question="", choices=("", "", "", "", ""),
                answer=0, score=5.5
                )
        with self.assertRaisesRegex(ValueError,
                r"failed MultipleChoicesFramework\.positive_score"):
            FiveChoicesFramework(
                question="", choices=("", "", "", "", ""),
                answer=0, score=-5
                )
        with self.assertRaisesRegex(TypeError,
                r"type 'str' for 'question'"):
            FiveChoicesFramework(
                question=100, choices=("", "", "", "", ""),
                answer=0
                )

############################################
##  Unit tests: After Framework Creation  ##
############################################

framework = FiveChoicesFramework(
    question="This is the question text",
    choices=("Choice A", "Choice B", "Choice C", "Choice D", "Choice E"),
    answer=0
)

class Phase_AfterFrameworkCreation(unittest.TestCase):

    def test_attributes(self):
        self.assertEqual(framework.question, "This is the question text")
        self.assertEqual(framework.choices[2], "Choice C")
        self.assertEqual(framework.answer, 0)
        self.assertEqual(framework.score, 10)

    def test_readonly(self):
        with self.assertRaises(AttributeError):
            framework.answer = 1

############################################################
##  Unit tests: After Session Creation and Serialization  ##
############################################################

session: Session = framework.create_session()
json_str = session.to_json()
new_session = loads(json_str)

class Phase_AfterSessionCreation(unittest.TestCase):

    def test_session(self):
        self.assertIs(session._framework, framework)
        self.assertFalse(session.has_started)
        self.assertFalse(session.has_finished)
        with self.assertRaises(AttributeError):
            session.public_data
        with self.assertRaises(AttributeError):
            session.summary_data

    def test_json_reciprocity(self):
        self.assertFalse(new_session.has_started)
        self.assertFalse(new_session.has_finished)
