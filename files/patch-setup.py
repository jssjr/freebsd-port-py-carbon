--- setup.py.orig	2011-08-14 23:55:14.000000000 +0000
+++ setup.py	2011-08-14 23:57:46.000000000 +0000
@@ -3,6 +3,9 @@
 import os
 from glob import glob
 
+carbon_dbdir = '%%CARBON_DBDIR%%' + '/'
+carbon_etcdir = '%%ETCDIR%%' + '/'
+
 if os.environ.get('USE_SETUPTOOLS'):
   from setuptools import setup
   setup_kwargs = dict(zip_safe=0)
@@ -11,10 +14,12 @@
   from distutils.core import setup
   setup_kwargs = dict()
 
+storage_dirs = [ ]
+
+for subdir in ('whisper', 'lists', 'rrd'):
+  storage_dirs.append( (carbon_dbdir + subdir, []) )
 
-storage_dirs = [ ('storage/whisper',[]), ('storage/lists',[]),
-                 ('storage/log',[]), ('storage/rrd',[]) ]
-conf_files = [ ('conf', glob('conf/*.example')) ]
+conf_files = [ (carbon_etcdir, glob('conf/*.example')) ]
 
 setup(
   name='carbon',
