from unittest.mock import MagicMock
import unittest
import root


class TestRoot(unittest.TestCase):

    def test_0_root(self):
        self.assertEqual(root.sqroots("1 2 1"), "-1.0")

    def test_1_root(self):
        self.assertEqual(root.sqroots("1 2 3"), "")

    def test_2_root(self):
        self.assertEqual(root.sqroots("1 2 -3"), "-3.0 1.0")

    def test_ZeroDivisionError_root(self):
        with self.assertRaises(ZeroDivisionError):
            root.sqroots("0 -1 -6")

    def test_ValueError_root(self):
        with self.assertRaises(ValueError):
            root.sqroots("-1 -6")

class TestSrvRoot(unittest.TestCase):

    def test_0_srv_root(self):
        self.assertEqual(root.sqroots("1 2 1"), "-1.0")

    def test_1_srv_root(self):
        self.assertEqual(root.sqroots("1 2 3"), "")

    def test_2_srv_root(self):
        self.assertEqual(root.sqroots("1 2 -3"), "-3.0 1.0")

    def test_ZeroDivisionError_srv_root(self):
        self.assertEqual(root.sqroots("0 -1 -6"), "")

    def test_ZeroDivisionError_srv_root(self):
        self.assertEqual(root.sqroots("-1 -6"), "")


class TestSrvRoot(unittest.TestCase):

    def setUp(self):
        self.mocker = MagicMock()
        self.mocker.sendall = lambda coeffs: setattr(self, "res", root.srv_sqroots(coeffs.decode()))
        self.mocker.recv = lambda args: self.res.encode()

    def test_0_srv_root(self):
        self.assertEqual(root.sqrootnet("1 2 1", self.mocker), "-1.0")

    def test_1_srv_root(self):
        self.assertEqual(root.sqrootnet("1 2 3", self.mocker), "")

    def test_2_srv_root(self):
        self.assertEqual(root.sqrootnet("1 2 -3", self.mocker), "-3.0 1.0")

    def test_ZeroDivisionError_srv_root(self):
        self.assertEqual(root.sqrootnet("0 -1 -6", self.mocker), "")

    def test_ValueError_srv_root(self):
        self.assertEqual(root.sqrootnet("-1 -6", self.mocker), "")

