# specpattern.spec
# vim:tw=0:ts=2:sw=2:et:
#
# This SPEC file serves as a template --a typical usage pattern-- for how I
# create RPMs. The first iteration of this contained copious notes. I will
# strip all that out in favor of as clean of a spec file as possible.
#
# This is not a canonical howto, but it should be good enough to get you
# started. Let me know if you see any blatant errors or needed correction:
# t0dd_at_protonmail.com
#
# ---
#
# The pattern will build, dependent on your configuration...

# - Production (generally available or GA):
#     Source RPM (SRPM): specpattern-1.0.1-1.fc27.taw0.src.rpm
#     Binary RPM (RPM): specpattern-1.0.1-1.fc27.taw0.x86_64.rpm
# - Pre-production (testing, alpha, beta, rc, ...):
#     Source RPM (SRPM): specpattern-1.0.1-0.1.beta2.fc27.taw0.src.rpm
#     Binary RPM (RPM): specpattern-1.0.1-0.1.beta2.fc27.taw0.x86_64.rpm
# - Examples with extended snapinfo (date, git hash snippet, ...):
#     specpattern-1.0.1-0.1.beta2.20180414.fc27.taw0.src.rpm
#     specpattern-1.0.1-0.1.beta2.6bba08bgit.fc27.taw0.src.rpm
# - Examples of packaging from pre-built source archives...
#     specpattern-1.0.1-1.rp.fc27.taw0.src.rpm
#     specpattern-1.0.1-0.1.testing.rp.fc27.taw0.src.rpm
#     specpattern-1.0.1-0.1.beta2.6bba08bgit.rp.fc27.taw0.src.rpm

#
# I will bump the versions and release over time as I develop this pattern. You
# know, like a real package. :)
#
# ---
#
# Included will be...
# * a functional minimal application that can be installed on Fedora Linux,
#   CentOS, or RHEL.
# * package release flags
#   - flag for type of primary source (source code or binary pre-build)
#   - flag for type of target -- pre-production or production
#   - flag for snapinfo inclusion
#   - flag for minorbump inclusion
# * an executable
# * systemd stuff
#   - executable daemon
#   - configuration
#   - email upon start, stop, systemd-level configuration
# * documentation
#   - docs (eventually)
#   - license file
#   - man page (1 and 5) (eventually)
# * a filewalld configuration example
# * logrotation
# * application as desktop, to include menu icons and such (hicolor and
#   highcontrast)
#
# ---
#
# Further reading:
# * https://docs.fedoraproject.org/quick-docs/en-US/creating-rpm-packages.html
# * https://docs.fedoraproject.org/en-US/packaging-guidelines/
# * https://docs.fedoraproject.org/en-US/packaging-guidelines/#_filesystem_layout
# * https://developer.fedoraproject.org/deployment/rpm/about.html
# * https://rpm-packaging-guide.github.io/
# * http://rpm-guide.readthedocs.io/en/latest/
# * http://backreference.org/2011/09/17/some-tips-on-rpm-conditional-macros/
# A note about specfile comments: commented out macros have to have their %'s
# doubled up in comments in order to have them properly escaped.
#
# ---
#
# Package (RPM) name-version-release.
#
# <name>-<version>-<release>
# ...version is (can be many decimals):
# <vermajor>.<verminor>
# ...where release is:
# <pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]
# ...all together now:
# <name>-<vermajor.<verminor>-<pkgrel>[.<extraver>][.<snapinfo>].DIST[.<minorbump>]
#
# Note about the pattern for release iterations (ie. the release value of
# name-version-release):
#     If you are still in development, but the production package is expected
#     to have a release value of 8 (previous release was 7) for example, you
#     always work one step back (in the 7's) and add another significant digit.
#     I.e., release value of 7.1, 7.2, 7.3, etc... are all pre-production
#     release nomenclatures for an eventual release numbered at 8. When we go
#     into production, we "round up" and drop the decimal and probably all the
#     snapinfo as well.  specpattern-1.0.1-7.3.beta2 --> specpattern-1.0.1-8
#
# Source tarballs that I am using to create this...
# - specpattern-1.0.1.tar.gz
# - specpattern-1.0-contrib.tar.gz
#

Name: specpattern
Summary: A packaging example/template (a pattern)
#BuildArch: noarch

%define targetIsProduction 0
%define sourceIsPrebuilt 0


