# This is a sample commands.py.  You can add your own commands here.
#
# Please refer to commands_full.py for all the default commands and a complete
# documentation.  Do NOT add them all here, or you may end up with defunct
# commands when upgrading ranger.

# A simple command for demonstration purposes follows.
# -----------------------------------------------------------------------------

from __future__ import (absolute_import, division, print_function)

# You can import any python module as needed.
import os

# You always need to import ranger.api.commands here to get the Command class:
from ranger.api.commands import Command


# Any class that is a subclass of "Command" will be integrated into ranger as a
# command.  Try typing ":my_edit<ENTER>" in ranger!
class my_edit(Command):
    # The so-called doc-string of the class will be visible in the built-in
    # help that is accessible by typing "?c" inside ranger.
    """:my_edit <filename>

    A sample command for demonstration purposes that opens a file in an editor.
    """

    # The execute method is called when you run this command in ranger.
    def execute(self):
        # self.arg(1) is the first (space-separated) argument to the function.
        # This way you can write ":my_edit somefilename<ENTER>".
        if self.arg(1):
            # self.rest(1) contains self.arg(1) and everything that follows
            target_filename = self.rest(1)
        else:
            # self.fm is a ranger.core.filemanager.FileManager object and gives
            # you access to internals of ranger.
            # self.fm.thisfile is a ranger.container.file.File object and is a
            # reference to the currently selected file.
            target_filename = self.fm.thisfile.path

        # This is a generic function to print text in ranger.
        self.fm.notify("Let's edit the file " + target_filename + "!")

        # Using bad=True in fm.notify allows you to print error messages:
        if not os.path.exists(target_filename):
            self.fm.notify("The given file does not exist!", bad=True)
            return

        # This executes a function from ranger.core.acitons, a module with a
        # variety of subroutines that can help you construct commands.
        # Check out the source, or run "pydoc ranger.core.actions" for a list.
        self.fm.edit_file(target_filename)

    # The tab method is called when you press tab, and should return a list of
    # suggestions that the user will tab through.
    # tabnum is 1 for <TAB> and -1 for <S-TAB> by default
    def tab(self, tabnum):
        # This is a generic tab-completion function that iterates through the
        # content of the current directory.
        return self._tab_directory_content()

class bg(Command):
    # set the selected image as bacground
    home = os.environ['HOME'] + '/'
    config_file = home+'.config/i3/config'
    
    def find_current_wall(self):
        with open(self.config_file, 'r') as conf:
            alines = conf.readlines()
        for line in alines:
            if 'feh --bg-scale' in line:
                return line.split()[-1]

    def execute(self):
        self.fm.run(f'feh --bg-scale {self.fm.thisfile}')
        # update i3 config file
        # getting the existing wallpaper name
        current_wall = self.find_current_wall()
        # make a backup of config
        self.fm.run(f'cp {self.config_file} {self.config_file+".bak"}')
        #update the i3 config file
        current_wall = current_wall.replace('/','\/')
        new_wall = str(self.fm.thisfile).replace('/','\/')
        self.fm.run(f'sed -i "s/{current_wall}/{new_wall}/" {self.config_file}')



class bk(Command):
    '''
    This is only for testing
    '''
    home = os.environ['HOME'] + '/'

    def remove_home(self, pathname):
        pathname = pathname.split('/')
        pathname = '/'.join(pathname[3:])
        return pathname

    def check_dir(self, fullpath):
        with open(self.home + 'dotdir.txt', 'r') as dotdirs:
            dirlist = dotdirs.readlines()
        dirlist = [x.strip('\n') for x in dirlist]
        if self.remove_home(str(fullpath)) in dirlist:
            return True
        else:
            return False

    def check_file(self, fullpath):
        with open(self.home + 'dotfile.txt', 'r') as dotfiles:
            filelist = dotfiles.readlines()
        filelist = [x.strip('\n') for x in filelist]
        if str(fullpath) in filelist:
            return True
        else:
            return False

    def savefile(self, filepath, outfile=None):
        if self.check_file(filepath):
            self.fm.notify('file is already in dotfile.txt', bad=True)
            return
        else:
            with open(self.home + 'dotfile.txt', 'a') as dotfiles:
                dotfiles.write(self.remove_home(str(filepath)) + '\n')
            self.fm.notify('file {} added to dotfile.txt'.format(filepath))

    def savedir(self, filepath, outfile=None):
        if self.check_dir(filepath):
            self.fm.notify('file is already in dotdir.txt', bad=True)
            return
        else:
            with open(self.home + 'dotdir.txt', 'a') as dotdirs:
                dotdirs.write(self.remove_home(str(filepath)) + '\n')
            self.fm.notify('file {} added to dotdir.txt'.format(filepath))

    def execute(self):
        fullpath = self.fm.thisfile.path
        if os.path.isfile(fullpath):
            self.savefile(fullpath)
        else:
            self.savedir(fullpath)
# https://github.com/ranger/ranger/wiki/Integrating-File-Search-with-fzf
# Now, simply bind this function to a key, by adding this to your ~/.config/ranger/rc.conf: map <C-f> fzf_select
class fzf_select(Command):
    """
    :fzf_select

    Find a file using fzf.

    With a prefix argument select only directories.

    See: https://github.com/junegunn/fzf
    """
    def execute(self):
        import subprocess
        if self.quantifier:
            # match only directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -type d -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        else:
            # match files and directories
            command="find -L . \( -path '*/\.*' -o -fstype 'dev' -o -fstype 'proc' \) -prune \
            -o -print 2> /dev/null | sed 1d | cut -b3- | fzf +m"
        fzf = self.fm.execute_command(command, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.decode('utf-8').rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)
# fzf_locate
class fzf_locate(Command):
    """
    :fzf_locate

    Find a file using fzf.

    With a prefix argument select only directories.

    See: https://github.com/junegunn/fzf
    """
    def execute(self):
        import subprocess
        if self.quantifier:
            command="locate home media | fzf -e -i"
        else:
            command="locate home media | fzf -e -i"
        fzf = self.fm.execute_command(command, stdout=subprocess.PIPE)
        stdout, stderr = fzf.communicate()
        if fzf.returncode == 0:
            fzf_file = os.path.abspath(stdout.decode('utf-8').rstrip('\n'))
            if os.path.isdir(fzf_file):
                self.fm.cd(fzf_file)
            else:
                self.fm.select_file(fzf_file)
