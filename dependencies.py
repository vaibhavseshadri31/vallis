import pkg_resources
import secrets

installed_packages = pkg_resources.working_set
installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
                                  for i in installed_packages])

print(installed_packages_list)
