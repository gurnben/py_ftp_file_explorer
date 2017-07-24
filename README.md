# py_ftp_file_explorer
A Command-Line FTP File Explorer for Python


To use:

1. Download files and add them to your project
2. Create an auth.txt file in the format:

         <FTP Address>
         <Username>
         <Password>
         <Base Directory/Starting Directory>
 
3. Instantiate an FtpDriver object.  
4. *optional* Ensure the FTP connection is successful using the is_connected() method. 
5. Call the FtpDriver object's get_file () method to prompt the user for a file and download it into a temporary file.  


That's all folks! 
