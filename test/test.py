
import unittest
import subprocess
import nose
import signal
import os
import shutil

import ll.core

BITBUCKET_URL = "https://bitbucket.org/pdekker/ll-api" # fork by pdekker
MONGOD_TEST_CONFIG = "config/mongodb_test.conf"
LL_CONFIG = "config/livinglabs.ini"
LL_DB_CONFIG = "config/db.ini"
USER = "ll"
USER_PWD = "USERSECRET"
DB_NAME = "ll"
ADMIN = "admin"
ADMIN_PWD = "ADMINSECRET"
DUMP_PATH = "dump"

SITE_KEY = "E0016261DE4C0D61-M6C4AMHHE4WV4OVY"
PARTICIPANT_KEY = "9EA887B684DD5822-JBB2XOCVEGYE7YAZ"
HOST = "localhost"
N_ITERATIONS = 3 # number of iterations site or participant runs

#mongo_pid = 0
#api_process = None
    
class TestLL(unittest.TestCase):
    
    def setUp(self):
        self.mongo_pid = 0
        self.api_process = None
        
        # Create clean directory for database, include example queries and docs
        os.makedirs("testdb")
        shutil.copy2("data/queries.xml","testdb")
        shutil.copy2("data/qrel.txt","testdb")
        shutil.copytree("data/docs","testdb/docs")
        # Launch mongod
        print("Launch MongoDB")
        mongo_output = subprocess.check_output(["mongod","--fork","--syslog","--config",MONGOD_TEST_CONFIG])
        # Real Mongo process will be forked, save for pid from output
        for word in mongo_output.split():
            if word.isdigit():
                self.mongo_pid = int(word)
        # Set up MongoDB users
        print("Setup MongoDB users")
        subprocess.call(["./bin/admin", "db", "--setup-db-users", "--mongodb_db", DB_NAME, "--mongodb_user", USER, "--mongodb_user_pw", USER_PWD, "--mongodb_admin", ADMIN, "--mongodb_admin_pw", ADMIN_PWD])
        # Save to configuration file
        subprocess.call(["./bin/admin", "db", "--mongodb_db", DB_NAME, "--mongodb_user", USER, "--mongodb_user_pw", USER_PWD, "--export-conf-file", LL_DB_CONFIG])
        # Start the API
        self.api_process = subprocess.Popen(["./bin/api","-c",LL_CONFIG,LL_DB_CONFIG,"--debug"])
        # Fill database with users
        subprocess.call(["./bin/admin","db","--import-json","dump","-c", LL_DB_CONFIG])
        
    
    def test_site(self):
        print("Test client")
        subprocess.call(["./bin/client-site", "--host", HOST, "--key", SITE_KEY, "-q","-d"])
        print("Simulate client")
        site_output = subprocess.check_output(["./bin/client-site", "--host", "localhost", "--key", SITE_KEY, "-s", "--iterations", str(N_ITERATIONS)])
        for line in site_output.split("\n"):
            if len(line) > 0:
                if line.split()[0] != "NDCG:":
                    raise ValueError("Unexpected site output:", line)
        return True
    
    def test_participant(self):
        print("Simulate participant")
        participant_output = subprocess.check_output(["./bin/client-participant", "--host", HOST, "--key", PARTICIPANT_KEY, "-s", "--iterations", str(N_ITERATIONS)])
        for line in participant_output.split("\n"):
            if len(line) > 0:
                first = line[0]
                last = line[-1]
                if not (first=="{" and last=="}"):
                    raise ValueError("Unexpected participant output:", line)
        return True
    
    def tearDown(self):
        print("Teardown")
        
        # Kill api
        self.api_process.kill()
        # Kill mongo
        os.kill(self.mongo_pid,signal.SIGKILL)
        
        # Remove testdb directory
        shutil.rmtree("testdb")
        

if __name__ == '__main__':
    unittest.main()
