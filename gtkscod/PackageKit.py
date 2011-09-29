#!/usr/bin/env python

import dbus
from dbus.mainloop.qt import DBusQtMainLoop
from dbus.mainloop.glib import DBusGMainLoop

import os

class PackageSummary(object):
    def __init__(self, info, _id, summary):
        self.info       = info
        self.package_id = _id
        self.summary    = summary

        self.package_name       = ''
        self.package_version    = ''
        self.package_reponame   = ''
        self.package_arch       = ''

        list_id = self.package_id.split(';')
        if len(list_id) == 4:
            self.package_name       = list_id[0]
            self.package_version    = list_id[1]
            self.package_arch       = list_id[2]
            self.package_reponame   = list_id[3]

    def is_null(self):
        result = False
        for i in [self.package_name, self.package_arch, self.package_version, self.package_reponame]:
            if len(i) == 0:
                result = True
                break
        return result

    def is_arch(self):
        arch = os.uname()[4]
        if self.package_arch == arch:
            return True
        elif self.package_arch == 'noarch':
            return True
        return False

    def debug_print(self):
        print("Package summary %s;%s;%s" % (self.info, self.package_id, self.summary))
        print("\tInfo:                  %s" % (self.info))
        print("\tSummary:               %s" % (self.summary))
        print("\tPackage name:          %s" % (self.package_name))
        print("\tPackage version:       %s" % (self.package_version))
        print("\tPackage arch:          %s" % (self.package_arch))
        print("\tPackage repo name:     %s" % (self.package_reponame))