# VERSION - can edit
# eg. 1.0.1
%define vermajor 1.0
%define verminor 1
Version: %{vermajor}.%{verminor}


# RELEASE - can edit
%if %{targetIsProduction}
  %define _pkgrel 1
%else
  %define _pkgrel 0.14
%endif

# MINORBUMP - can edit
%undefine minorbump
%define minorbump taw

#
# Build the release string - don't edit this
#

# rp = repackaged
# eg. 1.rp (prod) or 0.6.testing.rp (pre-prod)
%define _snapinfo testing
%if %{targetIsProduction}
  %undefine _snapinfo
%endif
%define _snapinfo_rp rp
%if ! %{sourceIsPrebuilt}
   %undefine _snapinfo_rp
%endif
%if 0%{?_snapinfo:1}
  %if 0%{?_snapinfo_rp:1}
    %define snapinfo %{_snapinfo}.%{_snapinfo_rp}
  %else
    %define snapinfo %{_snapinfo}
  %endif
%else
  %if 0%{?_snapinfo_rp:1}
    %define snapinfo %{_snapinfo_rp}
  %else
    %undefine snapinfo
  %endif
%endif

# _pkgrel will be defined, snapinfo and minorbump may not be
%define _release %{_pkgrel}
%if 0%{?snapinfo:1}
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}.%{snapinfo}%{?dist}
  %endif
%else
  %if 0%{?minorbump:1}
    %define _release %{_pkgrel}%{?dist}.%{minorbump}
  %else
    %define _release %{_pkgrel}%{?dist}
  %endif
%endif

Release: %{_release}
# ----------- end of release building section

# You can/should use URLs for sources as well. That is beyond the scope of
# this example.
# https://docs.fedoraproject.org/en-US/packaging-guidelines/SourceURL/
# https://docs.fedoraproject.org/en-US/packaging-guidelines/SourceURL/#_git_hosting_services
#Source0: https://github.com/PROJECT_NAME/%%{name}/releases/download/v%%{version}/%%{name}-%%{version}.tar.gz
#Source0: https://github.com/PROJECT_NAME/%%{name}/archive/v%%{version}/%%{name}-%%{version}.tar.gz
Source0: https://github.com/taw00/howto/raw/master/source/SOURCES/%{name}-%{version}.tar.gz
Source1: https://github.com/taw00/howto/raw/master/source/SOURCES/%{name}-%{vermajor}-contrib.tar.gz

# Most of the time, the build system can figure out the requires.
# But if you need something specific...
Requires: gnome-terminal
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
Requires: firewalld-filesystem
Requires(post): firewalld-filesystem
Requires(postun): firewalld-filesystem

%if 0%{?suse_version:1}
# https://en.opensuse.org/openSUSE:Build_Service_cross_distribution_howto
# mock builds of suse don't include cacerts for some reason
BuildRequires: ca-certificates-cacert ca-certificates-mozilla ca-certificates
BuildRequires: desktop-file-utils appstream-glib
%else
# Required for desktop applications (validation of .desktop and .xml files)
BuildRequires: desktop-file-utils libappstream-glib
%endif


# systemd stuff
# As per https://docs.fedoraproject.org/en-US/packaging-guidelines/Systemd/
# Oddly, contrary to the docs, systemd-rpm-macros doesn't exist
#BuildRequires: systemd systemd-rpm-macros
#Requires(post): systemd
#Requires(preun): systemd
#Requires(postun): systemd
BuildRequires: systemd
%{?systemd_requires}

#t0dd: for build environment introspection
%if ! %{targetIsProduction}
BuildRequires: tree vim-enhanced less findutils
%endif


# obsolete fictitious previous version of package after a rename
Provides: spec-pattern = 0.9
Obsoletes: spec-pattern < 0.9


# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing
# https://spdx.org/licenses/ (these differ!?!)
License: MIT
URL: https://github.com/taw00/howto
# Note, for example, this will not build on ppc64le
ExclusiveArch: x86_64 i686 i386
# Group, Vendor, Packager, and more is no longer used. Left here as a reminder...
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_tags_and_sections
#Group: Unspecified

# CHANGE or DELETE this for your package
# System user for the systemd specpatternd.service.
# If you want to retain the systemd service configuration and you therefore
# change this, you will have to dig into the various -contrib configuration
# files to change things there as well.
%define systemuser spuser
%define systemgroup spgroup


