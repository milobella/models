import json
import unittest
from scripts.builder import build
import os
dir_path = os.path.dirname(os.path.realpath(__file__))


class TestBuild(unittest.TestCase):

    def test_build_model1(self):
        with open(dir_path + '/data/in/manifest1.yaml', 'r') as manifest, \
                open(dir_path + '/data/tmp/model.json', 'w') as actual_output:
            build.main(dir_path + '/data/in', manifest, actual_output)

        with open(dir_path + '/data/tmp/model.json', 'r') as actual_output, \
                open(dir_path + '/data/out/model1.json', 'r') as expected_output:
            self.assertEqual(json.load(expected_output), json.load(actual_output))

    def test_build_model2(self):
        with open(dir_path + '/data/in/manifest2.yaml', 'r') as manifest, \
                open(dir_path + '/data/tmp/model.json', 'w') as actual_output:
            build.main(dir_path + '/data/in', manifest, actual_output)

        with open(dir_path + '/data/tmp/model.json', 'r') as actual_output, \
                open(dir_path + '/data/out/model2.json', 'r') as expected_output:
            self.assertEqual(json.load(expected_output), json.load(actual_output))


if __name__ == '__main__':
    unittest.main()
