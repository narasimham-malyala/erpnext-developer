# imports - compatibility imports
from __future__ import print_function
from six.moves.urllib.parse import urljoin

# imports - standard imports
import os.path as osp
import logging

# imports - third-party imports
import git

# imports - module imports
from bench import utils

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

# https://stackoverflow.com/a/31605564
class GitProgress(git.remote.RemoteProgress):
    def line_dropped(self, line):
        print(line)
    def update(self, *args):
        print(self._cur_line)

class Cache(object):
    def __init__(self, location = None, dirname = None):
        self.location = utils.assign_if_empty(location, osp.expanduser('~'))
        self.dirname  = utils.assign_if_empty(dirname , '.frappe')

    def create(self, exist_ok = True):
        dirs = osp.join(self.location, self.dirname, 'apps')
        utils.makedirs(dirs, exist_ok = exist_ok)

    def get(self, url, branch = None, verbose = False):
        branch    = utils.assign_if_empty(branch, 'master')
        path_apps = osp.join(self.location, self.dirname, 'apps')
        utils.makedirs(path_apps, exist_ok = True)

        repo      = None
        if not utils.check_url(url, raise_err = False):
            url   = urljoin('https://github.com/frappe', url)

        app      = url.rsplit('/', 1)[-1].replace('.git', '')
        app_path = osp.join(path_apps, app)

        if osp.exists(app_path):
            repo     = git.Repo(app_path)
            upstream = repo.remotes['upstream']
            upstream.pull()
        else:
            repo   = git.Repo.clone_from(url, app_path, branch = branch)
            origin = repo.remotes['origin']
            origin.rename('upstream')

        return repo