# If you comment out "debug_package" RPM will create additional RPMs that can
# be used for debugging purposes. I am not an expert at this, BUT ".build_ids"
# are associated to debug packages, and I have lately run into packaging
# conflicts because of them. This is a topic I can't share a whole lot of
# wisdom about, but for now... I turn all that off.
#
# How debug info and build_ids managed (I only halfway understand this):
# https://github.com/rpm-software-management/rpm/blob/master/macros.in
# ...flip-flop next two lines in order to disable (nil) or enable (1) debuginfo package build
%define debug_package 1
%define debug_package %{nil}
%define _unique_build_ids 1
%define _build_id_links alldebug

# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_pie
%define _hardened_build 1

# Extracted source tree structure (extracted in {_builddir})
#   sourceroot               {name}-1.0
#      \_sourcetree             \_{name}-1.0.1
#      \_sourcetree_contrib     \_{name}-1.0-contrib
%define sourceroot %{name}-%{vermajor}
%define sourcetree %{name}-%{version}
%define sourcetree_contrib %{name}-%{vermajor}-contrib
# /usr/share/specpattern
%define installtree %{_datadir}/%{name}


# RHEL5 and below need this defined.
#BuildRoot: %%{_topdir}/BUILDROOT/


%description
This Spec Pattern RPM serves as a packaging example/template (a pattern). It
includes a simple application that serves to demonstrate how to configure
and deploy a graphical desktop application, systemd service, and more.


%prep
# Prep section starts us in directory .../BUILD -or- {_builddir}
# - This step extracts all code archives and takes any preparatory steps
#   necessary prior to the build.
#
# References (the docs for this universally suck):
# * http://ftp.rpm.org/max-rpm/s1-rpm-inside-macros.html
# * http://rpm.org/user_doc/autosetup.html
# * autosetup -q and setup -q leave out the root directory.

#rm -rf %%{sourceroot} ; mkdir -p %%{sourceroot}
mkdir -p %{sourceroot}
# sourcecode
%setup -q -T -D -a 0 -n %{sourceroot}
# contrib
%setup -q -T -D -a 1 -n %{sourceroot}

# Libraries ldconfig file - we create it, because lib or lib64
echo "%{_libdir}/%{name}" > %{sourcetree_contrib}/etc-ld.so.conf.d_%{name}.conf

# README message about the /var/lib/specpattern directory
echo "\
This directory only exists as an example data directory

The %{systemuser} home dir is here: /var/lib/%{name}
The systemd managed %{name} datadir is also here: /var/lib/%{name}
The %{name} config file is housed here: /etc/%{name}/%{name}.conf
" > %{sourcetree_contrib}/systemd/var-lib-%{name}_README

# For debugging purposes...
cd .. ; /usr/bin/tree -df -L 1 %{sourceroot} ; cd -

%if 0%{?suse_version:1}
  echo "======== Opensuse version: %{suse_version}"
%endif

%if 0%{?fedora:1}
  echo "======== Fedora version: %{fedora}"
%if 0%{?fedora} < 28
  echo "Fedora 27 and older can't be supported. Sorry."
  exit 1
%endif
%endif

%if 0%{?rhel:1}
  echo "======== EL version: %{rhel}"
%if 0%{?rhel} < 7
  echo "EL 6 and older can't be supported. Sorry."
  exit 1
%endif
%if 0%{?rhel} >= 8
  echo "EL 8 and newer is untested thus far. Good luck."
%endif
%endif


##
## Building the RPM: prep --> build --> install --> files
##


%build
# This section starts us in directory {_builddir}/{sourceroot}
# - This step performs any action that takes the code and turns it into a
#   runnable form. Usually by compiling.

# I do this for all npm processed applications...
# Clearing npm's cache will hopefully elminate SHA1 integrity issues.
#/usr/bin/npm cache clean --force
#rm -rf ../.npm/_cacache
#rm -f %%{sourcetree}/package-lock.json

## Man Pages - not used as of yet
#gzip %%{buildroot}%%{_mandir}/man1/*.1

cd %{sourcetree}
# <insert program building instructions here>


%install
# This section starts us in directory {_builddir}/{sourceroot}
# - This step moves anything needing to be part of the package into the
#   {buildroot}, therefore mirroring the final directory and file structure of
#   an installed RPM.

