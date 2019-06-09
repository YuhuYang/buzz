import os
import shutil
import unittest

from unittest.mock import ANY, Mock, mock_open, patch
from buzz.corpus import Corpus
from buzz.constants import CONLL_COLUMNS
from buzz.contents import Contents
from buzz.dataset import Dataset

TOTAL_TOKENS = 329

STRUCTURE = dict(first='one',
                 second='second',
                 third='space in name')

BOOK_IX = [('second', 1, 6), ('space in name', 3, 2), ('space in name', 4, 12)]


class TestCorpus(unittest.TestCase):

    def setUp(self):
        self.unparsed = Corpus('tests/data')
        self.parsed = Corpus('tests/testing-parsed')
        self.loaded = self.parsed.load()
        # super().__init__()

    def test_subcorpora_and_files(self, corpus=None):
        corpus = corpus or self.unparsed
        subcorpora = corpus.subcorpora
        files = corpus.files
        self.assertIsInstance(subcorpora, Contents)
        self.assertEqual(len(subcorpora), 3)
        for i, (k, v) in enumerate(STRUCTURE.items()):
            sub = corpus[i]
            also_sub = subcorpora[i]
            self.assertEqual(sub, also_sub)
            self.assertEqual(sub.name, k)
            f = sub[0]
            also_f = sub.files[0]
            self.assertEqual(f, also_f)
            self.assertEqual(f.name, v)

        for sub in subcorpora:
            self.assertTrue(len(sub))
        self.assertIsInstance(files, Contents)
        self.assertEqual(len(files), 3)

    def test_repr(self):
        start = '<buzz.corpus.Corpus'
        end = '(tests/data, unparsed)>'
        self.assertTrue(str(self.unparsed).startswith(start), str(self.unparsed))
        self.assertTrue(str(self.unparsed).endswith(end), str(self.unparsed))

    # add slow deco
    def test_parse(self):
        parsed_path = 'tests/data-parsed'
        shutil.rmtree(parsed_path)
        parsed = self.unparsed.parse()
        self.assertEqual(parsed.name, self.unparsed.name + '-parsed')
        self.test_subcorpora_and_files(parsed)
        start = '<buzz.corpus.Corpus'
        end = '(tests/data-parsed, parsed)>'
        self.assertTrue(str(parsed).startswith(start))
        self.assertTrue(str(parsed).endswith(end), str(parsed))

    def test_loaded(self):
        self.assertIsInstance(self.loaded, Dataset)
        self.assertEqual(len(self.loaded), TOTAL_TOKENS)
        self.assertTrue(all(i in self.loaded.columns for i in CONLL_COLUMNS))

    def test_just_skip(self):
        book = self.just.lemmata.book
        regex_book = l.just.lemmata('b..k')
        self.assertTrue(all(book.index == regex_book.index))
        self.assertEqual(len(book), 3)
        indices = list(book.index)
        for fsi in BOOK_IX:
            self.assertTrue(fsi in indices)
        nobook = self.skip.lemmata.book
        self.assertEqual(len(nobook), TOTAL_TOKENS-len(book))

    def test_search(self):
        # todo
        pass


if __name__ == '__main__':
    unittest.main()
