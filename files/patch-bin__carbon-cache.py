--- bin/carbon-cache.py.orig	2011-04-02 00:08:30.000000000 +0000
+++ bin/carbon-cache.py	2011-08-15 02:54:58.000000000 +0000
@@ -36,7 +36,7 @@
 
 
 # Figure out where we're installed
-BIN_DIR = dirname( os.path.abspath(__file__) )
+BIN_DIR = dirname( os.path.realpath(__file__) )
 ROOT_DIR = dirname(BIN_DIR)
 STORAGE_DIR = join(ROOT_DIR, 'storage')
 LOG_DIR = join(STORAGE_DIR, 'log', 'carbon-cache')
@@ -62,11 +62,17 @@
 parser.add_option('--debug', action='store_true', help='Run in the foreground, log to stdout')
 parser.add_option('--profile', help='Record performance profile data to the given file')
 parser.add_option('--pidfile', default=join(STORAGE_DIR, '%s.pid' % program.split('.')[0]), help='Write pid to the given file')
+parser.add_option('--confdir', default=CONF_DIR, help="Read config files from the givien directory")
 parser.add_option('--config', default=join(CONF_DIR, 'carbon.conf'), help='Use the given config file')
 parser.add_option('--logdir', default=LOG_DIR, help="Write logs in the given directory")
+parser.add_option('--storagedir', default=STORAGE_DIR, help="Write data in the storage directory")
 
 (options, args) = parser.parse_args()
 
+STORAGE_DIR = options.storagedir
+CONF_DIR = options.confdir
+__builtins__.CONF_DIR = CONF_DIR # repeatable evil
+
 if not args:
   parser.print_usage()
   raise SystemExit(1)
@@ -105,11 +111,20 @@
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
