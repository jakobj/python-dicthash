# -*- coding: utf-8 -*-
"""
Unit and integration tests for the dicthash.dicthash module

"""

import unittest
import numpy as np

from .. import dicthash


class DictHashTest(unittest.TestCase):

    def test_fails_with_non_dict(self):
        self.assertRaises(AssertionError, dicthash.generate_hash_from_dict, 2)

    def test_same_value_for_same_dict(self):
        d0 = {
            'a': [1, 2, 3],
            'b': 'asd',
            'c': 1.2,
        }
        d1 = {
            'a': [1, 2, 3],
            'b': 'asd',
            'c': 1.2,
        }

        hash0 = dicthash.generate_hash_from_dict(d0)
        hash1 = dicthash.generate_hash_from_dict(d1)

        self.assertEqual(hash0, hash1)

    def test_different_value_for_different_dict(self):
        d0 = {
            'a': [1, 2, 3],
            'b': 'asd',
            'c': 1.2,
        }
        d1 = {
            'a': [1, 2, 5],
            'b': 'asd',
            'c': 1.2,
        }

        hash0 = dicthash.generate_hash_from_dict(d0)
        hash1 = dicthash.generate_hash_from_dict(d1)

        self.assertNotEqual(hash0, hash1)

    def test_nested_dictionary(self):
        d0 = {
            'a': {
                'a0': [1, 2, 3],
                'a1': 'asd',
                'a2': 1.2,
            },
            'b': {
                'a0': [1, 2, 3],
                'a1': 'asd',
                'a2': 1.2,
            }
        }

        dicthash.generate_hash_from_dict(d0)

    def test_nested_lists(self):
        d0 = {
            'a': [[1, 2, 3], [4, 5, 6]],
            'b': 'asd',
            'c': 1.2,
        }
        dicthash.generate_hash_from_dict(d0)

    def test_nested_numpy_arrays(self):
        d0 = {
            'a': np.array([[1, 2, 3], [4, 5, 6]]),
            'b': 'asd',
            'c': 1.2,
        }
        dicthash.generate_hash_from_dict(d0)

    def test_integer_keys(self):
        d0 = {
            0: [1, 2, 3],
            1: 'asd',
            2: 1.2,
        }
        dicthash.generate_hash_from_dict(d0)

    def test_blacklist(self):
        d0 = {
            'a': [1, 2, 3],
            'b': 'asd',
            'c': 1.2,
            'd': 123,
        }
        d1 = {
            'a': [1, 2, 3],
            'b': 'asd',
            'c': 1.2,
            'e': 'xyz',
        }

        hash0 = dicthash.generate_hash_from_dict(d0, blacklist=['d'])
        hash1 = dicthash.generate_hash_from_dict(d1, blacklist=['e'])

        self.assertEqual(hash0, hash1)

        hash0 = dicthash.generate_hash_from_dict(d0, blacklist=['a'])
        hash1 = dicthash.generate_hash_from_dict(d1, blacklist=['e'])

        self.assertNotEqual(hash0, hash1)

    def test_whitelist(self):
        d0 = {
            'a': [1, 2, 3],
            'b': 'asd',
            'c': 1.2,
            'd': 123,
        }
        d1 = {
            'a': [1, 2, 3],
            'b': 'asd',
            'c': 1.2,
            'e': 'xyz',
        }

        hash0 = dicthash.generate_hash_from_dict(d0, whitelist=['a', 'b', 'c'])
        hash1 = dicthash.generate_hash_from_dict(d1, whitelist=['a', 'b', 'c'])

        self.assertEqual(hash0, hash1)

        hash0 = dicthash.generate_hash_from_dict(d0, whitelist=['a', 'b', 'd'])
        hash1 = dicthash.generate_hash_from_dict(d1, whitelist=['a', 'b', 'c'])

        self.assertNotEqual(hash0, hash1)

    def test_invalid_blackwhitelist_raises_error(self):
        d0 = {
            'a': 5,
        }
        self.assertRaises(KeyError, dicthash.generate_hash_from_dict, d0, {'blacklist': ['a']})
        self.assertRaises(KeyError, dicthash.generate_hash_from_dict, d0, {'whitelist': ['c']})