class PackageKitTransaction:
    def __init__(self, tctrl, tid, main_loop):
        self.pk = tctrl
        self.tid = tid
        self.props = dbus.Interface(self.pk, "org.freedesktop.DBus.Properties")
        self.main_loop = main_loop
        self.pk.connect_to_signal('ErrorCode', self._handle_error)
        self.pk.connect_to_signal('Finished', self._handle_finished)
        self.pk.connect_to_signal('Changed', self._handle_changed)
        self._is_started = False
        self._error_present = False
        self._error_code = ''
        self._error_description = ''
        
        # some handlers
        self._s_handler_property_changed = None

    def SetHints(self, locale=None, idle=True, interactive=False, cache_age=3600):
        if locale is None:
            locale = os.environ['LANG']
        
        strhint = []
        strhint.append('locale=%s' % locale)
        strhint.append('idle=%s' % idle)
        strhint.append('interactive=%s' % interactive)
        strhint.append('cache-age=%s' % cache_age)
        self.pk.SetHints(strhint)

    def AcceptEula(self, eula_id):
        self.pk.AcceptEula(eula_id)
        self._start()

    def Cancel(self):
        self.pk.Cancel()
        self._start()

    def DownloadPackages(self, store_in_cache, package_ids):
        self.files = {}
        self.pk.connect_to_signal('Files', self._handle_files)
        self.pk.DownloadPackages(store_in_cache, package_ids)
        self._start()

    def GetCategories(self):
        self.categories = []
        self.pk.connect_to_signal('Category', self._handle_store_category)
        self.pk.GetCategories()
        self._start()

    # def GetOldTransactions # FIXME: I'm not sure need this method

    def GetPackages(self, filt):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.GetPackages(filt)
        self._start()

    def GetRepoList(self, filt):
        self.repos = []
        self.pk.connect_to_signal('RepoDetail', self._handle_repo_detail)
        self.pk.GetRepoList(filt)
        self._start()

    def GetRequires(self, filt, package_ids, recursive):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self._start()

    def GetUpdateDetail(self, package_ids):
        self.update_details = []
        self.pk.connect_to_signal('UpdateDetail', self._handle_update_detail)
        self.pk.GetUpdateDetail(package_ids)
        self._start()

    def GetUpdates(self, filt='none'):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.GetUpdates(filt)
        self._start()

    '''def GetDistroUpgrades(self):
        self.distro_upgrades = []
        self.pk.connect_to_signal('DistroUpgrade', self._handle_distro_upgrade)
        self.pk.GetDistroUpgrades()
        self._start()'''

    def InstallFiles(self, only_trusted, full_paths):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.InstallFiles(only_trusted, full_paths)
        self._start()

    def InstallPackages(self, only_trusted, package_ids):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.InstallPackages(only_trusted, package_ids)
        self._start()

    #def InstallSignature(self, sig_type, key_id, package_id):

    def RefreshCache(self, force):
        self.repos = []
        self.pk.connect_to_signal('RepoDetail', self._handle_repo_detail)
        self.pk.RefreshCache(force)
        self._start()

    def RemovePackages(self, package_ids, allow_deps, autoremove):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.RemovePackages(package_ids, allow_deps, autoremove)
        self._start()

    def RepoEnable(self, repo_id, enabled):
        self.pk.RepoEnable(repo_id, enabled)
        self._start()

    def RepoSetData(self, repo_id, param, value):
        self.pk.RepoSetData(repo_id, param, value)
        self._start()

    def Resolve(self, filt, packages_names):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.Resolve(filt, packages_names)
        self._start()

    #def Rollback(self, transaction_id):

    def SearchDetails(self, filt, values):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.SearchDetails(filt, values)
        self._start()

    def SearchFiles(self, filt, values):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.SearchFiles(filt, values)
        self._start()

    def SearchNames(self, filt, names):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.SearchNames(filt, names)
        self._start()

    def SearchGroups(self, filt, values):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.SearchGroups(filt, values)
        self._start()

    def SearchNames(self, filt, values):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.SearchNames(filt, values)
        self._start()
    
    def SimulateInstallFiles(self, full_paths):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.SimulateInstallFiles(full_paths)
        self._start()
        
    def SimulateInstallPackages(self, package_ids):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.SimulateInstallPackages(package_ids)
        self._start()

    def SimulateRemovePackages(self, package_ids, autoremove):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.SimulateRemovePackages(package_ids, autoremove)
        self._start()

    def SimulateUpdatePackages(self, package_ids):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.SimulateUpdatePackages(package_ids)
        self._start()

    def UpdatePackages(self, only_trusted, package_ids):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.UpdatePackages(only_trusted, package_ids)
        self._start()

    def UpdateSystem(self, only_trusted):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.UpdateSystem(only_trusted)
        self._start()

    def WhatProvides(self, filt, _type, values):
        self.package_summary = []
        self.pk.connect_to_signal('Package', self._handle_store_package_id)
        self.pk.WhatProvides(filt, _type, values)
        self._start()

    #def UpgradeSystem(self, distro_id, upgrade_kind):

    # Usability
    def get_packages_summary(self):
        if self.package_summary is not None:
            return self.package_summary
        return []
        
    def get_package_ids(self, filtered_arch=False, filter_arch=None):
        pkg_sum = self.get_packages_summary()
        pkg_ids = []
        for psum in pkg_sum:
            added = False
            if (filtered_arch) and (filter_arch is None):
                added = psum.is_arch()
            elif (filtered_arch) and (filter_arch is not None):
                added = psum.package_arch == filter_arch
            else:
                added = True

            if added:
                pkg_ids.append(psum.package_id)
        return pkg_ids

    def has_error(self):
        return self._error_present

    def error(self):
        return (self._error_code, self._error_description)

    def is_finished(self):
        return not self._is_started

    def set_property_changed_signal(self, handler):
        if handler is not None:
            self._s_handler_property_changed = handler

    # Services
    def _start(self):
        self._is_started = True
        self.main_loop.run()
    
    def _stop(self):
        self._is_started = False
        self.main_loop.quit()

    # Handlers
    def _handle_changed(self):
        props = self.props.GetAll('org.freedesktop.PackageKit.Transaction') 
        if self._s_handler_property_changed is not None:
            self._s_handler_property_changed(props)

    def _handle_error(self, code, description):
        print "DBus error: [%s] %s" % (code, description)
        self._error_present     = True
        self._error_code        = code
        self._error_description = description
        self._stop()
    
    def _handle_finished(self, exit_enum, runtime):
        print "DBus process finished [%s], runtime %u" % (exit_enum, runtime)
        self._stop()

    def _handle_store_package_id(self, info, package_id, summary):
        pkg_sum = PackageSummary(info, package_id, summary)
        if not pkg_sum.is_null():
            self.package_summary.append(pkg_sum)

    def _handle_store_category(self, parent_id, cat_id, name, summary, icon):
        cat_atom = {}
        cat_atom['parent_id'] = parent_id
        cat_atom['cat_id'] = cat_id
        cat_atom['name'] = name
        cat_atom['summary'] = summary
        cat_atom['icon'] = icon
        self.categories.append(cat_atom)

    def _handle_files(self, package_id, file_list):
        if self.files is not None:
            self.files[package_id] = file_list

    def _handle_repo_detail(self, repo_id, description, enabled):
        repo_detail = {}
        repo_detail['repo_id']          = repo_id
        repo_detail['description']      = description
        repo_detail['enabled']          = enabled
        
        if self.repos is not None:
            self.repos.append(repo_detail)

    def _handle_update_detail(self, 
                              package_id,
                              updates,
                              obsoletes,
                              vendor_url,
                              bugzilla_url,
                              cve_url,
                              restart,
                              update_text,
                              changelog,
                              state,
                              issued,
                              updated):
        update_detail = {}
        update_detail['package_id']     = package_id
        update_detail['updates']        = updates.split('&')
        update_detail['obsoletes']      = obsoletes.split('&')
        update_detail['vendor_url']     = vendor_url
        update_detail['bugzilla_url']   = bugzilla_url
        update_detail['cve_url']        = cve_url
        update_detail['restart']        = restart
        update_detail['update_text']    = update_text
        update_detail['changelog']      = changelog
        update_detail['state']          = state
        update_detail['issued']         = issued
        update_detail['updated']        = updated
        if self.update_details is not None:
            self.update_details.append(update_detail)


    # this is not us way (backend not supported) 
    '''def _handle_distro_upgrade(self, _type, name, summary):
        dupg = {}
        dupg['type']    = _type
        dupg['name']    = name
        dupg['summary'] = summary
        if self.distro_upgrades is not None:
            self.distro_upgrades.append(dupg)'''

