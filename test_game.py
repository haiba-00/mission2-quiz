import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from game import QuizGame
from inputs import read_number
from quiz import Quiz
from storage import StateStore
import main


class GameTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / 'state.json'

    def test_numeric_validation(self):
        with patch('builtins.input', side_effect=['', 'abc', '0', '9', ' 2 ']):
            self.assertEqual(read_number('>', 1, 4), 2)

    def test_quiz_schema(self):
        for answer in [True, 0, 5, '1']:
            with self.assertRaises(ValueError):
                Quiz('문제', ['a', 'b', 'c', 'd'], answer)

    def test_add_and_restart(self):
        game = QuizGame(self.path)
        with patch('builtins.input', side_effect=['', '새 문제', 'a', 'b', 'c', 'd', 'abc', '4']):
            game.add_quiz()
        loaded = QuizGame(self.path)
        self.assertEqual(len(loaded.quizzes), 6)
        self.assertEqual(loaded.quizzes[-1].question, '새 문제')
        self.assertEqual(loaded.quizzes[-1].answer, 4)

    def test_play_best_persists_and_does_not_decrease(self):
        game = QuizGame(self.path)
        with patch('builtins.input', side_effect=['2', '1', '3', '4', '1']):
            self.assertEqual(game.play(), 100)
        game = QuizGame(self.path)
        with patch('builtins.input', return_value='2'):
            self.assertLess(game.play(), 100)
        self.assertEqual(QuizGame(self.path).best_score, 100)

    def test_no_game_vs_zero_score(self):
        game = QuizGame(self.path)
        self.assertIsNone(game.best_score)
        with patch('builtins.input', return_value='4'):
            self.assertEqual(game.play(), 20)
        game.best_score = 0
        game.save()
        self.assertEqual(QuizGame(self.path).best_score, 0)

    def test_missing_corrupt_and_invalid_schema(self):
        self.assertIsNone(StateStore(self.path).load())
        for raw in ['{broken', '[]', '{"quizzes": [{}]}', '{"quizzes": [], "best_score": true}']:
            self.path.write_text(raw, encoding='utf-8')
            self.assertEqual(len(QuizGame(self.path).quizzes), 5)
        self.path.write_bytes(b'\xff')
        self.assertEqual(len(QuizGame(self.path).quizzes), 5)

    def test_empty_collection(self):
        self.path.write_text('{"quizzes": [], "best_score": null}', encoding='utf-8')
        game = QuizGame(self.path)
        with patch('builtins.input', side_effect=AssertionError('Must not ask for answer')):
            self.assertIsNone(game.play())
            game.list_quizzes()

    def test_write_failure_preserves_old_state(self):
        game = QuizGame(self.path)
        game.save()
        old = self.path.read_bytes()
        with patch('pathlib.Path.replace', side_effect=PermissionError('denied')):
            self.assertFalse(game.save())
        self.assertEqual(old, self.path.read_bytes())

    def test_eof_and_ctrl_c_save(self):
        for error in [EOFError, KeyboardInterrupt]:
            game = QuizGame(self.path)
            with patch('main.QuizGame', return_value=game), patch('builtins.input', side_effect=error):
                main.main()
            self.assertTrue(self.path.exists())

    def test_backup_recovery_preserves_corrupt_original(self):
        game = QuizGame(self.path)
        game.best_score = 80
        self.assertTrue(game.save())
        game.best_score = 100
        self.assertTrue(game.save())
        self.path.write_text('{broken', encoding='utf-8')
        restored = QuizGame(self.path)
        self.assertEqual(restored.best_score, 80)
        originals = list(self.path.parent.glob('state.json.corrupt-*'))
        self.assertEqual(len(originals), 1)
        self.assertEqual(originals[0].read_text(encoding='utf-8'), '{broken')
        self.assertTrue(restored.save())
        self.assertEqual(QuizGame(self.path).best_score, 80)

    def test_missing_primary_recovers_backup(self):
        game = QuizGame(self.path)
        game.best_score = 60
        game.save()
        game.save()
        self.path.unlink()
        self.assertEqual(QuizGame(self.path).best_score, 60)

    def test_invalid_backup_falls_back_to_defaults(self):
        self.path.write_text('{broken', encoding='utf-8')
        self.path.with_name('state.json.bak').write_text('[]', encoding='utf-8')
        self.assertEqual(len(QuizGame(self.path).quizzes), 5)

    def test_menu_dispatch(self):
        game = QuizGame(self.path)
        with patch('builtins.input', side_effect=['3', '4', '5']), patch.object(game, 'list_quizzes') as listing, patch.object(game, 'show_score') as score:
            game.run()
        listing.assert_called_once()
        score.assert_called_once()


if __name__ == '__main__':
    unittest.main()
