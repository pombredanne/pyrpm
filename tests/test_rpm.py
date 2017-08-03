from io import BytesIO
import unittest
import sys

try:
    # py2
    string_type = unicode
except NameError:
    # py3
    string_type = str

from pyrpm.rpm import RPM


class RPMTest(unittest.TestCase):

    def setUp(self):
        self.rpm = RPM(open('tests/Eterm-0.9.3-5mdv2007.0.src.rpm', 'rb'))

    def tearDown(self):
        self.rpm.rpmfile.close()

    def test_entries(self):

        description = '''Eterm is a color vt102 terminal emulator intended as a replacement for Xterm.\nIt is designed with a Freedom of Choice philosophy, leaving as much power,\nflexibility, and freedom as possible in the hands of the user.\n\nIt is designed to look good and work well, but takes a feature-rich approach\nrather than one of minimalism while still maintaining speed and efficiency.\n\nIt works on any windowmanager/desktop environment, although it is designed\nto work and integrate best with Enlightenment.'''

        self.assertEqual(self.rpm.header.name, 'Eterm')
        self.assertEqual(self.rpm.header.version, '0.9.3')
        self.assertEqual(self.rpm.header.release, '5mdv2007.0')
        self.assertEqual(self.rpm.header.architecture, 'i586')
        self.assertEqual(self.rpm.header.license, 'BSD')
        self.assertEqual(self.rpm.header.description, description)

    def test_package_type(self):
        self.assertEqual(self.rpm.binary, False)
        self.assertEqual(self.rpm.source, True)

    def test_filename(self):
        self.assertEqual(self.rpm.canonical_filename, 'Eterm-0.9.3-5mdv2007.0.src.rpm')


class RPMLatin1Test(unittest.TestCase):

    def setUp(self):
        self.rpm = RPM(open('tests/compat-libcap1-1.10-7.el7.x86_64.rpm', 'rb'))

    def tearDown(self):
        self.rpm.rpmfile.close()

    def test_entries(self):
        self.assertEqual(self.rpm.header.name, 'compat-libcap1')
        self.assertEqual(self.rpm.header.version, '1.10')
        self.assertEqual(self.rpm.header.release, '7.el7')
        self.assertEqual(self.rpm.header.architecture, 'x86_64')
        self.assertEqual(self.rpm.header.license, 'BSD-like and LGPL')

    def test_package_type(self):
        self.assertEqual(self.rpm.binary, True)
        self.assertEqual(self.rpm.source, False)

    def test_filename(self):
        self.assertEqual(self.rpm.canonical_filename, 'compat-libcap1-1.10-7.el7.x86_64.rpm')

    def test_changelog(self):
        for entry in self.rpm.changelog:
            self.assertEqual(type(entry.name), string_type)


class RPMStringIOTest(RPMTest):

    def setUp(self):
        with open('tests/Eterm-0.9.3-5mdv2007.0.src.rpm', 'rb') as f:
            data = f.read()
        self.rpm = RPM(BytesIO(data))
