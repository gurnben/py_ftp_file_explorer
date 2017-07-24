import os
import ftplib
import tempfile


class FtpServ:
    """This class will open, hold, and provide a simple interface with an FTP connection.

    This is meant as a backend for an FTP driver utility to take user input; however, it can be used individually.
    Copyright (C) 2017 Gurney Benjamin Buchanan (gurney.buchanan@gmail.com)
    """

    def __init__(self):
        """This method initializes two important variables to determine the FTP state."""
        self.state = False
        self.cur_vid = None

    def connect(self):
        """This method initiates an FTP connection based on the information in the auth.txt file.

        If there is no auth.txt file it will print an error and break.
        """
        while True:
            try:
                if os.path.exists("auth.txt"):
                    self.file = open("auth.txt", 'r')
                    self.ftp = ftplib.FTP(self.file.readline()[:-1])
                    # Will NOT save passwords
                    self.ftp.login(self.file.readline()[:-1], self.file.readline()[:-1])
                    self.base_dir = self.file.readline()[:-1]
                    self.ftp.cwd(self.base_dir)
                    self.file.close()
                    self.state = True
                    break
                else:
                    print("No auth.txt file.  Create an auth.txt file in the same directory as beet.py.")
                    break
            except (ftplib.error_perm, AttributeError):
                print("Connection Failure.  Check your login credentials in auth.txt.")
                continue

    def list_dir(self):
        """This method returns a tuple that lists the current directory's contents.

        :return: A tuple of strings representing the current directory's contents.
        """
        return self.ftp.nlst()

    def current_dir(self):
        """This method will return the current directory location.

        :return: A string representing the current directory location.
        """
        return self.ftp.pwd()

    def goto(self, file):
        """This method will navigate to or download a directory or file name.

        :param file: The filename or directory name to navigate to.
        :return: Boolean -- True if the file was NOT chosen, false if the file was chosen
                 String  -- A string location of the downloaded file or a null string if no file was chosen.
        """
        try:
            if file.endswith(".h264"):  # TODO: Change this line to change the target file type!!
                self.cur_vid = file
                self.file = tempfile.NamedTemporaryFile(delete=False)
                self.ftp.retrbinary("RETR " + self.ftp.pwd() + "/" + file, self.file.write)
                self.file.close()
                return True, self.file.name
            else:
                self.to_dir(os.path.join(self.ftp.pwd(), file))
                return False, ""
        except ftplib.all_errors:
            print("FTP Error")
            return False, ""

    def to_dir(self, path):
        """This method will change the directory to the input directory if possible.

        If the desired directory cannot be navigated to, it will remain in the current directory.
        :param path: The filepath to navigate to.
        :return: True if the navigation was successful, False if not.
        """
        current = self.ftp.pwd()
        try:
            self.ftp.cwd(path)
            return True
        except ftplib.all_errors:
            print("Invalid Entry")
            self.ftp.cwd(current)
            return False

    def to_home(self):
        """This method will return to the base directory given in the login/auth file."""
        self.ftp.cwd(self.base_dir)

    def get_next_video(self):
        """This method will download the next video and return the location if it exists.

        :return: Boolean    --  True if the file exists and was downloaded, False if not.
                 String     --  The downloaded file's location if it exists.
        """
        assert(self.cur_vid is not None)
        list = self.ftp.nlst()
        index = list.index(self.cur_vid)
        if len(list) > (index + 1):
            file = list[index + 1]
            self.cur_vid = file
            if os.path.exists(self.file.name):
                os.remove(self.file.name)
            self.file = tempfile.NamedTemporaryFile(delete=False)
            self.ftp.retrbinary("RETR " + self.ftp.pwd() + "/" + file, self.file.write)
            self.file.close()
            return True, self.file.name
        else:
            return False, ""

    def is_connected(self):
        """This method will return the connection status.

        It will check the state to see if a connection has been initialized.  If it has not been initialized, then /
        it will return True, False.  If the connection has been initialized it will attempt to send a NOOP command /
        to test the connection.  If the connection throws and error it will return False, True.  Otherwise if the  /
        connection has been initialized and is still connected it will return False, False.
        :return: Boolean    --  True if the connection was NOT initialized, False if it was initialized.
                 Boolean    --  True if the connection is NOT functioning, False if the connection is valid.
        """
        if self.state is False:
            return True, False
        else:
            try:
                self.ftp.voidcmd("NOOP")
                return False, True
            except ftplib.all_errors:
                return False, False

    def end_video(self):
        """This method will close the temp file and delete it.

        This is done so temp files do not build up on the host computer.
        """
        if self.file is not None:
            self.file.close()
        if self.file is not None and os.path.exists(self.file.name):
            os.remove(self.file.name)

    def close(self):
        """This method will close the FTP connection."""
        self.ftp.close()

    def get_cur_vid(self):
        """This method will return the current video location.

        :return: String --  The current video location.
        """
        return self.cur_vid

    def get_vid_date(self):
        """This method will return the current video's date recorded.

        This is intended to be used with Beemon files so the date recorded is the directory name up one directory from
        the current location.  
        :return:
        """
        return os.path.split(os.path.split(self.ftp.pwd())[0])[1]
