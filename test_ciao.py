
import unittest
import os
import subprocess as subp
import sys
import glob


class CiaoError(Exception):
    pass



class TestCiao(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """setting up"""
        
        cls.chandra_basedir = '/home/idies/workspace/headata/FTP/chandra/data/byobsid' 
        cls.chandra_obsid   = '9805'
        cls.chandra_outdir  = f'tmp.{cls.chandra_obsid}'
        
        if os.path.exists(cls.chandra_outdir):
            os.system(f'rm -rf {cls.chandra_outdir}')
        os.system(f'mkdir -p {cls.chandra_outdir}')
        
    @classmethod
    def tearDownClass(cls):
        os.system(f'rm -rf {cls.chandra_outdir}')
    
    def test_conda_env(self):
        """Test we are in heasoft conda env"""
        self.assertIn('CONDA_PREFIX', os.environ)
        
        env = os.environ['CONDA_PREFIX'].split('/')[-1]
        self.assertEqual(env, 'ciao')
    
    def test_env(self):
        """Test envirenment vairables are set"""
        self.assertIn('HEADAS', os.environ)
        self.assertIn('CALDB', os.environ)
        self.assertIn('CIAO_VERSION', os.environ)
        
    def test_sherpa(self):
        """Test sherpa can be imported"""
        import sherpa
    
    def test_caldbinfo(self):
        """Test a call to caldb works"""
        out = os.system('caldbinfo BASIC')
        self.assertEqual(out, 0)
        
        
    def test_chandra_pipeline(self):
        """test a call to chandra data reduction"""
                
        basedir = self.chandra_basedir 
        obsid   = self.chandra_obsid
        outdir  = self.chandra_outdir
        obsdir  = f'{basedir}/5/{obsid}'
        os.system(f'cp -rL {obsdir} {outdir}')
        
        
        cmd = f'chandra_repro {outdir}/9805 {outdir}/9805.repro'
        proc = subp.Popen(cmd.split(), stdout=subp.PIPE, stderr=subp.PIPE)
        out, err = proc.communicate()
        
        if proc.returncode != 0:
            raise CiaoError('chandra_repro in test_chandra_pipeline failed!\n' + 
                               '\n'.join(out.decode()+err.decode()))


if __name__ == '__main__':
    
    unittest.main()