class PackageKit:
    def __init__(self, main_loop = None):
        self.iface = None
        self.bus   = None
        
        #self.dbus_loop = None
        self.dbus_loop = self._init_empty_loop(main_loop)
            
        self.bus = dbus.SystemBus() 
        self.pk = self.bus.get_object('org.freedesktop.PackageKit', '/org/freedesktop/PackageKit', False)
        self.iface = dbus.Interface(self.pk, 'org.freedesktop.PackageKit')

    def getTransaction(self):
        try:
            tid = self.iface.GetTid()
        except:
            return None
        
        tiface = self.bus.get_object('org.freedesktop.PackageKit', tid, False)
        tctrl  = dbus.Interface(tiface, 'org.freedesktop.PackageKit.Transaction')
        trans = self._get_transaction_ptr(tctrl, tid, self.dbus_loop) 
                #PackageKitTransaction(tctrl, tid, self.dbus_loop)
        
        return trans

    def _get_transaction_ptr(self, tctrl, tid, dbus_loop):
        trans = PackageKitTransaction(tctrl, tid, dbus_loop)
        return trans

    def _init_empty_loop(self, main_loop):
        if main_loop is None:
            import gobject
            main_loop = gobject.MainLoop()
            DBusGMainLoop(set_as_default = True)
        return main_loop
        

def print_props(props):
    print("=== begin ===")
    for key in props.keys():
        print('\t%s=%s' % (key, props[key]))
    print("==== end ====")

if __name__ == '__main__':
    #import gobject
    #loop = gobject.MainLoop()
    pk = PackageKit()
    tr = pk.getTransaction()
    tr.set_property_changed_signal(print_props)
    if tr is None:
        print "Oops!"
    else:
        tr.SetHints()
        tr.Resolve('none', ['python3-PyQt4', 'python3-PyQt4-devel'])
        #tr.UpdateSystem(False)
        for p in tr.get_packages_summary():
            p.debug_print()
        #package_ids = tr.get_package_ids(True)

#        tr.debug_pring_list_of_dict(tr.package_ids)
#        pkg_ids = tr.get_package_ids_from_summary_list(tr.package_ids)
#        pass
#        tr2 = pk.getTransaction()
#        tr2.InstallPackages(True, package_ids)
#        tr2.debug_pring_list_of_dict(tr2.package_ids)
#        for p in tr2.get_packages_summary():
#            p.debug_print()
