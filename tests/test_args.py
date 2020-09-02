import unittest

from tew_reader.args import Args


class TestArgs(unittest.TestCase):
    def test_args_ok(self):
        sys_args = ['-th', 'path-to-tew2020',
                    '-td', 'database-name',
                    '-ts', 'save-name',
                    '-i', 'initials',
                    '-s', 'sort-key',
                    '-o', 'csv',
                    '-t', 'simple',
                    '--asc']

        args = Args().parse_args(args=sys_args)
        self.assertEqual(args.tew_home, 'path-to-tew2020')
        self.assertEqual(args.tew_db, 'database-name')
        self.assertEqual(args.tew_save, 'save-name')
        self.assertEqual(args.initials, 'initials')
        self.assertEqual(args.sort, 'sort-key')
        self.assertEqual(args.type, 'simple')
        self.assertEqual(args.reverse, False)

    def test_exclusive_asc_desc(self):
        sys_args = ['--asc', '--desc']

        with self.assertRaises(SystemExit):
            Args().parse_args(args=sys_args)


if __name__ == '__main__':
    unittest.main()