# Cheatsheet for built-in RPM macros:
# https://docs.fedoraproject.org/en-US/packaging-guidelines/RPMMacros/
#   _builddir = {_topdir}/BUILD
#   _buildrootdir = {_topdir}/BUILDROOT
#   buildroot = {_buildrootdir}/{name}-{version}-{release}.{_arch}
#   _bindir = /usr/bin
#   _sbindir = /usr/sbin
#   _datadir = /usr/share
#   _mandir = /usr/share/man
#   _sysconfdir = /etc
#   _localstatedir = /var
#   _sharedstatedir is /var/lib
#   _prefix or _usr = /usr
#   _libdir = /usr/lib or /usr/lib64 (depending on system)
# The _rawlib define is used to quiet rpmlint who can't seem to understand
# that /usr/lib is still used for certain things.
%define _rawlib lib
%define _usr_lib /usr/%{_rawlib}
# These three are defined in some versions of RPM and not in others.
%if ! 0%{?_unitdir:1}
  %define _unitdir %{_usr_lib}/systemd/system
%endif
%if ! 0%{?_tmpfilesdir:1}
  %define _tmpfilesdir %{_usr_lib}/tmpfiles.d
%endif
%if ! 0%{?_metainfodir:1}
  %define _metainfodir %{_datadir}/metainfo
%endif


# Create directories
# /usr/[lib,lib64]/specpattern/
install -d %{buildroot}%{_libdir}/%{name}
# /usr/bin/ and /usr/sbin/
install -d -m755 -p %{buildroot}%{_bindir}
install -d -m755 -p %{buildroot}%{_sbindir}
# /usr/share/applications/
install -d %{buildroot}%{_datadir}/applications
# /usr/share/metainfo/
install -d %{buildroot}%{_metainfodir}
# /etc/ld.so.conf.d/
install -d %{buildroot}%{_sysconfdir}/ld.so.conf.d
# /etc/specpattern/
install -d %{buildroot}%{_sysconfdir}/%{name}
# /var/lib/specpattern/...
install -d %{buildroot}%{_sharedstatedir}/%{name}
# /var/log/specpattern/
install -d -m750 %{buildroot}%{_localstatedir}/log/%{name}
# /usr/share/specpattern/
install -d %{buildroot}%{installtree}

# Create directories (systemd stuff)
# /usr/lib/systemd/system/
install -d %{buildroot}%{_unitdir}
# /etc/sysconfig/specpatternd-scripts/
install -d %{buildroot}%{_sysconfdir}/sysconfig/%{name}d-scripts
# /usr/lib/tmpfiles.d/
install -d %{buildroot}%{_tmpfilesdir}

# Binaries - a little ugly - symbolic link creation
ln -s %{installtree}/%{name}-gnome-terminal.sh %{buildroot}%{_bindir}/%{name}
ln -s %{installtree}/%{name}-daemon.sh %{buildroot}%{_sbindir}/%{name}d
install -D -p %{sourcetree}/%{name}-gnome-terminal.sh %{buildroot}%{installtree}/%{name}-gnome-terminal.sh
install -D -p %{sourcetree}/%{name}-daemon.sh %{buildroot}%{installtree}/%{name}-daemon.sh
install -D -p %{sourcetree}/%{name}-process.sh %{buildroot}%{installtree}/%{name}-process.sh

# Desktop
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.hicolor.16x16.png   %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.hicolor.22x22.png   %{buildroot}%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.hicolor.24x24.png   %{buildroot}%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.hicolor.32x32.png   %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.hicolor.48x48.png   %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.hicolor.128x128.png %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.hicolor.256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.hicolor.512x512.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.hicolor.svg         %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.highcontrast.16x16.png   %{buildroot}%{_datadir}/icons/HighContrast/16x16/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.highcontrast.22x22.png   %{buildroot}%{_datadir}/icons/HighContrast/22x22/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.highcontrast.24x24.png   %{buildroot}%{_datadir}/icons/HighContrast/24x24/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.highcontrast.32x32.png   %{buildroot}%{_datadir}/icons/HighContrast/32x32/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.highcontrast.48x48.png   %{buildroot}%{_datadir}/icons/HighContrast/48x48/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.highcontrast.128x128.png %{buildroot}%{_datadir}/icons/HighContrast/128x128/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.highcontrast.256x256.png %{buildroot}%{_datadir}/icons/HighContrast/256x256/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.highcontrast.512x512.png %{buildroot}%{_datadir}/icons/HighContrast/512x512/apps/%{name}.png
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.highcontrast.svg         %{buildroot}%{_datadir}/icons/HighContrast/scalable/apps/%{name}.svg

