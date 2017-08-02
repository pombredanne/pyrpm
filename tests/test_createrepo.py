import os
import os.path
import shutil
import unittest


from pyrpm.yum import YumPackage
from pyrpm.tools.createrepo import YumRepository


class CreateRepoTest(unittest.TestCase):
    def setUp(self):
        self.repodir = os.path.join(os.path.dirname(__file__), "testrepo")
        self.pkg = YumPackage(open('tests/Eterm-0.9.3-5mdv2007.0.src.rpm', 'rb'))

        # ensure empty repodir
        if os.path.exists(self.repodir):
            shutil.rmtree(self.repodir)
        os.mkdir(self.repodir)

    def tearDown(self):
        self.pkg.rpmfile.close()

    def test_simple(self):
        # create repo
        repo = YumRepository(self.repodir)
        assert len(list(repo.packages())) == 0

        # add package
        repo.add_package(self.pkg)
        assert len(list(repo.packages())) == 1

        # delete package
        repo.remove_package('4d9c71201f9c0d11164772600d7dadc2cad0a01ac4e472210641e242ad231b3a')
        assert len(list(repo.packages())) == 1

        repo.remove_package('c77bcc090c8d541e475f6f39b65a742a92a7f9a2e545ea8210eef0ca995515ac')
        assert len(list(repo.packages())) == 0

    def test_save_read(self):
        # create repo
        repo = YumRepository(self.repodir)
        assert len(list(repo.packages())) == 0

        # add package
        repo.add_package(self.pkg)
        repo.save()
        assert len(list(repo.packages())) == 1

        repo = YumRepository(self.repodir)
        assert len(list(repo.packages())) == 0
        repo.read()
        assert len(list(repo.packages())) == 1
