from util.FtpServ import FtpServ
import os


class FtpDriver:
    """This class is a command-line ftp file explorer using FtpServ to interact with the remote server.

    This class functions as a Driver for FtpServ.
    Copyright (C) 2017 Gurney Benjamin Buchanan (gurney.buchanan@gmail.com)
    """
    def __init__(self, files=None):
        """This method initializes some critical variables and an FtpServ object.

        This method also initializes the FtpServ object's FTP connection by calling connect.
        :param files: unused -- this allows FtpDriver and LocalDriver to have the same interface.
        """
        self.ftp_service = FtpServ()
        self.ftp_service.connect()
        self.continue_to_next = False

    def is_connected(self):
        """This method checks to see if the ftp_service (FtpServ object) is_connected.

        This simply passes the call through to the ftp_service object.
        :return: The FTP connection status.  True if there is a successful connection, false if not.
        """
        return self.ftp_service.is_connected()

    def get_file(self):
        """This is the main loop for the driver, prompting for input and navigating directories until a file is chosen.

        This method handles the printing of prompts, lists of files in each folder, and taking user input.
        :return: the location of the downloaded temp file.
        """
        print("Initializing FTP Connection")
        _found = False
        while not _found:
            print("Current Directory: " + self.ftp_service.current_dir())
            print("Current Directory Contains: ")
            _item_number = 1
            _list = self.ftp_service.list_dir()
            print("{:_<20}\t{:_<20}\t{:_<20}\t{:_<20}".format("", "", "", ""))
            for item in _list:
                print("{:<20}\t".format("{:.20}".format(item)), end='')
                if (_item_number % 4) is 0:
                    print("")
                _item_number += 1
            if ((_item_number - 1) % 4) is not 0:
                print("")
            print("{:_<20}\t{:_<20}\t{:_<20}\t{:_<20}".format("", "", "", ""))
            print("Enter: \n-The item you want to open\n-The directory to navigate to\n-'up' to go up a directory\n-'base' to return to the home directory\n-'quit' to quit beet\n > ", end="")
            _dest = input()
            if _dest.lower() == "base":
                self.ftp_service.to_home()
            elif _dest.lower() == "up":
                self.ftp_service.to_dir(os.path.split(self.ftp_service.current_dir())[0])
            elif _dest.lower() == "quit":
                _found = True
                _temp_file = None
            else:
                _found, _temp_file = self.ftp_service.goto(_dest)
        _continue_set = False
        while _temp_file is not None and not _continue_set:
            _continue_video_input = input("\nDo you want to analyze all videos after this one? (y/n)\n > ")
            if _continue_video_input.lower() == "y":
                _continue_set = True
                self.continue_to_next = True
            elif _continue_video_input.lower() == "n":
                _continue_set = True
                self.continue_to_next = False
            else:
                print("Invalid Entry")
        return _temp_file

    def continue_video(self):
        """This method will either download the next video and return its location or return None is it does not exist.

        :return: exists --  The location of the next video after it is downloaded or none if there is no next video.
        """
        if self.continue_to_next:
            _exists, _next = self.ftp_service.get_next_video()
            if not _exists:
                return None
            else:
                return _next
        else:
            return None

    def close(self):
        """This method closes the ftp connection by passing the call through to the ftp_service object."""
        self.ftp_service.close()

    def end_video(self):
        """This method ends the video playback to delete the temporary video file by passing the call through."""
        self.ftp_service.end_video()

    def get_cur_vid(self):
        """This method will return the current video by passing the call to the ftp_service.

        :return: a string representing the current video
        """
        return self.ftp_service.get_cur_vid()

    def get_vid_date(self):
        """This method will return the current video date by passing te call to ftp_service.

        This is only intended to work with Beemon files.
        :return: a string representing the current video's date recorded.
        """
        return self.ftp_service.get_vid_date()
