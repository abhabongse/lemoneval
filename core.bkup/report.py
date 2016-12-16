# Lemoneval Project
# Author: Abhabongse Janthong <abhabongse@gmail.com>
import operator
import os.path


class Reporter(object):
    """
    Reports are generated messages from the program evaluation. It provides
    and interface to write messages from each test and combine all result so
    that it could be exported in various formats.
    """
    def __init__(self):
        self._subreports = []
        self._factory = lambda: Reporter()
        self.message = ''

    def subreport(self):
        """
        Create a new subreport and return that subreport to be used nestedly.
        """
        subreport = self._factory()
        self._subreports.append(subreport)
        return subreport

    def write(self, message, append=False):
        """
        Write a message report.
        """
        if append:
            self.message += str(message)
        else:
            self.message = str(message)

    def export(self, writer, *args, **kwargs):
        """
        Flatten the report structure and generate the report. To be implememted
        by subclasses.
        """
        raise NotImplementedError


class StringReporter(Reporter):
    """
    String-based reporter, using indentations to group test structures.
    """
    def __init__(self, indent='\t'):
        super().__init__()
        self._factory = lambda: StringReporter(indent=indent)
        self.indent = indent

    def export(self, writer, num_indents=0):
        """
        Make a call to writer with the message to write.
        """
        writer('{}{}\n'.format(self.indent * num_indents, self.message))
        for subreport in self._subreports:
            subreport.export(writer, num_indents=num_indents+1)

    def export_file(self, fileobj):
        """
        Write the report to the given file object.
        """
        def _write_to_file(message):
            print(message, file=fileobj, end='')
        self.export(_write_to_file)

    def export_string(self):
        """
        Return the flattened message.
        """
        messages = []
        self.export(messages.append)
        return ''.join(messages)