# specpattern.desktop
# https://docs.fedoraproject.org/en-US/packaging-guidelines/#_desktop_files
# https://fedoraproject.org/wiki/NewMIMESystem
install -m755  %{sourcetree_contrib}/desktop/%{name}.wrapper.sh %{buildroot}%{_bindir}/
desktop-file-install --dir=%{buildroot}%{_datadir}/applications/ %{sourcetree_contrib}/desktop/%{name}.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

# specpattern.appdata.xml
# https://docs.fedoraproject.org/en-US/packaging-guidelines/AppData/
# https://fedoraproject.org/wiki/NewMIMESystem
install -D -m644 -p %{sourcetree_contrib}/desktop/%{name}.appdata.xml %{buildroot}%{_metainfodir}/%{name}.appdata.xml
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/*.appdata.xml

# Libraries
#install -D -m755 -p %%{buildroot}%%{installtree}/libffmpeg.so %%{buildroot}%%{_libdir}/%%{name}/libffmpeg.so
#install -D -m755 -p %%{buildroot}%%{installtree}/libnode.so %%{buildroot}%%{_libdir}/%%{name}/libnode.so
install -D -m644 -p %{sourcetree_contrib}/etc-ld.so.conf.d_%{name}.conf %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}.conf

## Man Pages - not used as of yet
#install -d %%{buildroot}%%{_mandir}
#install -D -m644 %%{sourcetree}/share/man/man1/* %%{buildroot}%%{_mandir}/man1/

## Bash completion
#install -D -m644 %%{sourcetree_contrib}/bash/%%{name}.bash-completion  %%{buildroot}%%{_datadir}/bash-completion/completions/%%{name}
#install -D -m644 %%{sourcetree_contrib}/bash/%%{name}d.bash-completion %%{buildroot}%%{_datadir}/bash-completion/completions/%%{name}d

# Config
install -D -m640 %{sourcetree_contrib}/systemd/etc-%{name}_%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/%{name}.conf
install -D -m644 %{sourcetree_contrib}/systemd/etc-%{name}_%{name}.conf %{sourcetree_contrib}/%{name}.conf.example

# README message about the /var/lib/specpattern directory
install -D -m644 %{sourcetree_contrib}/systemd/var-lib-%{name}_README %{buildroot}%{_sharedstatedir}/%{name}/README

# System services
install -D -m600 -p %{sourcetree_contrib}/systemd/etc-sysconfig_%{name}d %{buildroot}%{_sysconfdir}/sysconfig/%{name}d
install -D -m755 -p %{sourcetree_contrib}/systemd/etc-sysconfig-%{name}d-scripts_send-email.sh %{buildroot}%{_sysconfdir}/sysconfig/%{name}d-scripts/send-email.sh
install -D -m755 -p %{sourcetree_contrib}/systemd/etc-sysconfig-%{name}d-scripts_config-file-check.sh %{buildroot}%{_sysconfdir}/sysconfig/%{name}d-scripts/config-file-check.sh
install -D -m755 -p %{sourcetree_contrib}/systemd/etc-sysconfig-%{name}d-scripts_write-to-journal.sh %{buildroot}%{_sysconfdir}/sysconfig/%{name}d-scripts/write-to-journal.sh
install -D -m644 -p %{sourcetree_contrib}/systemd/usr-lib-systemd-system_%{name}d.service %{buildroot}%{_unitdir}/%{name}d.service
install -D -m644 -p %{sourcetree_contrib}/systemd/usr-lib-tmpfiles.d_%{name}d.conf %{buildroot}%{_tmpfilesdir}/%{name}d.conf

# Log files
# ...logrotate file rules
install -D -m644 -p %{sourcetree_contrib}/logrotate/etc-logrotate.d_%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
# ...ghosted log files - need to exist in the installed buildroot
touch %{buildroot}%{_localstatedir}/log/%{name}/debug.log

# Service definition files for firewalld
install -D -m644 -p %{sourcetree_contrib}/firewalld/usr-lib-firewalld-services_%{name}.xml %{buildroot}%{_usr_lib}/firewalld/services/%{name}.xml

# Note that we do not do this... cuz, init.d is dead. I leave it for pedantic completness
# /etc/init.d/
#install -d %%{buildroot}%%{_sysconfdir}/init.d
#install -D -m755 %%{sourcetree_contrib}/systemd/etc-init.d_specpatternd.init %%{buildroot}%%{_sysconfdir}/init.d/specpatternd.init


%files
# This section starts us in directory {_buildrootdir} (I think)
# (note that macros like %%docs, %%licence, etc may locate in
# {_builddir}/{sourceroot})
# - This step makes a declaration of ownership of any listed directories
#   or files
# - The install step should have set permissions and ownership correctly,
#   but of final tweaking is often done in this section
#
%defattr(-,root,root,-)
%license %{sourcetree}/LICENSE

# The directories...
# /etc/specpattern/
%dir %attr(750,%{systemuser},%{systemgroup}) %{_sysconfdir}/%{name}
# /var/lib/specpattern/
%dir %attr(750,%{systemuser},%{systemgroup}) %{_sharedstatedir}/%{name}
# /var/log/specpattern/
%dir %attr(750,%{systemuser},%{systemgroup}) %{_localstatedir}/log/%{name}
# /etc/sysconfig/specpatternd-scripts/
%dir %attr(755,%{systemuser},%{systemgroup}) %{_sysconfdir}/sysconfig/%{name}d-scripts
# /usr/share/specpattern/
%dir %attr(755,%{systemuser},%{systemgroup}) %{_datadir}/%{name}
# /usr/[lib,lib64]/specpattern/
%dir %attr(755,root,root) %{_libdir}/%{name}

%defattr(-,%{systemuser},%{systemgroup},-)
# /var/lib/specpattern/*
%attr(-,%{systemuser},%{systemgroup}) %{_sharedstatedir}/%{name}/*
%defattr(-,root,root,-)

# Documentation
# no manpage examples yet
#%%{_mandir}/man1/*.1.gz
#%%{_docsdir}/*
# config example
%doc %{sourcetree_contrib}/%{name}.conf.example

# Binaries
%{_bindir}/%{name}
%{_bindir}/%{name}.wrapper.sh
%{_sbindir}/%{name}d
%defattr(-,%{systemuser},%{systemgroup},-)
%{_datadir}/%{name}/%{name}-process.sh
%{_datadir}/%{name}/%{name}-daemon.sh
%{_datadir}/%{name}/%{name}-gnome-terminal.sh
%defattr(-,root,root,-)

# systemd service definition
%{_unitdir}/%{name}d.service

# systemd service tmp file
%{_tmpfilesdir}/%{name}d.conf

# systemd service config and scripts
%config(noreplace) %attr(600,root,root) %{_sysconfdir}/sysconfig/%{name}d
%attr(755,root,root) %{_sysconfdir}/sysconfig/%{name}d-scripts/send-email.sh
%attr(755,root,root) %{_sysconfdir}/sysconfig/%{name}d-scripts/config-file-check.sh
%attr(755,root,root) %{_sysconfdir}/sysconfig/%{name}d-scripts/write-to-journal.sh

# application configuration when run as systemd service
%config(noreplace) %attr(640,%{systemuser},%{systemgroup}) %{_sysconfdir}/%{name}/%{name}.conf

# /var/lib/specpattern/README
%attr(640,%{systemuser},%{systemgroup}) %{_sharedstatedir}/%{name}/README

# firewalld service definition
%{_usr_lib}/firewalld/services/%{name}.xml

# Desktop
%{_datadir}/icons/*
%{_datadir}/applications/%{name}.desktop
%{_metainfodir}/%{name}.appdata.xml
#%%{_metainfodir}/%%{name}.metainfo.xml

# Libraries
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
#%%{_libdir}/%%{name}/libffmpeg.so
#%%{_libdir}/%%{name}/libnode.so

# Logs
# log file - doesn't initially exist, but we still own it
%ghost %{_localstatedir}/log/%{name}/debug.log
%attr(644,root,root) %{_sysconfdir}/logrotate.d/%{name}


##
## Installing/Uninstalling the RPM: pre, post, posttrans, preun, postun
##


%pre
# This section starts us in directory {_builddir}/{sourceroot}
# an installation step (runs right prior to installation)
# - system users are added if needed. Any other roadbuilding.
#
# Note that _sharedstatedir is /var/lib and /var/lib/specpattern will be the homedir
# for spuser
#
# This is for the case where you run specpattern as a service (systemctl start specpatternd)
getent group %{systemgroup} >/dev/null || groupadd -r %{systemgroup}
getent passwd %{systemuser} >/dev/null || useradd -r -g %{systemgroup} -d %{_sharedstatedir}/%{name} -s /sbin/nologin -c "System user '%{systemuser}' to isolate execution" %{systemuser}


%post
# an installation step (runs after install process is complete)
# This section starts us in directory {_builddir}/{sourceroot}
umask 007
# refresh library context
/sbin/ldconfig > /dev/null 2>&1

# refresh systemd context
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_scriptlets
#test -e %%{_sysconfdir}/%%{name}/%%{name}.conf && %%systemd_post %%{name}d.service
%systemd_post %{name}d.service

# refresh firewalld context
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
#test -f %%{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true
%firewalld_reload

# Update the desktop database
# https://fedoraproject.org/wiki/NewMIMESystem
/usr/bin/update-desktop-database &> /dev/null || :


%posttrans
/usr/bin/systemd-tmpfiles --create
#TODO: Replace above with %%tmpfiles_create_package macro
#TODO: https://github.com/systemd/systemd/blob/master/src/core/macros.systemd.in


%preun
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_scriptlets
%systemd_preun %{name}d.service


%postun
# an uninstallation step (runs after uninstall process is complete)
# This section starts us in directory {_builddir}/{sourceroot}
umask 007
# refresh library context
/sbin/ldconfig > /dev/null 2>&1

# refresh firewalld context
# https://fedoraproject.org/wiki/PackagingDrafts/ScriptletSnippets/Firewalld
#test -f %%{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true
%firewalld_reload

# Update the desktop database
# https://fedoraproject.org/wiki/NewMIMESystem
/usr/bin/update-desktop-database &> /dev/null || :
# systemd stuff
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/#_scriptlets
%systemd_postun %{name}d.service


#%%clean
# No longer used.


%changelog
* Fri Jul 23 2021 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.14.testing.taw
  - genericized the rpm-version-specific macros

* Wed Mar 27 2019 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.13.testing.taw
  - added os versioning examples
  - cleaned up some things in the specfile as well

* Thu Dec 13 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.12.testing.taw
  - added an example wrapper script that specpattern.desktop will call  
    and can be used if a derived application is sensitive to certain bugs in  
    the QT5+GNOME+Wayland environment or KDE+Electron.

* Mon Dec 10 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.11.testing.taw
  - cleaned up firewalld_reloads and systemd_stuff

* Thu Dec 06 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.10.testing.taw
  - cleaned up a lot of links

* Fri Nov 23 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.9.testing.taw
  - Fix systemd config in spec file for postun, etc.
  - Some simplification of the release string logic.
  - /usr/share/applications/specpatternd.desktop file Exec line updated to  
    work better with KDA Plasma desktops. Something to do with an electron  
    bug or somesuch. Now it reads:  
    `Exec=env XDG_CURRENT_DESKTOP=Unity /usr/bin/riot`  
    instead of `Exec=/usr/bin/specpattern`

* Wed May 23 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.8.testing.taw
  - locking down supported architectures w/ ExclusiveArch

* Thu May 10 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.7.testing.taw1
  - spec file change:
    - mkdir -p not just mkdir cuz... what if it is already populated.
    - consider rm -rf ... && mkdir -p ... instead.

* Sun May 06 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.7.testing.taw0
  - Tweaked the .desktop and .appdata.xml files a bit (more conforming)
  - Reduced a bit of noise in the specfile comments. Only a bit. :)
  - Source[n] values are now URLs as they should be.

* Mon Apr 30 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.6.testing.taw[n]
  - Fixed some errors in the systemd scripts.
  - Improved some comments.
  - Simplified some scripting.

* Sat Apr 28 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.5.testing.taw[n]
  - Deployed .desktop file correctly and include an .appdata.xml file.

* Thu Apr 26 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.4.testing.taw[n]
  - cleanup - version and release build should all be together.

* Tue Apr 24 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.3.testing.taw[n]
  - Further simplified the snapinfo, minorbump, and repackage logic.
  - Issue warnings if your production and snapinfo settings are atypical.

* Sun Apr 22 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.2.testing.taw[n]
  - Simplified the snapinfo logic.
  - Updated the desktop icons.
  - Added a simple little specpattern loop program that runs in a terminal  
    or is daemonized.
  - Added systemd and firewalld service definitions. Added logrotation rules.
  - Logs nicely to the journal.

* Sat Apr 14 2018 Todd Warner <t0dd_at_protonmail.com> 1.0.1-0.1.testing.taw[n]
  - Initial test build.
