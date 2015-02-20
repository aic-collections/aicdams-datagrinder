import multiprocessing
import subprocess

import cherrypy

class Engine():
    '''App engine class.

    Contains the application's core functionality not strictly related
    to the HTTP request.
    '''

    def fork_and_callback(
            args, ds, on_success=None, on_error=None, on_complete=None):
        '''Asynchronous processing with callback.

        Forks a process and runs a callable when the sub-process is complete.
        Adapted from http://stackoverflow.com/a/2581943/1069841

        @param args (list) List of arguments as supported by subprocess.Popen.
        @param on_success @TODO (callable) A function to be called after the
            subprocess completes successfully.
        @param on_error @TODO (callable) A function to be called after the
            subprocess returns an error.
        @param on_complete (callable) A function to be called after the
            subprocess returns.
        '''

        def run_subprocess(args, onSuccess, onError, onComplete):
            proc = subprocess.Popen(*args)
            proc.wait()
            on_complete()
            return

        p = multiprocessing.Process(
            target=run_subprocess,
            args=(args, onSuccess, onError, onComplete)
        )
        p.start()
        # returns immediately after the subprocess starts
        return p


    def process_stream(args, ds, timeout=30):
        '''Synchronous processing.

        This method simply returns the datastream processed.

        @param args (list) List of arguments as supported by subprocess.Popen.
        @param timeout (int) Seconds to timeout
        '''

        cherrypy.log('Popen arguments: {}'.format(args))
        proc = subprocess.Popen(
                args, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        try:
            out, err = proc.communicate(input=ds.read(), timeout=timeout)
        except TimeoutExpired:
            proc.kill()
            out, err = proc.communicate()

        if err:
            raise cherrypy.HTTPError(
                '400 Bad Request',
                'Error processing data: {}'.format(err)
            )
        return out

