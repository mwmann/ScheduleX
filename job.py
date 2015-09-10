import sys
import traceback
import subprocess

class Job(object):
    """Basic Job implementation to execute a basic subprocess with arguments"""

    jobExec = None
    jobArgs = None
    jobpid = None
    jobretcode = None
    cmdlst = []

    def __init__(self,jobcmd,arglst):
        self.jobExec = str(jobcmd)
        self.jobArgs = arglst

        # validate input arguments / parameter list
        if len(self.jobArgs)==0:
            self.cmdlst=[self.jobExec]
        else:
            self.cmdlst = self.jobArgs
            self.cmdlst.insert(0,self.jobExec)


    def buildcmd(self):
        """Validates input arguments and builds executable command list.

        This function is intended to be overidden in subclass implementations on Job()
        depending on the type of script or executiable needing to be run.
        Examples of different execution commands which will require their own
        implementation of buildcmd() to prepend the respective interpreter:
        Windows Executable -- myprogram.exe
        Windows batch -- myscript.bat
        Unix Shell -- myshell.sh
        Java -- java myclass
        Python -- python myyscript.py
        """
        pass


    def execjob(self):
        """Execute command and arguments.

        This function is intended to be overidden in subclasss implementations of Job()
        if custom logic is required to execute the subprocess.
        Examples could inlclude:
        -- execute a number of subprocesses / multi-threading
        -- manipulate arguments prior to subprocess execution
        """

        self.buildcmd()
        self.execproc()

    def execproc(self) :
        """Execute job command and arguments as a subprocess."""

        try:
            proc = subprocess.Popen(self.cmdlst,stdout=subprocess.PIPE)
            self.jobpid = proc.pid
            self.stdout_value, self.stderr_value = proc.communicate()

            self.jobretcode = proc.returncode
            self.jobout = self.stdout_value
            #print 'DEBUG:',self.jobout

            if self.jobretcode <> 0 :
                raise RuntimeError('exited with non zero return code')

        except Exception as err:
            #print 'EXCEPTION ERROR: ',str(err)
            print traceback.print_exc(file=sys.stdout)
            print 'DEBUG:',self.jobout
            exit(-1)


class JavaJob(Job):

    def buildcmd(self):
        """Validates input arguments and builds executable command list for a java job.

        Java -- java myclass
        """
        #add a java interpreter call as a pre command to the java class
        precmd='java'
        self.cmdlst.insert(0,precmd)

class PythonJob(Job):

    def buildcmd(self):
        """Validates input arguments and builds executable command list for a python job.

        python -- python myscript.py
        """
        #add python  interpreter call as a pre command to the python script
        precmd='python'
        self.cmdlst.insert(0,precmd)

if __name__ == '__main__':
    winarg=['param1']
    wincmd = 'C:\py_sandbox\ScheduleX-master\scripts\hellow.bat'

    winJob = Job(wincmd,winarg)
    winJob.execjob()
    print 'Job Process Id:', winJob.jobpid
    print 'Job Return Code:',winJob.jobretcode
    print 'Job Output: ',winJob.jobout

    javaarg=['param1']
    javacmd = 'C:\py_sandbox\ScheduleX-master\scripts\helloj'

    javaJob = JavaJob(javacmd,javaarg)
    javaJob.execjob()
    print 'Job Process Id:',javaJob.jobpid
    print 'Job Return Code:',javaJob.jobretcode
    print 'Job Output: ',javaJob.jobout

    pyarg=['param1']
    pycmd = 'C:\py_sandbox\ScheduleX-master\scripts\hellop.py'

    pyJob = PythonJob(pycmd,pyarg)
    pyJob.execjob()
    print 'Job Process Id:',pyJob.jobpid
    print 'Job Return Code:',pyJob.jobretcode
    print 'Job Output: ',pyJob.jobout

    exit (0)
