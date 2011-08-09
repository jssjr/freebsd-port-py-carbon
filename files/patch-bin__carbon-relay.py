--- bin/carbon-relay.py.orig	2011-07-23 22:47:25.859199852 -0400
+++ bin/carbon-relay.py	2011-07-23 22:42:04.000000000 -0400
@@ -32,7 +32,7 @@
 
 
 # Figure out where we're installed
-BIN_DIR = dirname(__file__)
+BIN_DIR = dirname( os.path.realpath(__file__) )
 ROOT_DIR = dirname(BIN_DIR)
 STORAGE_DIR = join(ROOT_DIR, 'storage')
 LOG_DIR = join(STORAGE_DIR, 'log', 'carbon-relay')
@@ -92,11 +92,20 @@
     print 'Failed to read pid from %s' % options.pidfile
     raise SystemExit(1)
 
-  if exists('/proc/%d' % pid):
-    print "%s is running with pid %d" % (program, pid)
-    raise SystemExit(0)
+  try:
+    os.kill(pid, 0)
+  except OSError, err:
+    if err.errno == errno.ESRCH:
+      print "%s is not running" % program
+      raise SystemExit(0)
+    elif err.errno == errno.EPERM:
+      print "No permission to signal %s" % program
+      raise SystemExit(1)
+    else:
+      print "Unknown error" % program
+      raise SystemExit(1)
   else:
-    print "%s is not running" % program
+    print "%s is running with pid %d" % (program, pid)
     raise SystemExit(0)
 
 elif action != 'start':
