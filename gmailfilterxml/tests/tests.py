import os
import unittest
import datetime
from lxml.doctestcompare import LXMLOutputChecker
from doctest import Example
from gmailfilterxml.api import GmailFilterSet, GmailFilter
from gmailfilterxml.xmlschemas import Feed, Entry, EntryProperty


class XmlTest(unittest.TestCase):
    """http://stackoverflow.com/a/7060342"""
    def assertXmlEqual(self, got, want):
        checker = LXMLOutputChecker()
        if not checker.check_output(want, got, 0):
            message = checker.output_difference(Example("", want), got, 0)
            raise AssertionError(message)


class SingleFilterTest(XmlTest):
    def setUp(self):
        with open(os.path.join(os.path.dirname(__file__), 'single-filter.xml')) as f:
            self.expected_xml = f.read()

    def test_api(self):
        filter_set = GmailFilterSet(
            author_name='Danny Roberts',
            author_email='droberts@dimagi.com',
            updated_timestamp=datetime.datetime(2014, 9, 19, 17, 40, 28),
            filters=[
                GmailFilter(
                    id='1286460749536',
                    from_='noreply@github.com',
                    label='github',
                    should_archive=True,
                )
            ]
        )
        self.assertXmlEqual(filter_set.to_xml(), self.expected_xml)

    def test_schema(self):
        updated = datetime.datetime(2014, 9, 19, 17, 40, 28).strftime("%Y-%m-%dT%H:%M:%SZ")

        entries = [
            Entry(
                id='tag:mail.google.com,2008:filter:1286460749536',
                updated=updated,
                properties=[
                    EntryProperty(name='from', value='noreply@github.com'),
                    EntryProperty(name='label', value='github'),
                    EntryProperty(name='shouldArchive', value='true'),
                ]
            )
        ]
        feed = Feed(
            author_name='Danny Roberts',
            author_email='droberts@dimagi.com',
            updated=updated,
            id='tag:mail.google.com,2008:filters:1286460749536',
            entries=entries
        )
        self.assertXmlEqual(feed.serializeDocument(), self.expected_xml)


class FilterValidationTest(unittest.TestCase):
    def test(self):
        with self.assertRaises(TypeError):
            GmailFilter(id='1234567890123', xyz=123)
        with self.assertRaises(TypeError):
            GmailFilter(xyz=123)
        with self.assertRaises(AssertionError):
            GmailFilter(from_='github@dimagi.com')
        GmailFilter(id='1234567890123', from_='github@dimagi.com')