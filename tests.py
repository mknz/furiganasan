import unittest

from app import app
from furi import add_yomi


class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True

        # Need this to do form post test
        app.config['WTF_CSRF_ENABLED'] = False

        self.app = app.test_client()

    def tearDown(self):
        pass


class TestInputs(FlaskTestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_get(self):
        response = self.app.get('/')
        assert response.status_code == 200

    def test_yomi(self):
        examples = []
        examples.append(dict(before='漢字', after='漢字(かんじ)'))
        examples.append(dict(before='程度', after='程度(ていど)'))
        examples.append(dict(before='言い方', after='言(い)方(かた)'))
        examples.append(dict(before='他ならず', after='他(ほか)ならず'))
        examples.append(dict(before='意味合い', after='意味合(いみあ)い'))
        examples.append(dict(before='一時的', after='一時的(いちじてき)'))
        examples.append(dict(before='茅ヶ崎', after='茅ヶ崎(ちがさき)'))

        for example in examples:
            string_with_yomi = add_yomi(example['before'])
            with self.subTest():
                self.assertEqual(string_with_yomi, example['after'], example['before'])


if __name__ == '__main__':
    unittest.main()
